from pathlib import Path

from open_acp.loops.loop_a.nodes import _build_bootstrap_warnings, _load_raw_sources
from open_acp.models.signals import SignalBatch, RawSignal, ChannelCategory, ChannelType
from open_acp.orchestrator.loop_review import LoopReviewRunner


def test_loop_review_runner_executes_first_loop_a_stage(monkeypatch, tmp_path):
    runner = LoopReviewRunner(output_dir=str(tmp_path))

    def fake_stage(state):
        return {
            "signal_batch": SignalBatch(
                batch_id="batch_1",
                signals=[
                    RawSignal(
                        signal_id="sig_1",
                        channel_category=ChannelCategory.INDUSTRY_MARKET,
                        channel_name="sources",
                        content="Python remains important for GenAI.",
                        timestamp="2026-04-16T00:00:00+00:00",
                        signal_type=ChannelType.PROACTIVE,
                        metadata={"filename": "genai_120hr_curriculum.md"},
                    )
                ],
                ingested_at="2026-04-16T00:00:00+00:00",
                source_domain="genai",
            ),
            "bootstrap_warnings": ["Using shared market inputs for now."],
        }

    monkeypatch.setattr(runner, "_load_stage_callable", lambda loop_id, stage_id: fake_stage)

    result = runner.execute_review_stage(
        loop_id="loop_a",
        base_state={"domain": "genai", "cycle_id": "cycle_a"},
    )

    assert result["status"] == "awaiting_review"
    assert result["stage_id"] == "ingest_signals"
    assert result["next_stage_id"] == "detect_patterns"
    assert "Bootstrap mode is active" in result["review_packet"]["summary"]
    assert "genai_120hr_curriculum.md" in result["review_packet"]["key_decisions"][1]
    assert "Using shared market inputs for now." in result["review_packet"]["key_decisions"]
    assert Path(result["review_packet_paths"]["markdown"]).exists()
    assert Path(result["state_path"]).exists()


def test_loop_review_runner_resumes_next_stage(monkeypatch, tmp_path):
    runner = LoopReviewRunner(output_dir=str(tmp_path))

    def fake_callable(loop_id, stage_id):
        if stage_id == "ingest_signals":
            return lambda state: {
                "signal_batch": SignalBatch(
                    batch_id="batch_1",
                    signals=[
                        RawSignal(
                            signal_id="sig_1",
                            channel_category=ChannelCategory.INDUSTRY_MARKET,
                            channel_name="sources",
                            content="RAG and Python remain important.",
                            timestamp="2026-04-16T00:00:00+00:00",
                            signal_type=ChannelType.PROACTIVE,
                            metadata={"filename": "genai_120hr_curriculum.md"},
                        )
                    ],
                    ingested_at="2026-04-16T00:00:00+00:00",
                    source_domain="genai",
                )
            }
        return lambda state: {
            "detected_patterns": [{"pattern_id": "p1", "description": "Demand for RAG skills"}],
            "pattern_detection_status": "parsed",
            "drift_score": 0.42,
        }

    monkeypatch.setattr(runner, "_load_stage_callable", fake_callable)

    runner.execute_review_stage(
        loop_id="loop_a",
        base_state={"domain": "genai", "cycle_id": "cycle_b"},
    )
    result = runner.execute_review_stage(
        loop_id="loop_a",
        base_state={"domain": "genai", "cycle_id": "cycle_b"},
    )

    assert result["stage_id"] == "detect_patterns"
    assert result["next_stage_id"] == "update_skill_graph"
    assert "drift score 0.42" in result["review_packet"]["summary"]
    assert "genai_120hr_curriculum.md" in result["review_packet"]["key_decisions"][0]


def test_loop_review_runner_detect_patterns_fallback_wording(monkeypatch, tmp_path):
    runner = LoopReviewRunner(output_dir=str(tmp_path))

    def fake_callable(loop_id, stage_id):
        if stage_id == "ingest_signals":
            return lambda state: {
                "signal_batch": SignalBatch(
                    batch_id="batch_1",
                    signals=[
                        RawSignal(
                            signal_id="sig_1",
                            channel_category=ChannelCategory.INDUSTRY_MARKET,
                            channel_name="sources",
                            content="RAG and Python remain important.",
                            timestamp="2026-04-16T00:00:00+00:00",
                            signal_type=ChannelType.PROACTIVE,
                            metadata={"filename": "genai_120hr_curriculum.md"},
                        )
                    ],
                    ingested_at="2026-04-16T00:00:00+00:00",
                    source_domain="genai",
                )
            }
        return lambda state: {
            "detected_patterns": [{"pattern_id": "p_raw", "description": "Pattern detection returned non-JSON"}],
            "pattern_detection_status": "fallback_non_json",
            "pattern_detection_note": (
                "Pattern detection response could not be parsed as JSON. "
                "Using a fallback placeholder pattern and default drift score 0.50."
            ),
            "drift_score": 0.5,
        }

    monkeypatch.setattr(runner, "_load_stage_callable", fake_callable)

    runner.execute_review_stage(
        loop_id="loop_a",
        base_state={"domain": "genai", "cycle_id": "cycle_fallback"},
    )
    result = runner.execute_review_stage(
        loop_id="loop_a",
        base_state={"domain": "genai", "cycle_id": "cycle_fallback"},
    )

    assert result["stage_id"] == "detect_patterns"
    assert "Pattern detection parse failed" in result["review_packet"]["summary"]
    assert "fallback placeholder pattern" in result["review_packet"]["key_decisions"][2].lower()


def test_loop_review_runner_generate_curriculum_fallback_wording(monkeypatch, tmp_path):
    runner = LoopReviewRunner(output_dir=str(tmp_path))

    def fake_callable(loop_id, stage_id):
        if stage_id == "load_wiki_context":
            return lambda state: {
                "skill_graph_context": "## Skills in Wiki\n- **Python Programming**",
                "learner_context": "## Learner Segments\n- **Career Switcher**",
                "curriculum_source_context": "### Source: stack curriculum seed",
            }
        if stage_id == "resolve_pedagogy_profile":
            return lambda state: {
                "pedagogy_profile": "project_build_along",
                "pedagogy_rationale": "Project-centered stack.",
            }
        return lambda state: {
            "curriculum_generation_status": "fallback_non_json",
            "curriculum_generation_note": "Curriculum generation response could not be parsed as JSON. Using an empty fallback curriculum draft.",
            "curriculum_generation_raw_response": "This is not valid JSON.",
            "curriculum_map": {
                "curriculum_id": "cur_genai",
                "program_name": "genai Curriculum",
                "domain": "genai",
                "modules": [],
                "total_hours": 0,
            },
        }

    monkeypatch.setattr(runner, "_load_stage_callable", fake_callable)

    runner.execute_review_stage(
        loop_id="loop_b",
        base_state={"domain": "genai", "cycle_id": "cycle_curriculum", "content_type": "concept_explainer"},
    )
    runner.execute_review_stage(
        loop_id="loop_b",
        base_state={"domain": "genai", "cycle_id": "cycle_curriculum", "content_type": "concept_explainer"},
    )
    result = runner.execute_review_stage(
        loop_id="loop_b",
        base_state={"domain": "genai", "cycle_id": "cycle_curriculum", "content_type": "concept_explainer"},
    )

    assert result["stage_id"] == "generate_curriculum"
    assert result["next_stage_id"] == "compare_curriculum_changes"
    assert "Curriculum generation parse failed" in result["review_packet"]["summary"]
    assert "empty fallback curriculum draft" in result["review_packet"]["key_decisions"][0]


def test_load_raw_sources_prefers_manifest_for_genai():
    sources = _load_raw_sources("genai")
    filenames = sorted(source["filename"] for source in sources)

    assert "genai_120hr_curriculum.md" in filenames
    assert "target_persona.md" in filenames
    assert "competitor_courses.md" in filenames


def test_build_bootstrap_warnings_flags_generic_domain_coverage():
    warnings = _build_bootstrap_warnings(
        "genai",
        [
            {
                "filename": "target_persona.md",
                "category": "learner",
                "content": "persona",
                "path": "/tmp/target_persona.md",
            },
            {
                "filename": "ml_engineer_requirements.md",
                "category": "job_postings",
                "content": "requirements",
                "path": "/tmp/ml_engineer_requirements.md",
            },
            {
                "filename": "competitor_courses.md",
                "category": "competitors",
                "content": "competitors",
                "path": "/tmp/competitor_courses.md",
            },
        ],
    )

    assert any("job postings" in warning for warning in warnings)
    assert any("competitors" in warning for warning in warnings)
