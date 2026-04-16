"""Loop A — Intelligence & Signals — LangGraph state machine.

Flow: ingest_signals → detect_patterns → update_skill_graph →
      update_learner_model → update_competitor_map → update_product_context →
      update_wiki_index → END

Uses a TypedDict with reducer annotations so each node can return
partial updates that MERGE into state (rather than replacing it).
"""
from typing import Any, Optional, Annotated
from typing_extensions import TypedDict
import operator

from langgraph.graph import StateGraph, END

from open_acp.loops.loop_a.nodes import (
    ingest_signals,
    detect_patterns,
    update_skill_graph,
    update_learner_model,
    update_competitor_map,
    update_product_context,
    update_wiki_index,
)


def _replace(existing: Any, new: Any) -> Any:
    """Reducer that replaces old value with new (for scalar fields)."""
    return new if new is not None else existing


def _merge_list(existing: list, new: list) -> list:
    """Reducer that concatenates lists (for accumulating wiki entries)."""
    return (existing or []) + (new or [])


class LoopAGraphState(TypedDict, total=False):
    """Typed state for Loop A — fields use reducers for proper merging."""
    cycle_id: Annotated[str, _replace]
    domain: Annotated[str, _replace]
    product_family: Annotated[Any, _replace]
    product_version: Annotated[Any, _replace]
    require_product_context: Annotated[Any, _replace]
    strict_domain_inputs: Annotated[Any, _replace]
    signal_batch: Annotated[Any, _replace]
    detected_patterns: Annotated[list, _replace]
    pattern_detection_status: Annotated[str, _replace]
    pattern_detection_note: Annotated[Any, _replace]
    drift_score: Annotated[float, _replace]
    product_context: Annotated[Any, _replace]
    structure_profile: Annotated[Any, _replace]
    wiki_entries_created: Annotated[list, _merge_list]
    wiki_entries_updated: Annotated[list, _merge_list]
    stack_profiles_created: Annotated[list, _merge_list]
    stack_profiles_updated: Annotated[list, _merge_list]
    gate_g1_outcome: Annotated[Any, _replace]


def build_loop_a_graph() -> StateGraph:
    """Build the Loop A state graph."""
    graph = StateGraph(LoopAGraphState)

    graph.add_node("ingest_signals", ingest_signals)
    graph.add_node("detect_patterns", detect_patterns)
    graph.add_node("update_skill_graph", update_skill_graph)
    graph.add_node("update_learner_model", update_learner_model)
    graph.add_node("update_competitor_map", update_competitor_map)
    graph.add_node("update_product_context", update_product_context)
    graph.add_node("update_wiki_index", update_wiki_index)

    graph.set_entry_point("ingest_signals")

    graph.add_edge("ingest_signals", "detect_patterns")
    graph.add_edge("detect_patterns", "update_skill_graph")
    graph.add_edge("update_skill_graph", "update_learner_model")
    graph.add_edge("update_learner_model", "update_competitor_map")
    graph.add_edge("update_competitor_map", "update_product_context")
    graph.add_edge("update_product_context", "update_wiki_index")
    graph.add_edge("update_wiki_index", END)

    return graph


def run_loop_a(
    domain: str,
    cycle_id: str = "cycle_1",
    product_family: str | None = None,
    product_version: str | None = None,
    require_product_context: bool = False,
    strict_domain_inputs: bool = False,
) -> dict:
    """Convenience function to compile and run Loop A."""
    graph = build_loop_a_graph()
    app = graph.compile()

    initial_state: LoopAGraphState = {
        "cycle_id": cycle_id,
        "domain": domain,
        "product_family": product_family,
        "product_version": product_version,
        "require_product_context": require_product_context,
        "strict_domain_inputs": strict_domain_inputs,
    }

    result = app.invoke(initial_state)
    return dict(result)
