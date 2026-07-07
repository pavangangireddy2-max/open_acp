"""Unit tests for Echo. No network — a stub client stands in for the LLM.

Embedding-dependent tests are skipped if sentence-transformers isn't installed.
"""

from __future__ import annotations

import numpy as np
import pytest

from open_acp.echo import corpus
from open_acp.echo.ask import ask
from open_acp.echo.embeddings import PassageIndex, Passage, _split_markdownish

try:
    import sentence_transformers  # noqa: F401
    _HAS_ST = True
except ImportError:
    _HAS_ST = False


class StubClient:
    """Deterministic stand-in for ClaudeClient."""

    def __init__(self, answer: str = "ANSWER"):
        self.answer = answer
        self.prompts: list[tuple[str, str]] = []

    def active_provider(self) -> str:
        return "stub"

    def generate(self, prompt, system="", model_tier="strong", max_tokens=4096, temperature=0.7):
        self.prompts.append((model_tier, prompt))
        return self.answer


def _fake_index(sources) -> PassageIndex:
    """A deterministic PassageIndex without embeddings: one passage per source, unit vectors."""
    passages = [Passage(source_key=s.key, ordinal=0, heading="", text=s.key) for s in sources]
    mat = np.eye(len(passages), dtype=np.float32) if passages else np.zeros((0, 1), dtype=np.float32)
    return PassageIndex(passages=passages, matrix=mat, fingerprint="test")


# ---- corpus ---------------------------------------------------------------------

def test_list_sources_finds_handoff_docs():
    keys = {s.key for s in corpus.list_sources()}
    assert "docs/handoff/README.md" in keys
    cats = {s.category for s in corpus.list_sources()}
    assert {"handoff", "manifest"}.issubset(cats)


# ---- chunking (no model needed) -------------------------------------------------

def test_split_markdownish_splits_on_headings():
    text = "# Title\n\nintro para\n\n## Section A\n\nbody a\n\n## Section B\n\nbody b"
    blocks = _split_markdownish(text)
    headings = [h for h, _ in blocks]
    assert "Title" in headings and "Section A" in headings and "Section B" in headings


def test_split_markdownish_non_markdown_single_block():
    blocks = _split_markdownish("just some plain text\nsecond line")
    assert len(blocks) == 1
    assert blocks[0][0] == ""  # no heading


# ---- retrieve (patched embeddings, no model) ------------------------------------

def test_retrieve_uses_embedding_ranking(monkeypatch):
    import open_acp.echo.embeddings as emb
    srcs = corpus.list_sources()[:5]
    target = srcs[2].key

    monkeypatch.setattr(emb, "build_index", lambda sources=None, root=None: _fake_index(srcs))
    monkeypatch.setattr(emb, "rank_sources", lambda q, index, top_k=8: [target])

    from open_acp.echo.retrieve import retrieve
    picked = retrieve("anything", sources=srcs)
    assert target in {s.key for s in picked}


def test_retrieve_falls_back_when_embeddings_unavailable(monkeypatch):
    import open_acp.echo.embeddings as emb

    def boom(*a, **k):
        raise RuntimeError("no model")

    monkeypatch.setattr(emb, "build_index", boom)
    srcs = corpus.list_sources()
    from open_acp.echo.retrieve import retrieve
    picked = retrieve("q", sources=srcs)
    assert picked  # fell back, not empty
    assert all(s.category in {"handoff", "pedagogy"} for s in picked)


# ---- ask ------------------------------------------------------------------------

def test_ask_loads_selected_source_into_prompt(monkeypatch):
    import importlib
    ask_module = importlib.import_module("open_acp.echo.ask")
    srcs = corpus.list_sources()
    target = next(s for s in srcs if s.key == "docs/handoff/README.md")
    monkeypatch.setattr(ask_module, "retrieve", lambda q, client=None, sources=None: [target])

    client = StubClient(answer="grounded reply")
    result = ask("what is the bootstrap doc?", client=client, sources=srcs)
    assert result.text == "grounded reply"
    assert target in result.cited_sources
    answer_prompt = client.prompts[0][1]
    assert f"SOURCE: {target.key}" in answer_prompt


def test_ask_handles_empty_selection(monkeypatch):
    import importlib
    ask_module = importlib.import_module("open_acp.echo.ask")
    monkeypatch.setattr(ask_module, "retrieve", lambda q, client=None, sources=None: [])
    result = ask("q", client=StubClient(), sources=[])
    assert "No intelligence sources" in result.text


# ---- search (requires the real model) -------------------------------------------

@pytest.mark.skipif(not _HAS_ST, reason="sentence-transformers not installed")
def test_search_returns_ranked_hits():
    from open_acp.echo.search import search
    hits = search("What is NIAT?", top_k=3)
    assert hits
    assert hits[0].score >= hits[-1].score  # sorted
    assert hits[0].source_key and hits[0].snippet
