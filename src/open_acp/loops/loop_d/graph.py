"""Loop D — Evaluate + Backpropagate — LangGraph state machine.

Flow: collect_feedback → classify_insights → route_fixes → health_monitor → END
"""
from typing import Any, Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END


def _replace(existing: Any, new: Any) -> Any:
    return new if new is not None else existing


def _merge_list(existing: list, new: list) -> list:
    return (existing or []) + (new or [])


class LoopDGraphState(TypedDict, total=False):
    cycle_id: Annotated[str, _replace]
    domain: Annotated[str, _replace]
    content_modules: Annotated[list, _replace]
    raw_feedback: Annotated[list, _replace]
    insights: Annotated[list, _merge_list]
    fix_routes: Annotated[list, _merge_list]
    health_report: Annotated[dict, _replace]
    gate_g4_outcome: Annotated[Any, _replace]


def build_loop_d_graph() -> StateGraph:
    from open_acp.loops.loop_d.nodes import (
        collect_feedback,
        classify_insights,
        route_fixes,
        health_monitor,
    )

    graph = StateGraph(LoopDGraphState)
    graph.add_node("collect_feedback", collect_feedback)
    graph.add_node("classify_insights", classify_insights)
    graph.add_node("route_fixes", route_fixes)
    graph.add_node("health_monitor", health_monitor)

    graph.set_entry_point("collect_feedback")
    graph.add_edge("collect_feedback", "classify_insights")
    graph.add_edge("classify_insights", "route_fixes")
    graph.add_edge("route_fixes", "health_monitor")
    graph.add_edge("health_monitor", END)

    return graph


def run_loop_d(domain: str, cycle_id: str = "cycle_1", content_modules: list = None) -> dict:
    """Convenience function to compile and run Loop D."""
    graph = build_loop_d_graph()
    app = graph.compile()
    initial_state: LoopDGraphState = {
        "cycle_id": cycle_id,
        "domain": domain,
        "content_modules": content_modules or [],
    }
    result = app.invoke(initial_state)
    return dict(result)
