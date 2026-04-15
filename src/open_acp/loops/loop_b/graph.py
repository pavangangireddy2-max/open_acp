"""Loop B — Curriculum Design — LangGraph state machine.

Flow: load_wiki_context → select_pedagogy → generate_curriculum → generate_differentiation → align_assessments → END
"""
from typing import Any, Optional, Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END


def _replace(existing: Any, new: Any) -> Any:
    return new if new is not None else existing


class LoopBGraphState(TypedDict, total=False):
    cycle_id: Annotated[str, _replace]
    domain: Annotated[str, _replace]
    content_type: Annotated[str, _replace]
    skill_graph_context: Annotated[str, _replace]
    learner_context: Annotated[str, _replace]
    selected_pedagogy: Annotated[str, _replace]
    pedagogy_justification: Annotated[str, _replace]
    curriculum_map: Annotated[Any, _replace]
    differentiation_matrix: Annotated[Any, _replace]
    assessment_alignment: Annotated[Any, _replace]
    gate_g2_outcome: Annotated[Any, _replace]


def build_loop_b_graph() -> StateGraph:
    from open_acp.loops.loop_b.nodes import (
        load_wiki_context,
        select_pedagogy,
        generate_curriculum,
        generate_differentiation,
        align_assessments,
    )

    graph = StateGraph(LoopBGraphState)
    graph.add_node("load_wiki_context", load_wiki_context)
    graph.add_node("select_pedagogy", select_pedagogy)
    graph.add_node("generate_curriculum", generate_curriculum)
    graph.add_node("generate_differentiation", generate_differentiation)
    graph.add_node("align_assessments", align_assessments)

    graph.set_entry_point("load_wiki_context")
    graph.add_edge("load_wiki_context", "select_pedagogy")
    graph.add_edge("select_pedagogy", "generate_curriculum")
    graph.add_edge("generate_curriculum", "generate_differentiation")
    graph.add_edge("generate_differentiation", "align_assessments")
    graph.add_edge("align_assessments", END)

    return graph


def run_loop_b(domain: str, cycle_id: str = "cycle_1", content_type: str = "concept_explainer") -> dict:
    """Convenience function to compile and run Loop B."""
    graph = build_loop_b_graph()
    app = graph.compile()
    initial_state: LoopBGraphState = {
        "cycle_id": cycle_id,
        "domain": domain,
        "content_type": content_type,
    }
    result = app.invoke(initial_state)
    return dict(result)
