import json
from pathlib import Path

import pytest

from open_acp.models.artifacts import StageArtifact
from open_acp.pipeline_defs.pipeline_loader import PipelineDefinition, StageDefinition


class SequenceClaude:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def generate(self, prompt: str, system: str = "", **kwargs) -> str:
        self.calls.append({"prompt": prompt, "system": system, "kwargs": kwargs})
        if not self.responses:
            raise AssertionError("No fake Claude responses left")
        next_response = self.responses.pop(0)
        if callable(next_response):
            return next_response(prompt, system)
        return next_response


def _valid_objectives() -> dict:
    return {
        "objectives": [
            {
                "id": "obj_1",
                "statement": "Explain the main concept with one concrete example and one trade-off.",
                "bloom_level": "understand",
                "skill_ids": ["skill_1"],
                "assessment_method": "short_answer",
            }
        ]
    }


def _review_pass() -> dict:
    return {
        "summary": "Looks good.",
        "findings": [
            {
                "criterion": "Objectives are measurable",
                "status": "PASS",
                "detail": "The objective uses an observable verb and concrete condition.",
            }
        ],
    }


def _review_fail() -> dict:
    return {
        "summary": "Needs revision.",
        "findings": [
            {
                "criterion": "Objectives are measurable",
                "status": "FAIL",
                "detail": "The objective is not specific enough for assessment.",
            }
        ],
    }


def _make_executor(monkeypatch, tmp_path, responses):
    import open_acp.loops.loop_c.pipeline_executor as pipeline_executor_module

    fake_claude = SequenceClaude(responses)
    monkeypatch.setattr(pipeline_executor_module, "ClaudeClient", lambda: fake_claude)
    executor = pipeline_executor_module.PipelineExecutor(output_dir=str(tmp_path))
    return executor, fake_claude


def _make_stage() -> StageDefinition:
    return StageDefinition(
        id="objectives",
        skill="pipelines/concept_explainer/02_objectives",
        tools=["claude_generate"],
        artifact_schema="objectives.schema.json",
        review_focus=["Objectives are measurable"],
        success_criteria=["Objectives use a clear Bloom verb"],
        model_tier="strong",
    )


def _make_pipeline(review_max_rounds: int = 2) -> PipelineDefinition:
    return PipelineDefinition(
        pipeline_id="concept_explainer",
        content_type="concept_explainer",
        display_name="Concept Explainer Session",
        strict_execution=True,
        review_max_rounds=review_max_rounds,
        stages=[],
    )


def _module_context() -> dict:
    return {
        "module_id": "m1",
        "title": "Test Module",
        "estimated_hours": 1.0,
        "pedagogy_profile": "concept_progression",
    }


def test_executor_retries_after_invalid_json(monkeypatch, tmp_path):
    executor, _ = _make_executor(
        monkeypatch,
        tmp_path,
        responses=[
            "this is not json",
            json.dumps(_valid_objectives()),
            json.dumps(_review_pass()),
        ],
    )

    artifact = executor._execute_stage(
        stage=_make_stage(),
        pipeline_def=_make_pipeline(),
        previous_artifacts={},
        module_context=_module_context(),
        domain="genai",
    )

    assert artifact.attempts == 2
    assert artifact.validated is True
    assert artifact.review_decision == "PASS"


def test_executor_retries_after_schema_failure(monkeypatch, tmp_path):
    executor, _ = _make_executor(
        monkeypatch,
        tmp_path,
        responses=[
            json.dumps({"objectives": [{"id": "obj_1"}]}),
            json.dumps(_valid_objectives()),
            json.dumps(_review_pass()),
        ],
    )

    artifact = executor._execute_stage(
        stage=_make_stage(),
        pipeline_def=_make_pipeline(),
        previous_artifacts={},
        module_context=_module_context(),
        domain="genai",
    )

    assert artifact.attempts == 2
    assert artifact.validated is True
    assert artifact.validation_errors == []


def test_executor_retries_after_review_failure(monkeypatch, tmp_path):
    executor, _ = _make_executor(
        monkeypatch,
        tmp_path,
        responses=[
            json.dumps(_valid_objectives()),
            json.dumps(_review_fail()),
            json.dumps(_valid_objectives()),
            json.dumps(_review_pass()),
        ],
    )

    artifact = executor._execute_stage(
        stage=_make_stage(),
        pipeline_def=_make_pipeline(),
        previous_artifacts={},
        module_context=_module_context(),
        domain="genai",
    )

    assert artifact.attempts == 2
    assert artifact.review_decision == "PASS"


def test_executor_aborts_after_max_review_rounds(monkeypatch, tmp_path):
    executor, _ = _make_executor(
        monkeypatch,
        tmp_path,
        responses=[
            json.dumps(_valid_objectives()),
            json.dumps(_review_fail()),
            json.dumps(_valid_objectives()),
            json.dumps(_review_fail()),
        ],
    )

    with pytest.raises(RuntimeError, match="Strict execution failed"):
        executor._execute_stage(
            stage=_make_stage(),
            pipeline_def=_make_pipeline(review_max_rounds=1),
            previous_artifacts={},
            module_context=_module_context(),
            domain="genai",
        )


def test_executor_injects_pedagogy_and_style_context_into_prompt(monkeypatch, tmp_path):
    executor, fake_claude = _make_executor(
        monkeypatch,
        tmp_path,
        responses=[
            json.dumps(_valid_objectives()),
            json.dumps(_review_pass()),
        ],
    )

    executor._execute_stage(
        stage=_make_stage(),
        pipeline_def=_make_pipeline(),
        previous_artifacts={},
        module_context=_module_context(),
        domain="genai",
    )

    prompt = fake_claude.calls[0]["prompt"]
    assert "Pedagogy Profile: concept_progression" in prompt
    assert "## Pedagogy Core" in prompt
    assert "## Brand Guidelines" in prompt
    assert "## Format Guidelines" in prompt
    assert "## Domain Guidelines" in prompt


def test_execute_review_stage_writes_review_packet(monkeypatch, tmp_path):
    executor, _ = _make_executor(
        monkeypatch,
        tmp_path,
        responses=[
            json.dumps(_valid_objectives()),
            json.dumps(_review_pass()),
        ],
    )
    pipeline = _make_pipeline()
    pipeline.stages = [_make_stage()]
    monkeypatch.setattr(executor.pipeline_loader, "load", lambda _: pipeline)

    result = executor.execute_review_stage(
        content_type="concept_explainer",
        module_context=_module_context(),
        domain="genai",
    )

    assert result["status"] == "awaiting_review"
    assert result["stage_id"] == "objectives"
    assert result["next_stage_id"] is None

    review_md = Path(result["review_packet_paths"]["markdown"])
    review_json = Path(result["review_packet_paths"]["json"])
    assert review_md.exists()
    assert review_json.exists()
    assert "Key Decisions" in review_md.read_text(encoding="utf-8")


def test_execute_review_stage_resumes_after_saved_artifact(monkeypatch, tmp_path):
    executor, _ = _make_executor(
        monkeypatch,
        tmp_path,
        responses=[
            json.dumps(_valid_objectives()),
            json.dumps(_review_pass()),
        ],
    )

    first_stage = _make_stage()
    second_stage = StageDefinition(
        id="outline",
        skill=first_stage.skill,
        tools=first_stage.tools,
        artifact_schema=first_stage.artifact_schema,
        review_focus=first_stage.review_focus,
        success_criteria=first_stage.success_criteria,
        model_tier=first_stage.model_tier,
    )
    pipeline = _make_pipeline()
    pipeline.stages = [first_stage, second_stage]
    monkeypatch.setattr(executor.pipeline_loader, "load", lambda _: pipeline)

    saved = StageArtifact(
        artifact_id="art_existing",
        stage_id="objectives",
        pipeline_id="concept_explainer",
        content_type="concept_explainer",
        data=_valid_objectives(),
        schema_path="objectives.schema.json",
        created_at="2026-04-16T00:00:00+00:00",
        validated=True,
        review_decision="PASS",
        review_summary="Looks good.",
        review_findings=[],
    )
    executor._save_artifact(saved, "concept_explainer", "m1")

    result = executor.execute_review_stage(
        content_type="concept_explainer",
        module_context=_module_context(),
        domain="genai",
    )

    assert result["stage_id"] == "outline"
    assert result["next_stage_id"] is None
