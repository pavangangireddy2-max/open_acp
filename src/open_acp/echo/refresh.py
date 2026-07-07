"""Echo refresh (Refresh half) — weekly measured-layer update. STUB.

Orchestrates: fetch usage -> compute proposals -> HITL gate -> write approved edits
to the working tree. Echo is WRITE-ONLY: it never runs git; the human commits.

Not wired up in v0 (needs the Portal MCP + real usage schema). The shape is fixed so
the implementation is a fill-in, not a redesign.
"""

from __future__ import annotations

from open_acp.echo.ingest import (
    DocUpdateProposal,
    UsageSource,
    compute_proposals,
)
from open_acp.gates.gate_runner import GateRunner


def run_refresh(source: UsageSource, since: str, *, gate: GateRunner | None = None) -> list[DocUpdateProposal]:
    """Run one refresh cycle. Returns the proposals that were approved and written.

    STUB: relies on compute_proposals + the write step, both pending the real schema.
    """
    raise NotImplementedError(
        "run_refresh is not implemented in v0. Requires the Learning Portal MCP and the "
        "real usage schema. See docs/handoff/design_echo_rag_app.md §5. "
        "When implemented: fetch -> compute_proposals -> GateRunner.request_approval per "
        "proposal -> write approved new_text to doc_path in the working tree (no git)."
    )
