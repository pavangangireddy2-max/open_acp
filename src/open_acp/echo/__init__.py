"""Echo — the Agentic-RAG surface over the Open ACP intelligence layer.

v0 ships the *Ask* half: answer questions grounded in the handoff docs, manifests,
pedagogy YAML, architecture docs, and raw extracted sources, with citations.

The *Refresh* half (weekly Portal-MCP ingestion → HITL doc updates) is stubbed in
``ingest`` / ``refresh`` and implemented when the Learning Portal MCP exists.

See docs/handoff/design_echo_rag_app.md for the full spec.
"""

from open_acp.echo.ask import Answer, ask
from open_acp.echo.corpus import Source, list_sources, load_source

__all__ = ["Answer", "ask", "Source", "list_sources", "load_source"]
