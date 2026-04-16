"""Master graph — wires all 4 loops: A → B → C → D.

This is the outer orchestrator. Each loop is a subgraph that runs internally
using its own LangGraph state machine.
"""
from datetime import datetime, UTC
from typing import Any, Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, END

from open_acp.models.delivery import (
    AssessmentNature,
    AssessmentSystem,
    LearningUnitType,
    ModuleChangeType,
    ModuleWorkPlan,
    PlacementEligibilityRole,
    ProductionTarget,
    TopicDeliveryPlan,
)


def _replace(existing: Any, new: Any) -> Any:
    return new if new is not None else existing


class MasterGraphState(TypedDict, total=False):
    run_id: Annotated[str, _replace]
    cycle_id: Annotated[str, _replace]
    domain: Annotated[str, _replace]
    content_type: Annotated[str, _replace]
    module_title: Annotated[str, _replace]
    module_id: Annotated[str, _replace]
    estimated_hours: Annotated[float, _replace]
    auto_approve: Annotated[bool, _replace]
    # Loop results
    loop_a_result: Annotated[dict, _replace]
    loop_b_result: Annotated[dict, _replace]
    loop_c_result: Annotated[dict, _replace]
    loop_d_result: Annotated[dict, _replace]
    current_loop: Annotated[str, _replace]
    error: Annotated[str, _replace]


def _index_by(items: list[dict], key: str) -> dict[str, dict]:
    return {item[key]: item for item in items if item.get(key)}


def _unique_preserve_order(items: list[Any]) -> list[Any]:
    seen = set()
    ordered: list[Any] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


def _assessment_unit_type(assessment_id: str) -> str:
    if assessment_id.endswith("_classroom_quiz"):
        return LearningUnitType.CLASSROOM_QUIZ_UNIT.value
    if assessment_id.endswith("_module_quiz"):
        return LearningUnitType.MODULE_QUIZ_UNIT.value
    if assessment_id.endswith("_final_course_quiz"):
        return LearningUnitType.FINAL_COURSE_QUIZ_UNIT.value
    return LearningUnitType.CLASSROOM_QUIZ_UNIT.value


def _normalize_learning_unit_type(unit_type: str | None) -> str | None:
    if unit_type == "ppt_video_unit":
        return LearningUnitType.VIDEO_SESSION_UNIT.value
    return unit_type


def _select_module(
    modules: list[dict],
    courses_by_id: dict[str, dict],
    requested_module_id: str,
    requested_module_title: str,
) -> dict | None:
    if not modules:
        return None

    for module in modules:
        if module.get("module_id") == requested_module_id:
            return module

    if requested_module_id:
        for module in modules:
            course = courses_by_id.get(module.get("course_id", ""), {})
            if course.get("course_id") == requested_module_id:
                return module
            if course.get("source_module_id") == requested_module_id:
                return module

    if requested_module_title:
        requested_lower = requested_module_title.strip().lower()
        for module in modules:
            if module.get("title", "").strip().lower() == requested_lower:
                return module

    return modules[0]


def _build_module_work_plan(
    *,
    content_type: str,
    loop_b_result: dict,
    curriculum: dict,
    course: dict,
    curriculum_module: dict,
    topics: list[dict],
    learning_units: list[dict],
    practice_items: list[dict],
    classroom_quizzes: list[dict],
    module_quiz: dict,
    packaging_profile: dict,
) -> ModuleWorkPlan:
    practice_by_topic = _index_by(practice_items, "topic_id")
    classroom_quiz_by_topic = _index_by(classroom_quizzes, "topic_id")
    units_by_topic: dict[str, list[dict]] = {}
    for unit in learning_units:
        units_by_topic.setdefault(unit.get("topic_id", ""), []).append(unit)

    topic_plans: list[TopicDeliveryPlan] = []
    production_targets: list[ProductionTarget] = []
    for topic in topics:
        topic_id = topic.get("topic_id", "")
        topic_units = units_by_topic.get(topic_id, [])
        practice_item = practice_by_topic.get(topic_id)
        classroom_quiz = classroom_quiz_by_topic.get(topic_id)

        topic_plans.append(
            TopicDeliveryPlan(
                topic_id=topic_id,
                title=topic.get("title", "Untitled Topic"),
                sequence_within_module=int(topic.get("sequence_within_module", 0) or 0),
                estimated_minutes=float(topic.get("estimated_minutes", 0) or 0),
                skill_ids=topic.get("skill_ids", []),
                focus_outcomes=topic.get("focus_outcomes", []),
                learning_units=topic_units,
                practice_item=practice_item,
                classroom_quiz=classroom_quiz,
            )
        )

        for unit in topic_units:
            production_targets.append(
                ProductionTarget(
                    target_scope="learning_unit",
                    target_id=unit.get("learning_unit_id", ""),
                    title=unit.get("title", "Untitled Learning Unit"),
                    topic_id=topic_id,
                    learning_unit_type=_normalize_learning_unit_type(unit.get("unit_type")),
                    instructional_pattern=content_type,
                    question_formats=[],
                    metadata={
                        "delivery_intent": unit.get("delivery_intent"),
                        "estimated_minutes": unit.get("estimated_minutes"),
                    },
                )
            )

        if classroom_quiz:
            production_targets.append(
                ProductionTarget(
                    target_scope="assessment_unit",
                    target_id=classroom_quiz.get("assessment_id", ""),
                    title=f"{topic.get('title', 'Topic')} — Classroom Quiz",
                    topic_id=topic_id,
                    learning_unit_type=_assessment_unit_type(classroom_quiz.get("assessment_id", "")),
                    assessment_system=AssessmentSystem.LEARNING.value,
                    assessment_nature=AssessmentNature.FORMATIVE.value,
                    question_formats=classroom_quiz.get("question_types", []),
                    metadata={
                        "difficulty": classroom_quiz.get("difficulty"),
                        "cadence_minutes": classroom_quiz.get("cadence_minutes"),
                    },
                )
            )

    if module_quiz:
        production_targets.append(
            ProductionTarget(
                target_scope="assessment_unit",
                target_id=module_quiz.get("assessment_id", ""),
                title=f"{curriculum_module.get('title', 'Module')} — Module Quiz",
                learning_unit_type=_assessment_unit_type(module_quiz.get("assessment_id", "")),
                assessment_system=AssessmentSystem.LEARNING.value,
                assessment_nature=AssessmentNature.SUMMATIVE.value,
                question_formats=module_quiz.get("question_types", []),
                metadata={"difficulty": module_quiz.get("difficulty")},
            )
        )

    assessment_question_types = _unique_preserve_order(
        question_type
        for quiz in classroom_quizzes + ([module_quiz] if module_quiz else [])
        for question_type in quiz.get("question_types", [])
    )
    practice_types = _unique_preserve_order(
        item.get("practice_type", "")
        for item in practice_items
        if item.get("practice_type")
    )
    learning_unit_types = _unique_preserve_order(
        _normalize_learning_unit_type(unit.get("unit_type", ""))
        for unit in learning_units
        if _normalize_learning_unit_type(unit.get("unit_type"))
    )

    return ModuleWorkPlan(
        curriculum_id=curriculum.get("curriculum_id"),
        curriculum_title=curriculum.get("program_name"),
        course_id=course.get("course_id"),
        course_title=course.get("title"),
        module_id=curriculum_module.get("module_id", "unknown_module"),
        module_title=curriculum_module.get("title", "Untitled Module"),
        module_change_type=ModuleChangeType.MODULE_CREATION.value,
        module_sequence_within_course=curriculum_module.get("sequence_within_course"),
        estimated_hours=float(curriculum_module.get("estimated_hours", 0) or 0),
        pedagogy_profile=loop_b_result.get("pedagogy_profile"),
        instructional_pattern=content_type,
        packaging_profile_id=packaging_profile.get("packaging_profile_id"),
        skill_ids=curriculum_module.get("skill_ids", []),
        focus_outcomes=curriculum_module.get("focus_outcomes", []),
        topic_count=len(topic_plans),
        learning_unit_count=len(learning_units),
        learning_unit_types=learning_unit_types,
        practice_types=practice_types,
        classroom_quiz_count=len(classroom_quizzes),
        assessment_question_types=assessment_question_types,
        topics=topic_plans,
        module_quiz=module_quiz or None,
        skill_assessment_alignment=loop_b_result.get("assessment_alignment_report", {}) or {},
        production_targets=production_targets,
    )


def _build_loop_c_execution_context(loop_b_result: dict, state: dict) -> dict:
    """Build a richer Loop C execution context from Loop B outputs.

    Compatibility behavior:
    - Prefer a module-first execution target with a nested delivery plan when Loop B has expanded design artifacts.
    - Fall back to the older curriculum_map.modules contract when those richer artifacts are absent.
    """
    content_type = state.get("content_type", "concept_explainer")
    domain = state.get("domain", "ml-engineering")
    curriculum = loop_b_result.get("curriculum_map", {}) or {}
    course_design = loop_b_result.get("course_design", {}) or {}
    module_design = loop_b_result.get("module_design", {}) or {}
    topic_design = loop_b_result.get("topic_design", {}) or {}
    learning_unit_plan = loop_b_result.get("learning_unit_plan", {}) or {}
    practice_design = loop_b_result.get("practice_design", {}) or {}
    learning_assessment_plan = loop_b_result.get("learning_assessment_plan", {}) or {}
    assessment_alignment_report = loop_b_result.get("assessment_alignment_report", {}) or {}
    packaging_profile = loop_b_result.get("packaging_profile", {}) or {}

    curriculum_seeds = _index_by(curriculum.get("modules", []) or [], "module_id")
    courses_by_id = _index_by(course_design.get("courses", []) or [], "course_id")
    modules_by_id = _index_by(module_design.get("modules", []) or [], "module_id")
    modules = sorted(
        module_design.get("modules", []) or [],
        key=lambda module: (
            courses_by_id.get(module.get("course_id", ""), {}).get("sequence", 999),
            module.get("sequence_within_course", 999),
            module.get("module_id", ""),
        ),
    )
    learning_units = learning_unit_plan.get("learning_units", []) or []
    selected_module = _select_module(
        modules=modules,
        courses_by_id=courses_by_id,
        requested_module_id=state.get("module_id", ""),
        requested_module_title=state.get("module_title", ""),
    )
    if selected_module:
        course = courses_by_id.get(selected_module.get("course_id", ""), {})
        source_seed = curriculum_seeds.get(course.get("source_module_id", ""), {})
        selected_topics = sorted(
            [
                topic
                for topic in (topic_design.get("topics", []) or [])
                if topic.get("module_id") == selected_module.get("module_id")
            ],
            key=lambda topic: (topic.get("sequence_within_module", 999), topic.get("topic_id", "")),
        )
        selected_topic_ids = {topic.get("topic_id") for topic in selected_topics}
        selected_learning_units = [
            unit
            for unit in learning_units
            if unit.get("module_id") == selected_module.get("module_id")
        ]
        selected_practice_items = [
            item
            for item in (practice_design.get("items", []) or [])
            if item.get("module_id") == selected_module.get("module_id")
            or item.get("topic_id") in selected_topic_ids
        ]
        selected_classroom_quizzes = [
            item
            for item in (learning_assessment_plan.get("classroom_quizzes", []) or [])
            if item.get("module_id") == selected_module.get("module_id")
            or item.get("topic_id") in selected_topic_ids
        ]
        module_quiz = next(
            (
                item
                for item in (learning_assessment_plan.get("module_quizzes", []) or [])
                if item.get("module_id") == selected_module.get("module_id")
            ),
            {},
        )
        module_work_plan = _build_module_work_plan(
            content_type=content_type,
            loop_b_result=loop_b_result,
            curriculum=curriculum,
            course=course,
            curriculum_module=selected_module,
            topics=selected_topics,
            learning_units=selected_learning_units,
            practice_items=selected_practice_items,
            classroom_quizzes=selected_classroom_quizzes,
            module_quiz=module_quiz,
            packaging_profile=packaging_profile,
        )
        return {
            "execution_scope": "module",
            "execution_id": selected_module.get("module_id", state.get("module_id", "m1")),
            "execution_title": selected_module.get("title", state.get("module_title", "Introduction")),
            "module_id": selected_module.get("module_id", state.get("module_id", "m1")),
            "title": selected_module.get("title", state.get("module_title", "Introduction")),
            "domain": domain,
            "estimated_hours": float(selected_module.get("estimated_hours", 0) or state.get("estimated_hours", 1.0)),
            "objectives": source_seed.get("objectives", []),
            "prerequisites": source_seed.get("prerequisite_modules", []),
            "pedagogy_profile": loop_b_result.get("pedagogy_profile"),
            "instructional_pattern": content_type,
            "curriculum_id": curriculum.get("curriculum_id"),
            "curriculum_title": curriculum.get("program_name", f"{domain} Curriculum"),
            "course_id": course.get("course_id"),
            "course_title": course.get("title"),
            "course_sequence": course.get("sequence"),
            "curriculum_module_id": selected_module.get("module_id"),
            "curriculum_module_title": selected_module.get("title"),
            "module_sequence_within_course": selected_module.get("sequence_within_course"),
            "packaging_profile_id": packaging_profile.get("packaging_profile_id"),
            "module_topic_count": module_work_plan.topic_count,
            "module_learning_unit_count": module_work_plan.learning_unit_count,
            "module_learning_unit_types": module_work_plan.learning_unit_types,
            "module_practice_types": module_work_plan.practice_types,
            "module_assessment_question_types": module_work_plan.assessment_question_types,
            "module_work_plan": module_work_plan.model_dump(mode="json"),
            "skill_assessment_alignment": assessment_alignment_report,
            "requested_module_id": state.get("module_id"),
            "requested_module_title": state.get("module_title"),
        }

    modules = curriculum.get("modules", []) or []
    if modules:
        first_module = modules[0]
        fallback_plan = ModuleWorkPlan(
            curriculum_id=curriculum.get("curriculum_id"),
            curriculum_title=curriculum.get("program_name", f"{domain} Curriculum"),
            module_id=first_module.get("module_id", state.get("module_id", "m1")),
            module_title=first_module.get("title", state.get("module_title", "Introduction")),
            module_change_type=ModuleChangeType.MODULE_CREATION.value,
            estimated_hours=float(first_module.get("estimated_hours", state.get("estimated_hours", 1.0)) or 0),
            pedagogy_profile=loop_b_result.get("pedagogy_profile"),
            instructional_pattern=content_type,
            skill_ids=_unique_preserve_order(
                skill_id
                for objective in first_module.get("objectives", [])
                for skill_id in objective.get("skill_ids", [])
            ),
            focus_outcomes=[
                objective.get("statement", "")
                for objective in first_module.get("objectives", [])
                if objective.get("statement")
            ],
        )
        return {
            "execution_scope": "module",
            "execution_id": first_module.get("module_id", state.get("module_id", "m1")),
            "execution_title": first_module.get("title", state.get("module_title", "Introduction")),
            "module_id": first_module.get("module_id", state.get("module_id", "m1")),
            "title": first_module.get("title", state.get("module_title", "Introduction")),
            "domain": domain,
            "estimated_hours": first_module.get("estimated_hours", state.get("estimated_hours", 1.0)),
            "objectives": first_module.get("objectives", []),
            "prerequisites": first_module.get("prerequisite_modules", []),
            "pedagogy_profile": loop_b_result.get("pedagogy_profile"),
            "instructional_pattern": content_type,
            "curriculum_id": curriculum.get("curriculum_id"),
            "curriculum_title": curriculum.get("program_name", f"{domain} Curriculum"),
            "curriculum_module_id": first_module.get("module_id", state.get("module_id", "m1")),
            "curriculum_module_title": first_module.get("title", state.get("module_title", "Introduction")),
            "module_topic_count": 0,
            "module_learning_unit_count": 0,
            "module_learning_unit_types": [],
            "module_practice_types": [],
            "module_assessment_question_types": [],
            "module_work_plan": fallback_plan.model_dump(mode="json"),
        }

    fallback_id = state.get("module_id", "m1")
    fallback_title = state.get("module_title", "Introduction")
    fallback_plan = ModuleWorkPlan(
        curriculum_title=curriculum.get("program_name", f"{domain} Curriculum"),
        module_id=fallback_id,
        module_title=fallback_title,
        module_change_type=ModuleChangeType.MODULE_CREATION.value,
        estimated_hours=float(state.get("estimated_hours", 1.0) or 0),
        pedagogy_profile=loop_b_result.get("pedagogy_profile"),
        instructional_pattern=content_type,
    )
    return {
        "execution_scope": "module",
        "execution_id": fallback_id,
        "execution_title": fallback_title,
        "module_id": fallback_id,
        "title": fallback_title,
        "domain": domain,
        "estimated_hours": state.get("estimated_hours", 1.0),
        "objectives": [],
        "prerequisites": [],
        "pedagogy_profile": loop_b_result.get("pedagogy_profile"),
        "instructional_pattern": content_type,
        "curriculum_title": curriculum.get("program_name", f"{domain} Curriculum"),
        "curriculum_module_id": fallback_id,
        "curriculum_module_title": fallback_title,
        "module_topic_count": 0,
        "module_learning_unit_count": 0,
        "module_learning_unit_types": [],
        "module_practice_types": [],
        "module_assessment_question_types": [],
        "module_work_plan": fallback_plan.model_dump(mode="json"),
    }


def run_loop_a_node(state: dict) -> dict:
    """Execute Loop A — Intelligence & Signals."""
    print("\n" + "="*60)
    print("  LOOP A: Intelligence & Signals")
    print("="*60)

    from open_acp.loops.loop_a.graph import run_loop_a
    result = run_loop_a(
        domain=state.get("domain", "ml-engineering"),
        cycle_id=state.get("cycle_id", "cycle_1"),
    )

    created = result.get("wiki_entries_created", [])
    updated = result.get("wiki_entries_updated", [])
    print(f"\n  Loop A complete: {len(created)} created, {len(updated)} updated, drift={result.get('drift_score', 0):.2f}")
    return {"loop_a_result": result, "current_loop": "B"}


def run_loop_b_node(state: dict) -> dict:
    """Execute Loop B — Curriculum Design."""
    print("\n" + "="*60)
    print("  LOOP B: Curriculum Design")
    print("="*60)

    from open_acp.loops.loop_b.graph import run_loop_b
    result = run_loop_b(
        domain=state.get("domain", "ml-engineering"),
        cycle_id=state.get("cycle_id", "cycle_1"),
        content_type=state.get("content_type", "concept_explainer"),
    )

    curriculum = result.get("curriculum_map", {})
    modules = curriculum.get("modules", [])
    print(f"\n  Loop B complete: {len(modules)} modules, pedagogy_profile={result.get('pedagogy_profile', '?')}")
    return {"loop_b_result": result, "current_loop": "C"}


def run_loop_c_node(state: dict) -> dict:
    """Execute Loop C — Content Compilation."""
    print("\n" + "="*60)
    print("  LOOP C: Content Compilation")
    print("="*60)

    from open_acp.loops.loop_c.pipeline_executor import PipelineExecutor
    from open_acp.tools.tool_registry import registry
    registry.discover()

    content_type = state.get("content_type", "concept_explainer")
    domain = state.get("domain", "ml-engineering")

    loop_b_result = state.get("loop_b_result", {})
    module_context = _build_loop_c_execution_context(loop_b_result, state)

    executor = PipelineExecutor()
    try:
        artifacts = executor.execute_pipeline(
            content_type=content_type,
            module_context=module_context,
            domain=domain,
        )
        result = {
            "stages_completed": len(artifacts),
            "stage_ids": list(artifacts.keys()),
            "module_id": module_context["module_id"],
            "execution_scope": module_context.get("execution_scope", "module"),
            "execution_id": module_context.get("execution_id", module_context["module_id"]),
            "execution_title": module_context.get("execution_title", module_context.get("title", "Untitled")),
            "instructional_pattern": module_context.get("instructional_pattern"),
            "course_id": module_context.get("course_id"),
            "curriculum_module_id": module_context.get("curriculum_module_id", module_context["module_id"]),
            "module_topic_count": module_context.get("module_topic_count", 0),
            "module_learning_unit_count": module_context.get("module_learning_unit_count", 0),
            "content_type": content_type,
        }
        print(
            f"\n  Loop C complete: {len(artifacts)} stages "
            f"for {result['execution_scope']} '{result['execution_title']}'"
        )
    except Exception as e:
        result = {"error": str(e), "stages_completed": 0}
        print(f"\n  Loop C error: {e}")

    return {"loop_c_result": result, "current_loop": "D"}


def run_loop_d_node(state: dict) -> dict:
    """Execute Loop D — Evaluate + Backpropagate."""
    print("\n" + "="*60)
    print("  LOOP D: Evaluate + Backpropagate")
    print("="*60)

    from open_acp.loops.loop_d.graph import run_loop_d

    loop_c_result = state.get("loop_c_result", {})
    content_modules = [loop_c_result.get("module_id", "m1")]

    result = run_loop_d(
        domain=state.get("domain", "ml-engineering"),
        cycle_id=state.get("cycle_id", "cycle_1"),
        content_modules=content_modules,
    )

    print(f"\n  Loop D complete: {result.get('health_report', {}).get('insights_count', 0)} insights, {result.get('health_report', {}).get('fix_routes_count', 0)} fixes routed")
    return {"loop_d_result": result, "current_loop": "complete"}


def build_master_graph() -> StateGraph:
    """Build the master A → B → C → D graph."""
    graph = StateGraph(MasterGraphState)

    graph.add_node("loop_a", run_loop_a_node)
    graph.add_node("loop_b", run_loop_b_node)
    graph.add_node("loop_c", run_loop_c_node)
    graph.add_node("loop_d", run_loop_d_node)

    graph.set_entry_point("loop_a")
    graph.add_edge("loop_a", "loop_b")
    graph.add_edge("loop_b", "loop_c")
    graph.add_edge("loop_c", "loop_d")
    graph.add_edge("loop_d", END)

    return graph


def run_master(
    domain: str,
    content_type: str = "concept_explainer",
    module_title: str = "Introduction",
    module_id: str = "m1",
    estimated_hours: float = 1.0,
    auto_approve: bool = False,
    cycle_id: str = "cycle_1",
) -> dict:
    """Run the full A → B → C → D pipeline."""
    import uuid

    graph = build_master_graph()
    app = graph.compile()

    initial_state: MasterGraphState = {
        "run_id": f"run_{uuid.uuid4().hex[:8]}",
        "cycle_id": cycle_id,
        "domain": domain,
        "content_type": content_type,
        "module_title": module_title,
        "module_id": module_id,
        "estimated_hours": estimated_hours,
        "auto_approve": auto_approve,
        "current_loop": "A",
    }

    result = app.invoke(initial_state)
    return dict(result)
