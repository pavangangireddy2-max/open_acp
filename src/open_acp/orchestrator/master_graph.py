"""Master graph — wires all 4 loops: A → B → C → D.

This is the outer orchestrator. Each loop is a subgraph that runs internally
using its own LangGraph state machine.
"""
import json
from datetime import datetime, UTC
from typing import Any, Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, END


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

    # Build module context from Loop B result or defaults
    loop_b_result = state.get("loop_b_result", {})
    curriculum = loop_b_result.get("curriculum_map", {})
    modules = curriculum.get("modules", [])

    # Use first module from curriculum, or build a default
    if modules:
        first_module = modules[0]
        module_context = {
            "module_id": first_module.get("module_id", state.get("module_id", "m1")),
            "title": first_module.get("title", state.get("module_title", "Introduction")),
            "domain": domain,
            "estimated_hours": first_module.get("estimated_hours", state.get("estimated_hours", 1.0)),
            "objectives": first_module.get("objectives", []),
            "prerequisites": first_module.get("prerequisite_modules", []),
            "pedagogy_profile": loop_b_result.get("pedagogy_profile"),
        }
    else:
        module_context = {
            "module_id": state.get("module_id", "m1"),
            "title": state.get("module_title", "Introduction"),
            "domain": domain,
            "estimated_hours": state.get("estimated_hours", 1.0),
            "objectives": [],
            "prerequisites": [],
            "pedagogy_profile": loop_b_result.get("pedagogy_profile"),
        }

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
            "content_type": content_type,
        }
        print(f"\n  Loop C complete: {len(artifacts)} stages")
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
