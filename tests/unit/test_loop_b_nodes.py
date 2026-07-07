import json

import pytest
import yaml

from open_acp.loops.loop_b import nodes


def test_parse_json_object_response_extracts_embedded_json():
    response = """
    Here is the curriculum draft:

    {
      "curriculum_id": "cur_genai",
      "courses": [],
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
    assert budget["packaging_total_hours"] is None


def test_generate_brief_uses_resolved_inputs_and_reports_fallback(monkeypatch, tmp_path):
    captured: dict = {}

    class FakeClaudeClient:
        def generate(self, prompt, system, model_tier, max_tokens):
            captured["prompt"] = prompt
            return "This is not valid JSON."

    monkeypatch.setattr(nodes, "ClaudeClient", FakeClaudeClient)
    monkeypatch.setattr(nodes, "_find_project_root", lambda: tmp_path)

    result = nodes.generate_brief(
        {
            "domain": "genai",
            "cycle_id": "cycle_brief",
            "pedagogy_profile": "project_build_along",
            "pedagogy_rationale": "Project-centered stack.",
            "skill_graph_context": "## Skills in Wiki\n- **Python Programming**",
            "learner_context": "## Learner Segments\n- **Career Switcher**",
            "skill_outcomes_context": "## Skill Outcomes Digest\n- Digest id: skill_outcomes_genai\n### Pattern Highlights\n- RAG is baseline",
            "market_and_community_context": "## Market And Community Digest\n- Digest id: market_genai\n### Pattern Highlights\n- Competitors emphasize deployment",
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
                "total_hours": 120.0,
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
                "packaging_total_hours": 120.0,
                "target_total_hours": 120.0,
                "slot_budget_hours": 120.0,
                "reserved_hours": 0.0,
                "available_design_hours": 120.0,
                "source_vs_packaging_conflict": False,
                "resolution_reason": "packaging-owned total hours resolved and cross-checked against the source curriculum",
            },
        }
    )

    assert "## Design Priority Profile" in captured["prompt"]
    assert "## Time Budget Context" in captured["prompt"]
    assert "## Skill Outcomes Digest" in captured["prompt"]
    assert "## Market And Community Digest" in captured["prompt"]
    assert "## Canonical Stack Course Abstract" not in captured["prompt"]
    assert "Target total hours: 120.0" in captured["prompt"]
    assert result["brief_generation_status"] == "fallback_non_json"
    assert "deterministic fallback brief" in result["brief_generation_note"]
    assert result["brief_generation_raw_response"] == "This is not valid JSON."
    assert result["brief"]["pedagogy"]["default_profile"] == "project_build_along"
    assert result["brief"]["packaging_profile_ref"] == "niat_b3_genai_packaging"
    assert result["brief"]["stack_name"] == "GenAI Stack Curriculum"
    assert result["brief"]["source_hours_declared"] == 120.0
    assert result["brief"]["source_vs_packaging_conflict"] is False
    artifact_path = tmp_path / "storage" / "design" / "genai" / "cycle_brief" / "brief.yaml"
    assert result["brief_artifact_path"] == str(artifact_path)
    assert artifact_path.exists()
    assert yaml.safe_load(artifact_path.read_text(encoding="utf-8"))["brief_id"] == result["brief"]["brief_id"]


def test_compose_product_specific_curriculum_container_uses_brief_artifact_and_reports_probable_truncation(monkeypatch, tmp_path):
    class FakeClaudeClient:
        def generate(self, prompt, system, model_tier, max_tokens):
            return '{"curriculum_id": "cur_genai", "courses": ['

    monkeypatch.setattr(nodes, "ClaudeClient", FakeClaudeClient)
    monkeypatch.setattr(nodes, "_find_project_root", lambda: tmp_path)

    artifact_dir = tmp_path / "storage" / "design" / "genai" / "cycle_curriculum"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    brief_path = artifact_dir / "brief.yaml"
    brief_path.write_text(
        yaml.safe_dump(
            {
                "brief_id": "brief_genai",
                "stack_name": "GenAI Stack Curriculum",
                "packaging_profile_ref": "genai_stack_packaging",
                "pedagogy": {"default_profile": "project_build_along"},
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    result = nodes.compose_product_specific_curriculum_container(
        {
            "domain": "genai",
            "cycle_id": "cycle_curriculum",
            "design_artifact_paths": {"brief": str(brief_path)},
            "curriculum_source_context": "### Source: stack curriculum seed",
            "skill_outcomes_context": "## Skill Outcomes Digest\n- Digest id: skill_outcomes_genai",
            "market_and_community_context": "## Market And Community Digest\n- Digest id: market_genai",
            "product_context": {"product_label": "NIAT B3", "product_only_courses": [], "course_variant_overrides": {}},
            "packaging_profile": {"packaging_profile_id": "genai_stack_packaging"},
            "time_budget_context": {"target_total_hours": 120.0},
            "content_type": "concept_explainer",
        }
    )

    assert result["curriculum_generation_status"] == "fallback_non_json"
    assert "appears to have been cut off mid-output" in result["curriculum_generation_note"]
    assert result["curriculum_map"]["brief_ref"] == "brief_genai"
    assert result["curriculum_validation_report"]["within_tolerance"] is False
    curriculum_path = tmp_path / "storage" / "design" / "genai" / "cycle_curriculum" / "curriculum.yaml"
    assert result["curriculum_artifact_path"] == str(curriculum_path)
    assert curriculum_path.exists()


def test_compose_product_specific_curriculum_container_raises_on_hours_validation_failure(monkeypatch, tmp_path):
    class FakeClaudeClient:
        def generate(self, prompt, system, model_tier, max_tokens):
            return json.dumps(
                {
                    "curriculum_id": "cur_genai",
                    "brief_ref": "brief_genai",
                    "packaging_profile_ref": "niat_b3_genai_packaging",
                    "stack_name": "GenAI Stack Curriculum",
                    "domain": "genai",
                    "courses": [
                        {
                            "course_id": "c1",
                            "title": "GenAI Foundations",
                            "sequence": 1,
                            "pedagogy_profile": "project_build_along",
                            "objectives": [],
                            "estimated_hours": 40.0,
                            "prerequisite_courses": [],
                            "content_types": ["concept_explainer"],
                        }
                    ],
                    "capstone_project": {},
                    "grand_quiz": {},
                    "total_hours": 120.0,
                }
            )

    monkeypatch.setattr(nodes, "ClaudeClient", FakeClaudeClient)
    monkeypatch.setattr(nodes, "_find_project_root", lambda: tmp_path)

    artifact_dir = tmp_path / "storage" / "design" / "genai" / "cycle_invalid"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    brief_path = artifact_dir / "brief.yaml"
    brief_path.write_text(
        yaml.safe_dump(
            {
                "brief_id": "brief_genai",
                "stack_name": "GenAI Stack Curriculum",
                "packaging_profile_ref": "niat_b3_genai_packaging",
                "pedagogy": {"default_profile": "project_build_along"},
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Curriculum hours validation failed"):
        nodes.compose_product_specific_curriculum_container(
            {
                "domain": "genai",
                "cycle_id": "cycle_invalid",
                "design_artifact_paths": {"brief": str(brief_path)},
                "curriculum_source_context": "### Source: stack curriculum seed",
                "packaging_profile": {
                    "packaging_profile_id": "niat_b3_genai_packaging",
                    "curriculum_hours_tolerance": 0.5,
                },
                "time_budget_context": {"target_total_hours": 120.0},
                "content_type": "concept_explainer",
            }
        )


def test_compose_product_specific_curriculum_container_repairs_hours_validation_once(monkeypatch, tmp_path):
    class FakeClaudeClient:
        def __init__(self):
            self.calls = 0

        def generate(self, prompt, system, model_tier, max_tokens):
            self.calls += 1
            if self.calls == 1:
                return json.dumps(
                    {
                        "curriculum_id": "cur_genai",
                        "brief_ref": "brief_genai",
                        "packaging_profile_ref": "niat_b3_genai_packaging",
                        "stack_name": "GenAI Stack Curriculum",
                        "domain": "genai",
                        "courses": [
                            {
                                "course_id": "c1",
                                "title": "GenAI Foundations",
                                "sequence": 1,
                                "pedagogy_profile": "project_build_along",
                                "objectives": [],
                                "estimated_hours": 120.0,
                                "prerequisite_courses": [],
                                "content_types": ["concept_explainer"],
                            }
                        ],
                        "capstone_project": {
                            "unit_id": "cap_cur_genai",
                            "type": "capstone_project_unit",
                            "estimated_hours": 20.0,
                            "brief": "Capstone",
                            "acceptance_criteria": ["Ship something"],
                        },
                        "grand_quiz": {
                            "unit_id": "gq_cur_genai",
                            "type": "grand_quiz_unit",
                            "estimated_hours": 2.0,
                            "blueprint": [{"course_ref": "c1", "weight": 1.0}],
                        },
                        "total_hours": 120.0,
                    }
                )
            return json.dumps(
                {
                    "curriculum_id": "cur_genai",
                    "brief_ref": "brief_genai",
                    "packaging_profile_ref": "niat_b3_genai_packaging",
                    "stack_name": "GenAI Stack Curriculum",
                    "domain": "genai",
                    "courses": [
                        {
                            "course_id": "c1",
                            "title": "GenAI Foundations",
                            "sequence": 1,
                            "pedagogy_profile": "project_build_along",
                            "objectives": [],
                            "estimated_hours": 98.0,
                            "prerequisite_courses": [],
                            "content_types": ["concept_explainer"],
                        }
                    ],
                    "capstone_project": {
                        "unit_id": "cap_cur_genai",
                        "type": "capstone_project_unit",
                        "estimated_hours": 20.0,
                        "brief": "Capstone",
                        "acceptance_criteria": ["Ship something"],
                    },
                    "grand_quiz": {
                        "unit_id": "gq_cur_genai",
                        "type": "grand_quiz_unit",
                        "estimated_hours": 2.0,
                        "blueprint": [{"course_ref": "c1", "weight": 1.0}],
                    },
                    "total_hours": 120.0,
                }
            )

    monkeypatch.setattr(nodes, "ClaudeClient", FakeClaudeClient)
    monkeypatch.setattr(nodes, "_find_project_root", lambda: tmp_path)

    artifact_dir = tmp_path / "storage" / "design" / "genai" / "cycle_repair"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    brief_path = artifact_dir / "brief.yaml"
    brief_path.write_text(
        yaml.safe_dump(
            {
                "brief_id": "brief_genai",
                "stack_name": "GenAI Stack Curriculum",
                "packaging_profile_ref": "niat_b3_genai_packaging",
                "pedagogy": {"default_profile": "project_build_along"},
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    result = nodes.compose_product_specific_curriculum_container(
        {
            "domain": "genai",
            "cycle_id": "cycle_repair",
            "design_artifact_paths": {"brief": str(brief_path)},
            "curriculum_source_context": "### Source: stack curriculum seed",
            "packaging_profile": {
                "packaging_profile_id": "niat_b3_genai_packaging",
                "curriculum_hours_tolerance": 0.5,
            },
            "time_budget_context": {"target_total_hours": 120.0},
            "content_type": "concept_explainer",
        }
    )

    assert result["curriculum_generation_status"] == "validated_after_repair"
    assert "single structured repair pass" in result["curriculum_generation_note"]
    assert result["curriculum_validation_report"]["within_tolerance"] is True
    assert result["curriculum_map"]["hours_check"] == {
        "courses_sum": 98.0,
        "capstone": 20.0,
        "grand_quiz": 2.0,
    }


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
    assert product_context["product_only_courses"] == []
    assert product_context["course_variant_overrides"] == {}

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


def test_compose_product_specific_curriculum_container_uses_brief_artifact_and_reports_fallback(monkeypatch):
    captured: dict = {}

    class FakeClaudeClient:
        def generate(self, prompt, system, model_tier, max_tokens):
            captured["prompt"] = prompt
            return "This is not valid JSON."

    monkeypatch.setattr(nodes, "ClaudeClient", FakeClaudeClient)

    result = nodes.compose_product_specific_curriculum_container(
        {
            "domain": "genai",
            "brief": {
                "brief_id": "brief_genai_niat_b3",
                "stack_name": "GenAI Stack Curriculum",
                "packaging_profile_ref": "niat_b3_genai_packaging",
                "pedagogy": {"default_profile": "project_build_along"},
            },
            "curriculum_source_context": "### Source: stack curriculum seed",
            "skill_outcomes_context": "## Skill Outcomes Digest\n- Digest id: skill_outcomes_genai",
            "market_and_community_context": "## Market And Community Digest\n- Digest id: market_genai",
            "product_context": {"product_label": "NIAT B3", "product_only_courses": [], "course_variant_overrides": {}},
            "structure_profile": {
                "structure_profile_id": "niat_university_structure",
                "hierarchy": ["batch_curriculum_grid_template", "university", "branch"],
                "design_priority_dimensions": ["regulatory_compliance", "job_placement_outcomes"],
            },
            "packaging_profile": {
                "packaging_profile_id": "niat_b3_genai_packaging",
                "total_hours": 120.0,
                "module_count_per_course": {"default": 3},
                "topic_count_per_module": {"default": 4},
                "allowed_learning_unit_types": ["video_session_unit", "reading_material_unit"],
            },
            "time_budget_context": {"target_total_hours": 120.0},
            "content_type": "concept_explainer",
        }
    )

    assert "## Brief Artifact" in captured["prompt"]
    assert '"brief_id": "brief_genai_niat_b3"' in captured["prompt"]
    assert '"stack_name": "GenAI Stack Curriculum"' in captured["prompt"]
    assert "## Canonical Stack Course Abstract" in captured["prompt"]
    assert "## Product Course Overlay" in captured["prompt"]
    assert "## Skill Outcomes Digest" in captured["prompt"]
    assert "## Market And Community Digest" in captured["prompt"]
    assert "Respect the resolved target total hours" in captured["prompt"]
    assert "do not emit explicit level output" in captured["prompt"]
    assert "Do not decide topic allocation here" in captured["prompt"]
    assert "course_kind" in captured["prompt"]
    assert "course_variant_id" in captured["prompt"]
    assert result["curriculum_generation_status"] == "fallback_non_json"
    assert "empty fallback curriculum draft" in result["curriculum_generation_note"]
    assert result["curriculum_generation_raw_response"] == "This is not valid JSON."
    assert result["curriculum_map"]["brief_ref"] == "brief_genai_niat_b3"
    assert result["curriculum_map"]["packaging_profile_ref"] == "niat_b3_genai_packaging"
    assert result["curriculum_map"]["total_hours"] == 120.0
    assert result["curriculum_map"]["courses"] == []


def test_design_stages_persist_course_module_topic_and_unit_artifacts(monkeypatch, tmp_path):
    monkeypatch.setattr(nodes, "_find_project_root", lambda: tmp_path)

    state = {
        "domain": "genai",
        "cycle_id": "cycle_artifacts",
        "pedagogy_profile": "project_build_along",
        "curriculum_map": {
            "curriculum_id": "cur_genai",
            "brief_ref": "brief_genai",
            "packaging_profile_ref": "genai_stack_packaging",
            "stack_name": "GenAI Stack Curriculum",
            "domain": "genai",
            "courses": [
                {
                    "course_id": "c1",
                    "title": "GenAI Foundations",
                    "sequence": 1,
                    "pedagogy_profile": "project_build_along",
                    "canonical_course_id": "introduction_to_genai",
                    "course_variant_id": None,
                    "course_kind": "stack_course",
                    "objectives": [
                        {
                            "id": "obj_1",
                            "statement": "Build a retrieval-backed GenAI workflow",
                            "bloom_level": "apply",
                            "skill_ids": ["python", "rag"],
                        }
                    ],
                    "estimated_hours": 24,
                    "prerequisite_courses": [],
                    "content_types": ["concept_explainer"],
                    "skill_ids": ["python", "rag"],
                }
            ],
            "capstone_project": {},
            "grand_quiz": {},
            "total_hours": 24,
            "hours_check": {"courses_sum": 24, "capstone": 0, "grand_quiz": 0},
        },
        "packaging_profile": {
            "packaging_profile_id": "genai_stack_packaging",
            "module_count_per_course": {"default": 2, "min": 2, "max": 2, "target_hours_per_module": 12},
            "topic_count_per_module": {"default": 2, "min": 2, "max": 2},
            "learning_units_per_topic": 2,
            "preferred_learning_unit_mix": ["video_session_unit", "coding_practice_unit"],
            "allowed_learning_unit_types": ["video_session_unit", "coding_practice_unit"],
        },
    }

    state.update(nodes.design_courses(state))
    state.update(nodes.design_modules(state))
    state.update(nodes.design_topics(state))
    state.update(nodes.design_learning_units(state))

    artifact_root = tmp_path / "storage" / "design" / "genai" / "cycle_artifacts"
    assert (artifact_root / "courses" / "index.yaml").exists()
    assert (artifact_root / "courses" / "course.c1.yaml").exists()
    assert (artifact_root / "modules" / "index.yaml").exists()
    assert (artifact_root / "topics" / "index.yaml").exists()
    assert (artifact_root / "units" / "index.yaml").exists()


def test_design_and_alignment_pipeline_exposes_external_skill_gaps(monkeypatch, tmp_path):
    monkeypatch.setattr(nodes, "_find_project_root", lambda: tmp_path)
    state = {
        "domain": "genai",
        "cycle_id": "cycle_alignment",
        "content_type": "concept_explainer",
        "pedagogy_profile": "project_build_along",
        "curriculum_map": {
            "curriculum_id": "cur_genai",
            "packaging_profile_ref": "genai_stack_packaging",
            "stack_name": "GenAI Stack Curriculum",
            "domain": "genai",
            "courses": [
                {
                    "course_id": "c1",
                    "title": "Level 1 — GenAI Foundations",
                    "sequence": 1,
                    "pedagogy_profile": "project_build_along",
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
                    "prerequisite_courses": [],
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
    artifact_root = tmp_path / "storage" / "design" / "genai" / "cycle_alignment"
    assert (artifact_root / "practice.yaml").exists()
    assert (artifact_root / "learning_assessments.yaml").exists()
    assert (artifact_root / "skill_assessment_requirements.yaml").exists()
    assert (artifact_root / "assessment_alignment.yaml").exists()
