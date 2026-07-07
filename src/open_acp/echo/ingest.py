"""Echo ingestion (Refresh half) — the Learning-Portal-MCP seam.

STUB. The weekly refresh reads portal usage, computes measured deltas, and proposes
doc updates for HITL review. The Portal MCP is not built yet, so this module only
defines the stable interface + a fixture adapter for manual exports. When the MCP
exists, implement ``PortalMCPUsageSource.fetch_since`` and nothing else changes.

Design invariants (see docs/handoff/design_echo_rag_app.md §5):
- Join usage by session_id / unit_id / question_id + content hash — never course_id.
- Carry served-denominator (exposure) counts for any per-item rate.
- Measured facts APPEND with provenance; authored reference facts and locked
  non-negotiables are never silently overwritten.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol


@dataclass
class UsageBatch:
    """A batch of portal usage events since the last refresh."""

    since: str  # ISO date the batch starts from
    rows: list[dict] = field(default_factory=list)  # raw usage records
    source_label: str = ""  # provenance: where this batch came from


@dataclass
class DocUpdateProposal:
    """A proposed edit to a dynamic doc, pending HITL approval."""

    doc_path: str  # repo-relative target doc
    summary: str  # e.g. "misconception M12 prevalence 4% -> 11% (N=2,310)"
    new_text: str  # the proposed replacement/added text
    provenance: str  # source + timestamp + sample size


class UsageSource(Protocol):
    """Anything that can supply portal usage. Swappable adapter."""

    def fetch_since(self, since: str) -> UsageBatch:  # pragma: no cover - protocol
        ...


class FixtureUsageSource:
    """Reads a manually-exported usage file (CSV/JSON) from disk.

    Lets the refresh loop be exercised end-to-end before the MCP exists.
    """

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def fetch_since(self, since: str) -> UsageBatch:
        if not self.path.exists():
            raise FileNotFoundError(f"Usage fixture not found: {self.path}")
        # v0: return raw text rows; parsing/joining is implemented with the real schema.
        rows = [{"raw": line} for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]
        return UsageBatch(since=since, rows=rows, source_label=f"fixture:{self.path.name}")


class PortalMCPUsageSource:
    """Reads usage from the Learning Portal MCP. NOT YET IMPLEMENTED."""

    def fetch_since(self, since: str) -> UsageBatch:
        raise NotImplementedError(
            "Learning Portal MCP is not built yet. Use FixtureUsageSource with a manual "
            "export, or implement this adapter once the MCP exists."
        )


def compute_proposals(batch: UsageBatch) -> list[DocUpdateProposal]:
    """Turn a usage batch into doc-update proposals. STUB.

    Implemented with the real usage schema once extracts exist. Must: join on
    session/unit/question_id + content hash, carry served-denominators, and emit
    append-only measured facts with provenance (never overwrite reference facts).
    """
    raise NotImplementedError(
        "compute_proposals awaits the real portal usage schema. See design doc §5."
    )
