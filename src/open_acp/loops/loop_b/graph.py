"""Loop B — Curriculum Design — LangGraph state machine."""
from typing import Any, Optional, Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END


def _replace(existing: Any, new: Any) -> Any:
    return new if new is not None else existing


class LoopBGraphState(TypedDict, total=False):
    cycle_id: Annotated[str, _replace]
    domain: Annotated[str, _replace]
    product_family: Annotated[Any, _replace]
    product_version: Annotated[Any, _replace]
    require_product_context: Annotated[Any, _replace]
    strict_domain_inputs: Annotated[Any, _replace]
    content_type: Annotated[str, _replace]
    detected_patterns: Annotated[Any, _replace]
    drift_score: Annotated[Any, _replace]
    skill_graph_context: Annotated[str, _replace]
    learner_context: Annotated[str, _replace]
    curriculum_source_context: Annotated[str, _replace]
    program_context: Annotated[str, _replace]
    product_context: Annotated[Any, _replace]
    structure_profile: Annotated[Any, _replace]
    pedagogy_profile: Annotated[str, _replace]
    pedagogy_rationale: Annotated[str, _replace]
    curriculum_generation_status: Annotated[str, _replace]
    curriculum_generation_note: Annotated[Any, _replace]
    curriculum_generation_raw_response: Annotated[Any, _replace]
    previous_curriculum_map: Annotated[Any, _replace]
    curriculum_map: Annotated[Any, _replace]
    curriculum_change_report: Annotated[Any, _replace]
    packaging_profile: Annotated[Any, _replace]
    course_design: Annotated[Any, _replace]
    module_design: Annotated[Any, _replace]
    topic_design: Annotated[Any, _replace]
    learning_unit_plan: Annotated[Any, _replace]
    practice_design: Annotated[Any, _replace]
    learning_assessment_plan: Annotated[Any, _replace]
    skill_assessment_requirements: Annotated[Any, _replace]
    assessment_alignment_report: Annotated[Any, _replace]
    gate_g2_outcome: Annotated[Any, _replace]


def build_loop_b_graph() -> StateGraph:
    from open_acp.loops.loop_b.nodes import (
        load_wiki_context,
        resolve_product_context,
        resolve_structure_profile,
        resolve_packaging_profile,
        resolve_pedagogy_profile,
        generate_curriculum,
        compare_curriculum_changes,
        design_courses,
        design_modules,
        design_topics,
        design_learning_units,
        design_practice,
        design_learning_assessments,
        resolve_skill_assessment_requirements,
        align_learning_with_skill_assessments,
    )

    graph = StateGraph(LoopBGraphState)
    graph.add_node("load_wiki_context", load_wiki_context)
    graph.add_node("resolve_product_context", resolve_product_context)
    graph.add_node("resolve_structure_profile", resolve_structure_profile)
    graph.add_node("resolve_packaging_profile", resolve_packaging_profile)
    graph.add_node("resolve_pedagogy_profile", resolve_pedagogy_profile)
    graph.add_node("generate_curriculum", generate_curriculum)
    graph.add_node("compare_curriculum_changes", compare_curriculum_changes)
    graph.add_node("design_courses", design_courses)
    graph.add_node("design_modules", design_modules)
    graph.add_node("design_topics", design_topics)
    graph.add_node("design_learning_units", design_learning_units)
    graph.add_node("design_practice", design_practice)
    graph.add_node("design_learning_assessments", design_learning_assessments)
    graph.add_node("resolve_skill_assessment_requirements", resolve_skill_assessment_requirements)
    graph.add_node("align_learning_with_skill_assessments", align_learning_with_skill_assessments)

    graph.set_entry_point("load_wiki_context")
    graph.add_edge("load_wiki_context", "resolve_product_context")
    graph.add_edge("resolve_product_context", "resolve_structure_profile")
    graph.add_edge("resolve_structure_profile", "resolve_packaging_profile")
    graph.add_edge("resolve_packaging_profile", "resolve_pedagogy_profile")
    graph.add_edge("resolve_pedagogy_profile", "generate_curriculum")
    graph.add_edge("generate_curriculum", "compare_curriculum_changes")
    graph.add_edge("compare_curriculum_changes", "design_courses")
    graph.add_edge("design_courses", "design_modules")
    graph.add_edge("design_modules", "design_topics")
    graph.add_edge("design_topics", "design_learning_units")
    graph.add_edge("design_learning_units", "design_practice")
    graph.add_edge("design_practice", "design_learning_assessments")
    graph.add_edge("design_learning_assessments", "resolve_skill_assessment_requirements")
    graph.add_edge("resolve_skill_assessment_requirements", "align_learning_with_skill_assessments")
    graph.add_edge("align_learning_with_skill_assessments", END)

    return graph


def run_loop_b(
    domain: str,
    cycle_id: str = "cycle_1",
    content_type: str = "concept_explainer",
    product_family: str | None = None,
    product_version: str | None = None,
    require_product_context: bool = False,
    strict_domain_inputs: bool = False,
) -> dict:
    """Convenience function to compile and run Loop B."""
    graph = build_loop_b_graph()
    app = graph.compile()
    initial_state: LoopBGraphState = {
        "cycle_id": cycle_id,
        "domain": domain,
        "product_family": product_family,
        "product_version": product_version,
        "require_product_context": require_product_context,
        "strict_domain_inputs": strict_domain_inputs,
        "content_type": content_type,
    }
    result = app.invoke(initial_state)
    return dict(result)
