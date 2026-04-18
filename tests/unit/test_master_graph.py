from open_acp.orchestrator.master_graph import _build_loop_c_execution_context


def test_build_loop_c_execution_context_prefers_module_work_plan():
    loop_b_result = {
        "pedagogy_profile": "project_build_along",
        "curriculum_map": {
            "curriculum_id": "cur_genai",
            "stack_name": "GenAI Stack Curriculum",
            "courses": [
                {
                    "course_id": "seed_l1",
                    "title": "Level 1 — Foundations",
                    "estimated_hours": 12,
                    "objectives": [{"id": "obj_1", "statement": "Understand framing", "skill_ids": ["python"]}],
                    "prerequisite_courses": [],
                }
            ],
        },
        "course_design": {
            "courses": [
                {
                    "course_id": "course_seed_l1",
                    "source_course_id": "seed_l1",
                    "title": "Level 1 — Foundations",
                    "sequence": 1,
                }
            ]
        },
        "module_design": {
            "modules": [
                {
                    "module_id": "course_seed_l1_m1",
                    "course_id": "course_seed_l1",
                    "title": "Level 1 — Foundations — Core workflow",
                    "sequence_within_course": 1,
                }
            ]
        },
        "topic_design": {
            "topics": [
                {
                    "topic_id": "course_seed_l1_m1_t1",
                    "module_id": "course_seed_l1_m1",
                    "course_id": "course_seed_l1",
                    "title": "Level 1 — Problem Framing",
                    "sequence_within_module": 1,
                    "estimated_minutes": 30,
                }
            ]
        },
        "learning_unit_plan": {
            "learning_units": [
                {
                    "learning_unit_id": "course_seed_l1_m1_t1_u1",
                    "topic_id": "course_seed_l1_m1_t1",
                    "module_id": "course_seed_l1_m1",
                    "course_id": "course_seed_l1",
                    "title": "Level 1 — Problem Framing — Reading material",
                    "unit_type": "reading_material_unit",
                    "estimated_minutes": 10,
                    "delivery_intent": "learn",
                },
                {
                    "learning_unit_id": "course_seed_l1_m1_t1_u2",
                    "topic_id": "course_seed_l1_m1_t1",
                    "module_id": "course_seed_l1_m1",
                    "course_id": "course_seed_l1",
                    "title": "Level 1 — Problem Framing — Instructor-led PPT session",
                    "unit_type": "video_session_unit",
                    "estimated_minutes": 20,
                    "delivery_intent": "learn",
                },
            ]
        },
        "practice_design": {
            "items": [
                {
                    "topic_id": "course_seed_l1_m1_t1",
                    "practice_type": "guided_reflection",
                }
            ]
        },
        "learning_assessment_plan": {
            "classroom_quizzes": [
                {
                    "topic_id": "course_seed_l1_m1_t1",
                    "question_types": ["mcq", "fib"],
                }
            ],
            "module_quizzes": [
                {
                    "module_id": "course_seed_l1_m1",
                    "question_types": ["mcq", "coding"],
                }
            ],
        },
        "assessment_alignment_report": {"overall_status": "needs_review"},
        "packaging_profile": {"packaging_profile_id": "genai_stack_packaging"},
    }

    state = {
        "content_type": "concept_explainer",
        "domain": "genai",
        "module_title": "Fallback Title",
        "module_id": "fallback_m1",
        "estimated_hours": 1.0,
    }

    context = _build_loop_c_execution_context(loop_b_result, state)

    assert context["execution_scope"] == "module"
    assert context["execution_id"] == "course_seed_l1_m1"
    assert context["title"] == "Level 1 — Foundations — Core workflow"
    assert context["instructional_pattern"] == "concept_explainer"
    assert context["course_title"] == "Level 1 — Foundations"
    assert context["curriculum_module_title"] == "Level 1 — Foundations — Core workflow"
    assert context["module_topic_count"] == 1
    assert context["module_learning_unit_count"] == 2
    assert context["module_learning_unit_types"] == ["reading_material_unit", "video_session_unit"]
    assert context["module_practice_types"] == ["guided_reflection"]
    assert context["module_assessment_question_types"] == ["mcq", "fib", "coding"]
    assert context["module_work_plan"]["module_change_type"] == "module_creation"
    assert context["module_work_plan"]["topics"][0]["title"] == "Level 1 — Problem Framing"
    assert context["module_work_plan"]["topics"][0]["learning_units"][1]["unit_type"] == "video_session_unit"
    assert context["module_work_plan"]["module_quiz"]["question_types"] == ["mcq", "coding"]
    assert len(context["module_work_plan"]["production_targets"]) == 4
