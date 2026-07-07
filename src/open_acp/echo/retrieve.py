"""Echo retrieval — local embedding ranking (no LLM selection call).

``retrieve(question) -> list[Source]`` ranks whole sources by embedding similarity
(via embeddings.py) and returns the top ones, bounded by a token budget. This replaces
the earlier cheap-tier LLM selection step: ranking is now a <10ms local matrix multiply,
removing a network round-trip from every question.

Interface unchanged, so ask.py is unaffected. If embeddings are unavailable (model not
installed), falls back to the handoff + pedagogy docs so Ask still works.
"""

from __future__ import annotations

from open_acp.echo.corpus import Source, list_sources

# Token ceiling for the docs handed to the answer step.
_ANSWER_TOKEN_BUDGET = 200_000
# How many top-ranked sources to consider before applying the budget.
_TOP_SOURCES = 12


def _fallback_sources(sources: list[Source]) -> list[Source]:
    picked = [s for s in sources if s.category in {"handoff", "pedagogy"}]
    return picked or sources


def _apply_budget(sources: list[Source], budget: int) -> list[Source]:
    kept: list[Source] = []
    total = 0
    for src in sources:
        total += src.approx_tokens
        kept.append(src)
        if total >= budget:
            break
    return kept


def retrieve(
    question: str,
    *,
    client=None,  # kept for signature compatibility; unused (no LLM selection now)
    sources: list[Source] | None = None,
    budget: int = _ANSWER_TOKEN_BUDGET,
    top_k: int = _TOP_SOURCES,
) -> list[Source]:
    """Return the sources most relevant to ``question``, bounded by a token budget."""
    sources = sources if sources is not None else list_sources()
    if not sources:
        return []

    by_key = {s.key: s for s in sources}

    try:
        from open_acp.echo.embeddings import build_index, rank_sources

        index = build_index(sources)
        ranked_keys = rank_sources(question, index, top_k=top_k)
        picked = [by_key[k] for k in ranked_keys if k in by_key]
    except Exception:
        # sentence-transformers missing or model load failed — degrade gracefully.
        picked = _fallback_sources(sources)

    if not picked:
        picked = _fallback_sources(sources)
    return _apply_budget(picked, budget)
