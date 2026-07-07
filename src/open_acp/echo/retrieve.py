"""Echo retrieval — document selection (not chunk search).

The corpus now includes raw extracted text, which is far larger than the handoff set,
so we can't blindly load everything. ``retrieve`` asks a cheap-tier model which sources
are relevant to the question, then returns those (bounded by a token budget). If the
selection step fails or the corpus is small enough, it falls back to loading the handoff
+ pedagogy docs, which answer the large majority of questions.

Interface is stable — ``retrieve(question) -> list[Source]`` — so a future embeddings /
vector-store implementation can drop in without changing ask.py.
"""

from __future__ import annotations

import json
import re

from open_acp.echo.corpus import Source, list_sources, manifest_lines
from open_acp.utils.claude import ClaudeClient

# Token ceiling for the set of docs handed to the answer step. Well under the 1M window,
# but keeps latency/cost sane and avoids dumping the entire raw corpus into one call.
_SELECTION_TOKEN_BUDGET = 200_000

_SELECTION_SYSTEM = (
    "You select which knowledge-base files are needed to answer a question. "
    "You are given a question and a manifest of files (path + description). "
    "Return ONLY a JSON array of the exact file paths (the string after the category "
    "tag) that are relevant. Prefer precision: pick the few files most likely to contain "
    "the answer, not everything plausibly related. Return [] if none seem relevant."
)


def _fallback_sources(sources: list[Source]) -> list[Source]:
    """Default set when selection is unavailable: handoff + pedagogy docs."""
    picked = [s for s in sources if s.category in {"handoff", "pedagogy"}]
    return picked or sources


def _parse_selection(raw: str, by_key: dict[str, Source]) -> list[Source]:
    """Pull a JSON array of paths out of the model reply and map to sources."""
    match = re.search(r"\[.*\]", raw, re.DOTALL)
    if not match:
        return []
    try:
        keys = json.loads(match.group(0))
    except (ValueError, TypeError):
        return []
    picked: list[Source] = []
    for key in keys:
        if isinstance(key, str) and key in by_key:
            picked.append(by_key[key])
    return picked


def _apply_budget(sources: list[Source], budget: int) -> list[Source]:
    """Keep sources until the token budget is exhausted (order preserved)."""
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
    client: ClaudeClient | None = None,
    sources: list[Source] | None = None,
    budget: int = _SELECTION_TOKEN_BUDGET,
) -> list[Source]:
    """Return the sources relevant to ``question``, bounded by a token budget."""
    sources = sources if sources is not None else list_sources()
    if not sources:
        return []

    by_key = {s.key: s for s in sources}

    # If the whole corpus fits the budget, skip the selection call entirely.
    if sum(s.approx_tokens for s in sources) <= budget:
        return sources

    client = client or ClaudeClient()
    prompt = (
        f"Question:\n{question}\n\n"
        f"Available files:\n{manifest_lines(sources)}\n\n"
        "Return the JSON array of relevant file paths."
    )
    try:
        raw = client.generate(
            prompt=prompt,
            system=_SELECTION_SYSTEM,
            model_tier="cheap",
            max_tokens=1024,
            temperature=0.0,
        )
    except Exception:
        return _apply_budget(_fallback_sources(sources), budget)

    picked = _parse_selection(raw, by_key)
    if not picked:
        picked = _fallback_sources(sources)
    return _apply_budget(picked, budget)
