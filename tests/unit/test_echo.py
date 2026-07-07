"""Unit tests for Echo (Ask half). No network — a stub client stands in for the LLM."""

from __future__ import annotations

from open_acp.echo import corpus
from open_acp.echo.ask import ask
from open_acp.echo.retrieve import retrieve


class StubClient:
    """Deterministic stand-in for ClaudeClient. Records prompts it receives."""

    def __init__(self, selection: str = "[]", answer: str = "ANSWER"):
        self.selection = selection
        self.answer = answer
        self.prompts: list[tuple[str, str]] = []

    def active_provider(self) -> str:
        return "stub"

    def generate(self, prompt, system="", model_tier="strong", max_tokens=4096, temperature=0.7):
        self.prompts.append((model_tier, prompt))
        return self.selection if model_tier == "cheap" else self.answer


def test_list_sources_finds_handoff_docs():
    srcs = corpus.list_sources()
    keys = {s.key for s in srcs}
    assert "docs/handoff/README.md" in keys
    # categories are assigned
    cats = {s.category for s in srcs}
    assert {"handoff", "manifest"}.issubset(cats)


def test_small_corpus_skips_selection():
    """If the whole corpus fits the budget, retrieve returns everything with no LLM call."""
    srcs = corpus.list_sources()[:2]
    client = StubClient()
    picked = retrieve("anything", client=client, sources=srcs, budget=10_000_000)
    assert picked == srcs
    assert client.prompts == []  # selection was skipped


def test_large_corpus_uses_selection():
    """When over budget, retrieve calls the cheap tier and honors its picks."""
    srcs = corpus.list_sources()
    assert len(srcs) > 2
    target = srcs[0].key
    client = StubClient(selection=f'["{target}"]')
    picked = retrieve("q", client=client, sources=srcs, budget=1)  # force selection
    assert client.prompts and client.prompts[0][0] == "cheap"
    assert target in {s.key for s in picked}


def test_selection_fallback_on_empty():
    """Empty/garbage selection falls back to handoff+pedagogy docs, not nothing."""
    srcs = corpus.list_sources()
    client = StubClient(selection="not json")
    picked = retrieve("q", client=client, sources=srcs, budget=1)
    assert picked  # fallback produced something
    assert all(s.category in {"handoff", "pedagogy"} for s in picked)


def test_ask_loads_selected_source_into_prompt():
    """End-to-end (stubbed): selected source content reaches the answer prompt."""
    srcs = corpus.list_sources()
    target = next(s for s in srcs if s.key == "docs/handoff/README.md")
    client = StubClient(selection=f'["{target.key}"]', answer="grounded reply")
    result = ask("what is the bootstrap doc?", client=client, sources=srcs)
    assert result.text == "grounded reply"
    assert target in result.cited_sources
    # the answer-tier prompt must contain the source delimiter for the picked file
    answer_prompt = next(p for tier, p in client.prompts if tier == "strong")
    assert f"SOURCE: {target.key}" in answer_prompt


def test_ask_handles_empty_corpus():
    client = StubClient()
    result = ask("q", client=client, sources=[])
    assert "No intelligence sources" in result.text
