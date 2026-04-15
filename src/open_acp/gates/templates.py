"""Gate display templates — rich CLI formatting for gate presentations."""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from open_acp.models.gates import GateType, GateOutcome


console = Console()


def display_gate_request(gate_type: GateType, context: dict) -> None:
    """Display a gate approval request with rich formatting."""
    gate_labels = {
        GateType.G1: ("Strategy Review", "yellow"),
        GateType.G2: ("Curriculum Approval", "red"),
        GateType.G3: ("Content Quality", "blue"),
        GateType.G4: ("High-Severity Fix", "red"),
    }
    label, color = gate_labels.get(gate_type, ("Unknown", "white"))

    console.print(Panel(
        f"[bold]{label}[/bold]\n\n"
        f"Loop: {context.get('loop', '?')}\n"
        f"Cycle: {context.get('cycle_id', '?')}\n"
        f"Domain: {context.get('domain', '?')}",
        title=f"Gate {gate_type.value}",
        border_style=color,
    ))


def display_gate_outcome(outcome: GateOutcome) -> None:
    """Display the outcome of a gate decision."""
    decision_style = {
        "approve": "green",
        "revise": "yellow",
        "abort": "red",
    }
    style = decision_style.get(outcome.decision.value, "white")
    console.print(f"  Gate {outcome.gate_type.value}: [{style}]{outcome.decision.value.upper()}[/{style}] -- {outcome.reason}")
