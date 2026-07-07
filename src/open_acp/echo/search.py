"""Echo search mode — sub-0.5s passage retrieval with zero LLM calls.

Returns ranked source passages by embedding similarity. This is the search-engine feel:
type a query, get the relevant passages instantly, no answer generation. Useful when you
want to *find where something is said* rather than have it summarized.
"""

from __future__ import annotations

from dataclasses import dataclass

from open_acp.echo.corpus import Source, list_sources
from open_acp.echo.embeddings import ScoredPassage, build_index, rank_passages


@dataclass
class SearchHit:
    source_key: str
    heading: str
    score: float
    snippet: str


def _snippet(text: str, limit: int = 320) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[:limit].rstrip() + "…"


def search(query: str, *, sources: list[Source] | None = None, top_k: int = 8) -> list[SearchHit]:
    """Return the top passages for ``query`` — no LLM, just embedding cosine ranking."""
    sources = sources if sources is not None else list_sources()
    index = build_index(sources)
    scored: list[ScoredPassage] = rank_passages(query, index, top_k=top_k)
    return [
        SearchHit(
            source_key=sp.passage.source_key,
            heading=sp.passage.heading,
            score=sp.score,
            snippet=_snippet(sp.passage.text),
        )
        for sp in scored
    ]
