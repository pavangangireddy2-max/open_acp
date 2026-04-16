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
