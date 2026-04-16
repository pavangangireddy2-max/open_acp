"""Unit tests for the wiki engine."""
import tempfile
from pathlib import Path
import pytest

from open_acp.knowledge.wiki_engine import WikiEngine


@pytest.fixture
def wiki():
    """Create a WikiEngine with a temp directory."""
    tmpdir = tempfile.mkdtemp()
    return WikiEngine(wiki_dir=tmpdir)


def test_create_entity(wiki):
    path = wiki.create_entity("skill", "python", "Python", "A programming language", confidence=0.9, durability="durable")
    assert "skill_python.md" in path


def test_get_entity(wiki):
    wiki.create_entity("skill", "python", "Python", "A programming language", confidence=0.9)
    entity = wiki.get_entity("skill", "python")
    assert entity is not None
    assert entity["frontmatter"]["title"] == "Python"
    assert entity["frontmatter"]["confidence"] == 0.9


def test_get_entity_not_found(wiki):
    assert wiki.get_entity("skill", "nonexistent") is None


def test_update_entity(wiki):
    wiki.create_entity("skill", "python", "Python", "A programming language", confidence=0.7)
    updated = wiki.update_entity("python", "skill", "Now with ML focus", "Updated for 2026", new_confidence=0.9)
    assert updated is True
    entity = wiki.get_entity("skill", "python")
    assert entity["frontmatter"]["confidence"] == 0.9
    assert "ML focus" in entity["content"]


def test_update_nonexistent_entity(wiki):
    assert wiki.update_entity("nope", "skill", "delta", "reason") is False


def test_supersede(wiki):
    wiki.create_entity("competitor", "old_co", "Old Company", "Was good", confidence=0.8)
    wiki.create_entity("competitor", "new_co", "New Company", "Is better", confidence=0.9)
    result = wiki.supersede("old_co", "competitor", "new_co", "competitor", "Acquired")
    assert result is True
    old = wiki.get_entity("competitor", "old_co")
    assert old["frontmatter"]["confidence"] == 0.0
    assert "SUPERSEDED" in old["content"]


def test_list_entities(wiki):
    wiki.create_entity("skill", "python", "Python", "Language")
    wiki.create_entity("skill", "pytorch", "PyTorch", "Framework")
    wiki.create_entity("competitor", "acme", "Acme", "Competitor")

    all_entities = wiki.list_entities()
    assert len(all_entities) == 3

    skills_only = wiki.list_entities(entity_type="skill")
    assert len(skills_only) == 2


def test_search(wiki):
    wiki.create_entity("skill", "python", "Python Programming", "Python is a versatile programming language for ML")
    wiki.create_entity("skill", "rust", "Rust", "Systems programming language")

    results = wiki.search("python programming")
    assert len(results) >= 1
    assert results[0]["entity_id"] == "python"


def test_search_by_type(wiki):
    wiki.create_entity("skill", "python", "Python", "Language")
    wiki.create_entity("competitor", "acme", "Acme Python Course", "Teaches Python")

    results = wiki.search("python", entity_type="skill")
    assert all(r["entity_type"] == "skill" for r in results)


def test_rebuild_index(wiki):
    wiki.create_entity("skill", "python", "Python", "Language", confidence=0.9)
    wiki.create_entity("skill", "rust", "Rust", "Language", confidence=0.6)

    index = wiki.rebuild_index()
    assert "Python" in index
    assert "Rust" in index
    assert "Total entities: 2" in index


def test_get_log(wiki):
    wiki.create_entity("skill", "python", "Python", "Language")
    log = wiki.get_log()
    assert "create" in log
    assert "python" in log


def test_lint_low_confidence(wiki):
    wiki.create_entity("skill", "obscure", "Obscure Skill", "Very niche", confidence=0.1)
    issues = wiki.lint()
    low_conf = [i for i in issues if i["type"] == "low_confidence"]
    assert len(low_conf) == 1


def test_lint_clean(wiki):
    wiki.create_entity("skill", "python", "Python", "Language", confidence=0.9)
    issues = wiki.lint()
    # Only orphan warning (acceptable with single entity)
    errors = [i for i in issues if i["severity"] == "error"]
    assert len(errors) == 0


def test_crystallize(wiki):
    path = wiki.crystallize("cycle_1", {
        "health_scores": ["module_1: 4.2/5"],
        "insights": ["Students need more practice exercises"],
        "lessons_learned": ["Shorter sections improve engagement"],
    })
    assert "cycle_cycle_1.md" in path
    log = wiki.get_log()
    assert "crystallize" in log


def test_invalid_entity_type(wiki):
    with pytest.raises(ValueError):
        wiki.create_entity("invalid_type", "test", "Test", "Content")


def test_cross_references(wiki):
    wiki.create_entity("skill", "python", "Python", "Language",
                       cross_references=["skill_ml", "skill_data_science"])
    entity = wiki.get_entity("skill", "python")
    refs = entity["frontmatter"].get("cross_references", [])
    assert "skill_ml" in refs


def test_sources_accumulate_on_update(wiki):
    wiki.create_entity("skill", "python", "Python", "Language", sources=["source_1"])
    wiki.update_entity("python", "skill", "More info", "New data", new_sources=["source_2"])
    entity = wiki.get_entity("skill", "python")
    sources = entity["frontmatter"].get("sources", [])
    assert "source_1" in sources
    assert "source_2" in sources


def test_default_wiki_dir_uses_runtime_storage():
    wiki = WikiEngine()
    assert str(wiki.wiki_dir).endswith(str(Path("storage") / "wiki"))


def test_write_and_get_stack_profile(wiki):
    path = wiki.write_stack_profile(
        stack_id="genai",
        entity_type="skill",
        entity_id="python",
        title="Python Programming (genai)",
        summary="Python is foundational for GenAI workflows.",
        relevance_score=0.95,
        role_in_stack="foundational",
        prerequisite_skills=["programming_basics"],
        downstream_skills=["rag", "pytorch"],
        pedagogy_notes=["Teach early and revisit through build checkpoints."],
        assessment_implications=["Assess before project usage."],
        sources=["genai_120hr_curriculum.md"],
    )

    assert "stack_profiles/genai/skill_python.md" in path

    profile = wiki.get_stack_profile("genai", "skill", "python")
    assert profile is not None
    assert profile["frontmatter"]["stack_id"] == "genai"
    assert profile["frontmatter"]["relevance_score"] == 0.95
    assert profile["frontmatter"]["role_in_stack"] == "foundational"
    assert "Python is foundational" in profile["content"]


def test_list_stack_profiles(wiki):
    wiki.write_stack_profile(
        stack_id="genai",
        entity_type="skill",
        entity_id="python",
        title="Python Programming (genai)",
        summary="Foundational skill for GenAI.",
        relevance_score=0.95,
        role_in_stack="foundational",
    )
    wiki.write_stack_profile(
        stack_id="dsa",
        entity_type="skill",
        entity_id="python",
        title="Python Programming (dsa)",
        summary="Implementation language for DSA.",
        relevance_score=0.7,
        role_in_stack="core",
    )

    profiles = wiki.list_stack_profiles()
    assert len(profiles) == 2

    genai_profiles = wiki.list_stack_profiles(stack_id="genai", entity_type="skill")
    assert len(genai_profiles) == 1
    assert genai_profiles[0]["canonical_entity_id"] == "python"


def test_rebuild_index_includes_stack_profiles(wiki):
    wiki.create_entity("skill", "python", "Python", "Language", confidence=0.9)
    wiki.write_stack_profile(
        stack_id="genai",
        entity_type="skill",
        entity_id="python",
        title="Python Programming (genai)",
        summary="Foundational skill for GenAI.",
        relevance_score=0.95,
        role_in_stack="foundational",
    )

    index = wiki.rebuild_index()
    assert "Total stack profiles: 1" in index
    assert "Stack Profiles" in index
    assert "Python Programming (genai)" in index
