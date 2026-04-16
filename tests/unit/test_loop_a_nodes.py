import pytest
from pathlib import Path

from open_acp.loops.loop_a import nodes
from open_acp.models.signals import ChannelCategory, ChannelType, RawSignal, SignalBatch


def _build_signal_batch() -> SignalBatch:
    return SignalBatch(
        batch_id="batch_1",
        signals=[
            RawSignal(
                signal_id="sig_1",
                channel_category=ChannelCategory.INDUSTRY_MARKET,
                channel_name="sources",
                content="Python foundations for AI and RAG systems.",
                timestamp="2026-04-16T00:00:00+00:00",
                signal_type=ChannelType.PROACTIVE,
                metadata={"filename": "genai_120hr_curriculum.md"},
            ),
            RawSignal(
                signal_id="sig_2",
                channel_category=ChannelCategory.INTERVIEW_INTEL,
                channel_name="job_postings",
                content="Python (98%), RAG, vector DBs, prompt engineering.",
                timestamp="2026-04-16T00:00:00+00:00",
                signal_type=ChannelType.PROACTIVE,
                metadata={"filename": "ml_engineer_requirements.md"},
            ),
        ],
        ingested_at="2026-04-16T00:00:00+00:00",
        source_domain="genai",
    )


def test_update_skill_graph_uses_detected_patterns_and_existing_skill_ids(monkeypatch):
    captured: dict = {}

    class FakeClaudeClient:
        def generate(self, prompt, system, model_tier, max_tokens):
            captured["prompt"] = prompt
            return """
            [
              {
                "skill_id": "python",
                "name": "Python Programming",
                "demand_score": 0.98,
                "durability": "durable",
                "description": "Core language for AI development.",
                "prerequisites": ["programming_basics"],
                "related_skills": ["pytorch"]
              }
            ]
            """

    class FakeWiki:
        def list_entities(self, entity_type=None):
            if entity_type == "skill":
                return [{"entity_id": "python", "title": "Python Programming"}]
            return []

        def get_entity(self, entity_type, entity_id):
            return None

        def create_entity(self, **kwargs):
            captured["create_kwargs"] = kwargs
            return "storage/wiki/entities/skill_python.md"

        def update_entity(self, **kwargs):
            captured["update_kwargs"] = kwargs
            return True

        def get_stack_profile(self, stack_id, entity_type, entity_id):
            return None

        def write_stack_profile(self, **kwargs):
            captured["stack_profile_kwargs"] = kwargs
            return "storage/wiki/stack_profiles/genai/skill_python.md"

    monkeypatch.setattr(nodes, "ClaudeClient", FakeClaudeClient)
    monkeypatch.setattr(nodes, "WikiEngine", lambda: FakeWiki())

    result = nodes.update_skill_graph(
        {
            "domain": "genai",
            "signal_batch": _build_signal_batch(),
            "detected_patterns": [
                {
                    "pattern_id": "p1",
                    "description": "Skill ontology duplication should be consolidated.",
                    "evidence": "Duplicate RAG and fine-tuning nodes appeared across prior runs.",
                    "affected_areas": ["skill_graph"],
                    "confidence": 0.84,
                    "is_new": True,
                }
            ],
        }
    )

    assert result["wiki_entries_created"] == ["skill_python"]
    assert "Detected Patterns To Honor" in captured["prompt"]
    assert "Skill ontology duplication should be consolidated." in captured["prompt"]
    assert "Existing Canonical Skill IDs" in captured["prompt"]
    assert "python: Python Programming" in captured["prompt"]
    assert captured["create_kwargs"]["sources"] == [
        "genai_120hr_curriculum.md",
        "ml_engineer_requirements.md",
    ]
    assert result["stack_profiles_created"] == ["genai/skill_python"]
    assert captured["stack_profile_kwargs"]["stack_id"] == "genai"
    assert captured["stack_profile_kwargs"]["entity_id"] == "python"
    assert captured["stack_profile_kwargs"]["role_in_stack"] == "foundational"


def test_update_product_context_creates_runtime_product_summary(monkeypatch):
    captured: dict = {}

    class FakeWiki:
        def get_entity(self, entity_type, entity_id):
            return None

        def create_entity(self, **kwargs):
            captured["create_kwargs"] = kwargs
            return "storage/wiki/entities/product_niat_b3.md"

    monkeypatch.setattr(nodes, "WikiEngine", lambda: FakeWiki())

    result = nodes.update_product_context(
        {
            "domain": "genai",
            "product_family": "NIAT",
            "product_version": "B3",
            "detected_patterns": [
                {
                    "description": "Industry-facing GenAI delivery needs project-heavy progression.",
                    "affected_areas": ["skill_graph", "learner_model"],
                }
            ],
        }
    )

    assert result["product_context"]["product_family"] == "NIAT"
    assert result["product_context"]["product_version"] == "B3"
    assert result["structure_profile"]["structure_profile_id"] == "niat_university_structure"
    assert result["wiki_entries_created"] == ["product_niat_b3"]
    assert captured["create_kwargs"]["entity_type"] == "product"
    assert captured["create_kwargs"]["title"] == "NIAT B3 Context"
    assert "Structure profile: niat_university_structure" in captured["create_kwargs"]["content"]


def test_ingest_signals_requires_manifest_backed_inputs_when_strict():
    with pytest.raises(ValueError, match="No stack manifest was found"):
        nodes.ingest_signals(
            {
                "domain": "missing_domain_for_test",
                "cycle_id": "cycle_strict",
                "strict_domain_inputs": True,
            }
        )


def test_update_product_context_requires_explicit_product_when_configured():
    with pytest.raises(ValueError, match="Explicit product context is required"):
        nodes.update_product_context(
            {
                "domain": "genai",
                "require_product_context": True,
            }
        )


def test_update_learner_model_requires_product_specific_inputs_for_explicit_product_run():
    with pytest.raises(ValueError, match="missing product-specific target-audience inputs"):
        nodes.update_learner_model(
            {
                "domain": "genai",
                "product_family": "NIAT",
                "product_version": "B3",
                "signal_batch": _build_signal_batch(),
            }
        )


def test_infer_category_treats_target_audience_paths_as_learner():
    path = Path("knowledge/sources/products/niat/target_audience/niat_target_audience_profile.md")

    assert nodes._infer_category(path) == "learner"


def test_signal_counts_as_learner_for_target_audience_source_path():
    signal = RawSignal(
        signal_id="sig_target_audience",
        channel_category=ChannelCategory.INDUSTRY_MARKET,
        channel_name="sources",
        content="NIAT target audience profile content",
        timestamp="2026-04-16T00:00:00+00:00",
        signal_type=ChannelType.PROACTIVE,
        metadata={
            "filename": "niat_target_audience_profile.md",
            "source_path": "knowledge/sources/products/niat/target_audience/niat_target_audience_profile.md",
        },
    )

    assert nodes._signal_counts_as_learner(signal) is True
