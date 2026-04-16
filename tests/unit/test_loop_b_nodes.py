import pytest

from open_acp.loops.loop_b import nodes


def test_parse_json_object_response_extracts_embedded_json():
    response = """
    Here is the curriculum draft:

    {
      "curriculum_id": "cur_genai",
      "modules": [],
      "total_hours": 120
    }

    Let me know if you want revisions.
    """

    parsed = nodes._parse_json_object_response(response)

    assert parsed["curriculum_id"] == "cur_genai"
    assert parsed["total_hours"] == 120


def test_generate_curriculum_uses_curriculum_source_context_and_reports_fallback(monkeypatch):
    captured: dict = {}

    class FakeClaudeClient:
        def generate(self, prompt, system, model_tier, max_tokens):
            captured["prompt"] = prompt
            return "This is not valid JSON."

    monkeypatch.setattr(nodes, "ClaudeClient", FakeClaudeClient)

    result = nodes.generate_curriculum(
        {
            "domain": "genai",
            "pedagogy_profile": "project_build_along",
            "pedagogy_rationale": "Project-centered stack.",
            "skill_graph_context": "## Skills in Wiki\n- **Python Programming**",
            "learner_context": "## Learner Segments\n- **Career Switcher**",
            "curriculum_source_context": "### Source: stack curriculum seed",
            "content_type": "concept_explainer",
        }
    )

    assert "## Curriculum Source Context" in captured["prompt"]
    assert "### Source: stack curriculum seed" in captured["prompt"]
    assert "Limit to 2-3 concise objectives per module." in captured["prompt"]
    assert "Use stable snake_case wiki skill IDs" in captured["prompt"]
    assert result["curriculum_generation_status"] == "fallback_non_json"
    assert "empty fallback curriculum draft" in result["curriculum_generation_note"]
    assert result["curriculum_generation_raw_response"] == "This is not valid JSON."
    assert result["curriculum_map"]["modules"] == []


def test_generate_curriculum_reports_probable_truncation(monkeypatch):
    class FakeClaudeClient:
        def generate(self, prompt, system, model_tier, max_tokens):
            return '{"curriculum_id": "cur_genai", "modules": ['

    monkeypatch.setattr(nodes, "ClaudeClient", FakeClaudeClient)

    result = nodes.generate_curriculum(
        {
            "domain": "genai",
            "pedagogy_profile": "project_build_along",
            "pedagogy_rationale": "Project-centered stack.",
            "skill_graph_context": "",
            "learner_context": "",
            "curriculum_source_context": "### Source: stack curriculum seed",
            "content_type": "concept_explainer",
        }
    )

    assert result["curriculum_generation_status"] == "fallback_non_json"
    assert "appears to have been cut off mid-output" in result["curriculum_generation_note"]


def test_resolve_product_and_structure_profile_from_manifest():
    product_state = nodes.resolve_product_context(
        {
            "domain": "genai",
            "product_family": "NIAT",
            "product_version": "B3",
        }
    )

    product_context = product_state["product_context"]
    assert product_context["product_family"] == "NIAT"
    assert product_context["product_version"] == "B3"
    assert product_context["structure_profile_id"] == "niat_university_structure"

    structure_state = nodes.resolve_structure_profile(product_state)
    structure_profile = structure_state["structure_profile"]
    assert structure_profile["structure_profile_id"] == "niat_university_structure"
    assert "batch_curriculum_grid_template" in structure_profile["hierarchy"]


def test_resolve_product_context_requires_explicit_product_when_configured():
    with pytest.raises(ValueError, match="Explicit product context is required"):
        nodes.resolve_product_context({"domain": "genai", "require_product_context": True})


def test_resolve_packaging_profile_uses_domain_override():
    result = nodes.resolve_packaging_profile({"domain": "genai", "content_type": "concept_explainer"})

    profile = result["packaging_profile"]

    assert profile["packaging_profile_id"] == "genai_stack_packaging"
    assert profile["module_count_per_course"]["default"] == 3
    assert "coding_practice_unit" in profile["preferred_learning_unit_mix"]


def test_resolve_packaging_profile_carries_product_feature_flags():
    product_state = nodes.resolve_product_context(
        {
            "domain": "genai",
            "product_family": "Academy",
            "product_version": "1.5",
        }
    )

    result = nodes.resolve_packaging_profile(
        {
            "domain": "genai",
            "content_type": "concept_explainer",
            "product_context": product_state["product_context"],
        }
    )

    profile = result["packaging_profile"]
    assert profile["product_feature_flags"]["recorded_videos_included"] is True
    assert profile["product_feature_flags"]["live_sessions_included"] is True


def test_design_and_alignment_pipeline_exposes_external_skill_gaps():
    state = {
        "domain": "genai",
        "content_type": "concept_explainer",
        "pedagogy_profile": "project_build_along",
        "curriculum_map": {
            "curriculum_id": "cur_genai",
            "program_name": "GenAI Stack Curriculum",
            "domain": "genai",
            "modules": [
                {
                    "module_id": "l1",
                    "title": "Level 1 — GenAI Foundations",
                    "sequence": 1,
                    "objectives": [
                        {
                            "id": "obj_1",
                            "statement": "Explain the role of retrieval in GenAI systems",
                            "bloom_level": "understand",
                            "skill_ids": ["python", "rag"],
                        },
                        {
                            "id": "obj_2",
                            "statement": "Build a minimal retrieval workflow",
                            "bloom_level": "apply",
                            "skill_ids": ["rag", "vector_databases"],
                        },
                    ],
                    "estimated_hours": 24,
                    "prerequisite_modules": [],
                    "content_types": ["concept_explainer", "project_building"],
                }
            ],
            "total_hours": 24,
        },
        "detected_patterns": [
            {"description": "RAG and retrieval evaluation remain central in industry hiring."}
        ],
    }

    state.update(nodes.resolve_packaging_profile(state))
    state.update(nodes.design_courses(state))
    state.update(nodes.design_modules(state))
    state.update(nodes.design_topics(state))
    state.update(nodes.design_learning_units(state))
    state.update(nodes.design_practice(state))
    state.update(nodes.design_learning_assessments(state))
    state.update(nodes.resolve_skill_assessment_requirements(state))
    state.update(nodes.align_learning_with_skill_assessments(state))

    assert state["course_design"]["course_count"] == 1
    assert state["module_design"]["total_module_count"] >= 2
    assert state["topic_design"]["total_topic_count"] >= state["module_design"]["total_module_count"]
    assert state["learning_unit_plan"]["total_learning_unit_count"] >= state["topic_design"]["total_topic_count"]
    assert state["practice_design"]["practice_touchpoint_count"] == state["topic_design"]["total_topic_count"]
    assert state["learning_assessment_plan"]["classroom_quizzes"]
    assert state["skill_assessment_requirements"]["signal_sync_status"] == "shared_loop_a_patterns"
    assert state["assessment_alignment_report"]["question_type_alignment"]["status"] == "gap"
    assert "project" in state["assessment_alignment_report"]["question_type_alignment"]["missing"]
