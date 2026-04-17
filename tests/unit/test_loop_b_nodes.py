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


def test_resolve_design_priority_profile_uses_structure_dimensions():
    result = nodes.resolve_design_priority_profile(
        {
            "structure_profile": {
                "structure_profile_id": "niat_university_structure",
                "design_priority_dimensions": [
                    "regulatory_compliance",
                    "university_policy_and_infra_constraints",
                    "job_placement_outcomes",
                ],
            },
            "product_context": {"focus_priority": "active"},
        }
    )

    profile = result["design_priority_profile"]
    assert profile["profile_id"] == "niat_university_structure_design_priorities"
    assert profile["dimension_ids"] == [
        "regulatory_compliance",
        "university_policy_and_infra_constraints",
        "job_placement_outcomes",
    ]
    assert profile["focus_priority"] == "active"


def test_resolve_time_budget_context_prefers_source_total_hours():
    result = nodes.resolve_time_budget_context(
        {
            "domain": "genai",
            "curriculum_source_context": "# GenAI 120 Hr Curriculum\nThis path is 120 hours long.",
            "packaging_profile": {},
        }
    )

    budget = result["time_budget_context"]
    assert budget["source_total_hours"] == 120.0
    assert budget["target_total_hours"] == 120.0
    assert budget["available_design_hours"] == 120.0


def test_generate_brief_uses_resolved_inputs_and_reports_fallback(monkeypatch):
    captured: dict = {}

    class FakeClaudeClient:
        def generate(self, prompt, system, model_tier, max_tokens):
            captured["prompt"] = prompt
            return "This is not valid JSON."

    monkeypatch.setattr(nodes, "ClaudeClient", FakeClaudeClient)

    result = nodes.generate_brief(
        {
            "domain": "genai",
            "pedagogy_profile": "project_build_along",
            "pedagogy_rationale": "Project-centered stack.",
            "skill_graph_context": "## Skills in Wiki\n- **Python Programming**",
            "learner_context": "## Learner Segments\n- **Career Switcher**",
            "curriculum_source_context": "### Source: stack curriculum seed",
            "product_context": {
                "product_label": "NIAT B3",
                "product_category": "degree_program_product",
                "curriculum_container_kind": "academic_degree_curriculum",
                "delivery_mode": "mixed_partner_delivery",
                "focus_priority": "active",
            },
            "structure_profile": {
                "structure_profile_id": "niat_university_structure",
                "hierarchy": ["batch_curriculum_grid_template", "university", "branch"],
                "design_priority_dimensions": ["regulatory_compliance", "job_placement_outcomes"],
            },
            "packaging_profile": {
                "packaging_profile_id": "niat_b3_genai_packaging",
                "module_count_per_course": {"default": 3},
                "topic_count_per_module": {"default": 4},
                "allowed_learning_unit_types": ["video_session_unit", "reading_material_unit"],
            },
            "design_priority_profile": {
                "profile_id": "niat_university_structure_design_priorities",
                "ordered_dimensions": ["regulatory_compliance", "job_placement_outcomes"],
                "dimension_ids": ["regulatory_compliance", "job_placement_outcomes"],
                "focus_priority": "active",
                "resolution_reason": "structure-driven",
            },
            "time_budget_context": {
                "context_id": "time_budget_genai",
                "source_total_hours": 120.0,
                "target_total_hours": 120.0,
                "slot_budget_hours": 120.0,
                "reserved_hours": 0.0,
                "available_design_hours": 120.0,
                "resolution_reason": "source-defined total hours preserved",
            },
        }
    )

    assert "## Design Priority Profile" in captured["prompt"]
    assert "## Time Budget Context" in captured["prompt"]
    assert "Target total hours: 120.0" in captured["prompt"]
    assert result["brief_generation_status"] == "fallback_non_json"
    assert "deterministic fallback brief" in result["brief_generation_note"]
    assert result["brief_generation_raw_response"] == "This is not valid JSON."
    assert result["brief"]["pedagogy"]["default_profile"] == "project_build_along"
    assert result["brief"]["total_hours"] == 120.0


def test_generate_curriculum_reports_probable_truncation(monkeypatch):
    class FakeClaudeClient:
        def generate(self, prompt, system, model_tier, max_tokens):
            return '{"curriculum_id": "cur_genai", "modules": ['

    monkeypatch.setattr(nodes, "ClaudeClient", FakeClaudeClient)

    result = nodes.generate_curriculum(
        {
            "domain": "genai",
            "brief": {
                "brief_id": "brief_genai",
                "program_name": "GenAI 120 Hr Curriculum",
                "pedagogy": {"default_profile": "project_build_along", "rationale": "Project-centered stack."},
                "total_hours": 120.0,
            },
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


def test_resolve_packaging_profile_uses_domain_override_without_product():
    result = nodes.resolve_packaging_profile({"domain": "genai", "content_type": "concept_explainer"})

    profile = result["packaging_profile"]

    assert profile["packaging_profile_id"] == "genai_stack_packaging"
    assert profile["module_count_per_course"]["default"] == 3
    assert "coding_practice_unit" in profile["preferred_learning_unit_mix"]
    assert profile["field_provenance"]["module_count_per_course.default"] == "stack_fallback:genai"


def test_resolve_packaging_profile_prefers_product_layers_and_records_provenance():
    product_state = nodes.resolve_product_context(
        {
            "domain": "genai",
            "product_family": "NIAT",
            "product_version": "B3",
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

    assert profile["packaging_profile_id"] == "niat_b3_genai_packaging"
    assert profile["module_count_per_course"]["default"] == 3
    assert profile["topic_count_per_module"]["default"] == 4
    assert "coding_practice_unit" in profile["allowed_learning_unit_types"]
    assert profile["field_provenance"]["module_count_per_course.default"] == "product_version_domain:NIAT:B3:genai"
    assert profile["field_provenance"]["topic_count_per_module.default"] == "product_version_domain:NIAT:B3:genai"
    assert profile["field_provenance"]["allowed_learning_unit_types"] == "product_default:NIAT"
    assert profile["field_provenance"]["preferred_learning_unit_mix"] == "product_domain:NIAT:genai"
    assert "product_default:NIAT B3" in profile["resolution_layers"]
    assert "product_version_domain:NIAT B3:genai" in profile["resolution_layers"]


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


def test_resolve_packaging_profile_refreshes_stale_product_context():
    result = nodes.resolve_packaging_profile(
        {
            "domain": "genai",
            "content_type": "concept_explainer",
            "product_family": "NIAT",
            "product_version": "B3",
            "product_context": {
                "product_family": "NIAT",
                "product_version": "B3",
                "product_label": "NIAT B3",
                "feature_flags": {"recorded_videos_included": True},
            },
        }
    )

    profile = result["packaging_profile"]
    refreshed_context = result["product_context"]
    assert refreshed_context["packaging_layers"]["product_version_domain"]["packaging_profile_id"] == "niat_b3_genai_packaging"
    assert profile["packaging_profile_id"] == "niat_b3_genai_packaging"


def test_resolve_pedagogy_profile_prefers_product_layers_and_records_source():
    product_state = nodes.resolve_product_context(
        {
            "domain": "genai",
            "product_family": "NIAT",
            "product_version": "B3",
            "content_type": "concept_explainer",
        }
    )

    result = nodes.resolve_pedagogy_profile(
        {
            "domain": "genai",
            "content_type": "concept_explainer",
            "product_context": product_state["product_context"],
        }
    )

    assert result["pedagogy_profile"] == "project_build_along"
    assert result["pedagogy_source"] == "product_version_domain:NIAT:B3:genai"
    assert "NIAT B3 GenAI" in result["pedagogy_rationale"]


def test_resolve_pedagogy_profile_refreshes_stale_product_context():
    result = nodes.resolve_pedagogy_profile(
        {
            "domain": "genai",
            "content_type": "concept_explainer",
            "product_family": "NIAT",
            "product_version": "B3",
            "product_context": {
                "product_family": "NIAT",
                "product_version": "B3",
                "product_label": "NIAT B3",
            },
        }
    )

    assert result["pedagogy_profile"] == "project_build_along"
    assert result["pedagogy_source"] == "product_version_domain:NIAT:B3:genai"


def test_generate_curriculum_uses_brief_artifact_and_reports_fallback(monkeypatch):
    captured: dict = {}

    class FakeClaudeClient:
        def generate(self, prompt, system, model_tier, max_tokens):
            captured["prompt"] = prompt
            return "This is not valid JSON."

    monkeypatch.setattr(nodes, "ClaudeClient", FakeClaudeClient)

    result = nodes.generate_curriculum(
        {
            "domain": "genai",
            "brief": {
                "brief_id": "brief_genai_niat_b3",
                "program_name": "GenAI 120 Hr Curriculum",
                "pedagogy": {
                    "default_profile": "project_build_along",
                    "rationale": "NIAT B3 GenAI needs milestone-based implementation practice.",
                },
                "total_hours": 120.0,
            },
            "curriculum_source_context": "### Source: stack curriculum seed",
            "structure_profile": {
                "structure_profile_id": "niat_university_structure",
                "hierarchy": ["batch_curriculum_grid_template", "university", "branch"],
                "design_priority_dimensions": ["regulatory_compliance", "job_placement_outcomes"],
            },
            "packaging_profile": {
                "packaging_profile_id": "niat_b3_genai_packaging",
                "module_count_per_course": {"default": 3},
                "topic_count_per_module": {"default": 4},
                "allowed_learning_unit_types": ["video_session_unit", "reading_material_unit"],
            },
            "content_type": "concept_explainer",
        }
    )

    assert "## Brief Artifact" in captured["prompt"]
    assert '"brief_id": "brief_genai_niat_b3"' in captured["prompt"]
    assert "Respect the total hours from the brief" in captured["prompt"]
    assert "do not emit explicit level output" in captured["prompt"]
    assert "Do not decide topic allocation here" in captured["prompt"]
    assert result["curriculum_generation_status"] == "fallback_non_json"
    assert "empty fallback curriculum draft" in result["curriculum_generation_note"]
    assert result["curriculum_generation_raw_response"] == "This is not valid JSON."
    assert result["curriculum_map"]["brief_ref"] == "brief_genai_niat_b3"
    assert result["curriculum_map"]["total_hours"] == 120.0


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
