"""Unit tests for pipeline loader and skill loader."""
import pytest
from pathlib import Path

from open_acp.pipeline_defs.pipeline_loader import (
    PipelineLoader,
    PipelineDefinition,
    StageDefinition,
    _load_yaml,
    _merge_dicts,
)
from open_acp.skills.skill_loader import SkillLoader


# ── Pipeline Loader ────────────────────────────────────────────────────────────

def test_load_base_yaml():
    """_base.yaml should load and contain expected defaults."""
    base_dir = Path(__file__).parent.parent.parent / "src" / "open_acp" / "pipeline_defs"
    data = _load_yaml(base_dir / "_base.yaml")

    assert data["version"] == "1.0"
    assert data["defaults"]["eval_threshold"] == 3.5
    assert data["defaults"]["max_iterations"] == 5
    assert "accuracy" in data["required_dimensions"]
    assert len(data["required_dimensions"]) == 5


def test_merge_dicts_simple():
    base = {"a": 1, "b": 2}
    override = {"b": 3, "c": 4}
    result = _merge_dicts(base, override)
    assert result == {"a": 1, "b": 3, "c": 4}


def test_merge_dicts_nested():
    base = {"defaults": {"threshold": 3.5, "gate": {"type": "G3"}}}
    override = {"defaults": {"threshold": 4.0}}
    result = _merge_dicts(base, override)
    assert result["defaults"]["threshold"] == 4.0
    assert result["defaults"]["gate"]["type"] == "G3"


def test_pipeline_definition_model():
    pd = PipelineDefinition(
        pipeline_id="test_pipeline",
        content_type="concept_explainer",
        display_name="Concept Explainer",
    )
    assert pd.eval_threshold == 3.5
    assert pd.max_iterations == 5
    assert pd.style == "default"
    assert pd.strict_execution is False


def test_stage_definition_model():
    sd = StageDefinition(
        id="outline",
        skill="pipelines/concept_explainer/01_outline",
        tools=["claude_generate"],
        artifact_schema="outline.schema.json",
    )
    assert sd.model_tier == "strong"
    assert sd.checkpoint_required is True
    assert sd.human_approval_default is False


def test_pipeline_loader_list_available():
    """Should return a list of concrete pipeline IDs."""
    loader = PipelineLoader()
    available = loader.list_available()
    assert isinstance(available, list)
    assert "concept_explainer" in available


def test_pipeline_loader_missing_content_type():
    loader = PipelineLoader()
    with pytest.raises(FileNotFoundError):
        loader.load("nonexistent_pipeline")


# ── Skill Loader ───────────────────────────────────────────────────────────────

def test_skill_loader_loads_reviewer():
    loader = SkillLoader()
    content = loader.load("meta/reviewer")
    assert "Self-Review Protocol" in content
    assert "PASS" in content
    assert "REVISE" in content


def test_skill_loader_loads_checkpoint():
    loader = SkillLoader()
    content = loader.load("meta/checkpoint_protocol")
    assert "Checkpoint Protocol" in content
    assert "G1" in content
    assert "G4" in content


def test_skill_loader_exists():
    loader = SkillLoader()
    assert loader.exists("meta/reviewer") is True
    assert loader.exists("meta/nonexistent") is False


def test_skill_loader_missing_skill():
    loader = SkillLoader()
    with pytest.raises(FileNotFoundError):
        loader.load("pipelines/nonexistent/01_outline")


def test_skill_loader_list_pipeline_skills():
    loader = SkillLoader()
    skills = loader.list_pipeline_skills("concept_explainer")
    assert isinstance(skills, list)
    assert "01_outline" in skills


def test_concept_explainer_v1_stage_order_and_strict_execution():
    loader = PipelineLoader()
    pipeline = loader.load("concept_explainer")

    assert pipeline.strict_execution is True
    assert [stage.id for stage in pipeline.stages] == [
        "objectives",
        "outline",
        "core_content",
        "activities",
        "brand_polish",
        "slide_deck",
    ]
    assert pipeline.stages[1].artifact_schema == "concept_outline.schema.json"


def test_project_building_v1_stage_order_and_project_brief():
    loader = PipelineLoader()
    pipeline = loader.load("project_building")

    assert pipeline.strict_execution is True
    assert [stage.id for stage in pipeline.stages] == [
        "project_brief",
        "objectives",
        "outline",
        "core_content",
        "activities",
        "brand_polish",
        "slide_deck",
    ]
    assert pipeline.stages[0].artifact_schema == "project_brief.schema.json"
