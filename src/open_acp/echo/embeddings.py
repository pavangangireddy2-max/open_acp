"""Echo local embeddings — sentence-transformers over the corpus, no vector DB.

Chunks every source into passages, embeds them once with all-MiniLM-L6-v2, and caches
the matrix to disk keyed by a corpus fingerprint. Cosine ranking is plain NumPy — the
corpus is small (a few thousand passages), so an in-memory matrix multiply is <10ms and
a dedicated vector database would be pure overhead.

Used by:
- retrieve.py — rank whole *sources* for the Ask step (no LLM selection call).
- search (cli/web) — rank *passages* for the sub-0.5s, no-LLM search mode.

The model is loaded lazily so importing Echo (and the fast search path) stays cheap
until the first embedding call.
"""

from __future__ import annotations

import hashlib
import pickle
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np

from open_acp.config.curriculum_context import find_project_root
from open_acp.echo.corpus import Source, list_sources, load_source

_MODEL_NAME = "all-MiniLM-L6-v2"
_CACHE_DIR = ".echo_cache"  # under the project root; git-ignored
_CACHE_FILE = "passage_index.pkl"

# Chunk sizing (characters). Small enough to be a citable passage, big enough for context.
_CHUNK_TARGET = 1200
_CHUNK_MAX = 2000


@dataclass(frozen=True)
class Passage:
    """One embeddable chunk of a source."""

    source_key: str  # repo-relative path of the origin file
    ordinal: int  # position within the source
    heading: str  # nearest markdown heading, for display
    text: str


@dataclass
class PassageIndex:
    """Embedded passages + their matrix. Cached to disk."""

    passages: list[Passage]
    matrix: np.ndarray  # shape (n_passages, dim), L2-normalized
    fingerprint: str


# ---- chunking -------------------------------------------------------------------

def _split_markdownish(text: str) -> list[tuple[str, str]]:
    """Split into (heading, body) blocks on markdown headings, then size-bound them."""
    lines = text.splitlines()
    blocks: list[tuple[str, list[str]]] = []
    heading = ""
    buf: list[str] = []
    for line in lines:
        if re.match(r"^#{1,6}\s", line):
            if buf:
                blocks.append((heading, buf))
            heading = line.lstrip("# ").strip()
            buf = []
        else:
            buf.append(line)
    if buf:
        blocks.append((heading, buf))
    if not blocks:  # non-markdown (yaml/csv/txt): one block
        blocks = [("", lines)]

    # Size-bound each block into chunks.
    out: list[tuple[str, str]] = []
    for hd, body_lines in blocks:
        body = "\n".join(body_lines).strip()
        if not body:
            continue
        if len(body) <= _CHUNK_MAX:
            out.append((hd, body))
            continue
        # Greedily pack paragraphs up to the target size.
        para = re.split(r"\n\s*\n", body)
        cur = ""
        for p in para:
            if len(cur) + len(p) > _CHUNK_TARGET and cur:
                out.append((hd, cur.strip()))
                cur = p
            else:
                cur = f"{cur}\n\n{p}" if cur else p
        if cur.strip():
            out.append((hd, cur.strip()))
    return out


def _chunk_source(source: Source) -> list[Passage]:
    text = load_source(source)
    passages: list[Passage] = []
    for i, (heading, body) in enumerate(_split_markdownish(text)):
        passages.append(Passage(source_key=source.key, ordinal=i, heading=heading, text=body))
    return passages


# ---- model + fingerprint --------------------------------------------------------

@lru_cache(maxsize=1)
def _model():
    # Imported lazily: keeps `echo ask`'s import path light and avoids the torch load
    # until an embedding is actually needed.
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(_MODEL_NAME)


def _fingerprint(sources: list[Source]) -> str:
    h = hashlib.sha256()
    h.update(_MODEL_NAME.encode())
    for s in sorted(sources, key=lambda x: x.key):
        try:
            mtime = int(s.path.stat().st_mtime)
            size = s.path.stat().st_size
        except OSError:
            mtime, size = 0, 0
        h.update(f"{s.key}:{size}:{mtime}".encode())
    return h.hexdigest()[:16]


def _embed(texts: list[str]) -> np.ndarray:
    vecs = _model().encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return np.asarray(vecs, dtype=np.float32)


# ---- index build / load ---------------------------------------------------------

def _cache_path(root: Path) -> Path:
    return root / _CACHE_DIR / _CACHE_FILE


def build_index(sources: list[Source] | None = None, root: Path | None = None) -> PassageIndex:
    """Build (and disk-cache) the passage index. Reuses cache when the fingerprint matches."""
    root = root or find_project_root()
    sources = sources if sources is not None else list_sources(root)
    fp = _fingerprint(sources)

    cache = _cache_path(root)
    if cache.exists():
        try:
            with open(cache, "rb") as f:
                cached: PassageIndex = pickle.load(f)
            if cached.fingerprint == fp:
                return cached
        except (pickle.PickleError, OSError, AttributeError):
            pass  # rebuild on any cache problem

    passages: list[Passage] = []
    for src in sources:
        passages.extend(_chunk_source(src))

    matrix = _embed([p.text for p in passages]) if passages else np.zeros((0, 384), dtype=np.float32)
    index = PassageIndex(passages=passages, matrix=matrix, fingerprint=fp)

    cache.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(cache, "wb") as f:
            pickle.dump(index, f)
    except OSError:
        pass  # cache is an optimization; ignore write failures
    return index


# ---- ranking --------------------------------------------------------------------

@dataclass
class ScoredPassage:
    passage: Passage
    score: float


def rank_passages(query: str, index: PassageIndex, top_k: int = 8) -> list[ScoredPassage]:
    """Cosine-rank passages against the query."""
    if not index.passages:
        return []
    q = _embed([query])[0]
    scores = index.matrix @ q  # both normalized → cosine similarity
    order = np.argsort(-scores)[:top_k]
    return [ScoredPassage(passage=index.passages[i], score=float(scores[i])) for i in order]


def rank_sources(query: str, index: PassageIndex, top_k: int = 8) -> list[str]:
    """Rank whole sources by their best-matching passage; returns source keys, best first."""
    if not index.passages:
        return []
    q = _embed([query])[0]
    scores = index.matrix @ q
    best: dict[str, float] = {}
    for passage, score in zip(index.passages, scores):
        if score > best.get(passage.source_key, -1.0):
            best[passage.source_key] = float(score)
    ranked = sorted(best.items(), key=lambda kv: -kv[1])
    return [key for key, _ in ranked[:top_k]]
