"""Echo Ask — grounded question answering over the intelligence corpus.

Read-only. Selects relevant sources (retrieve), loads them whole into context, and
asks a strong-tier model to answer using ONLY those sources, with citations.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from open_acp.echo.corpus import Source, load_source
from open_acp.echo.retrieve import retrieve
from open_acp.utils.claude import ClaudeClient

_ANSWER_SYSTEM = (
    "You are Echo, the question-answering surface over NxtWave's Open ACP intelligence "
    "layer. Answer the user's question using ONLY the provided source documents. "
    "Rules:\n"
    "- Ground every claim in the sources. Cite the source file path in brackets, e.g. "
    "[docs/handoff/context_products_all.md], next to the claim it supports.\n"
    "- If the answer is not in the provided sources, say so plainly: 'That is not in the "
    "intelligence layer.' Do not invent facts or use outside knowledge.\n"
    "- Be concise and direct. Prefer the source's own terminology.\n"
    "- If sources conflict, surface the conflict rather than picking silently."
)


@dataclass
class Answer:
    """Result of an Echo query."""

    text: str
    cited_sources: list[Source] = field(default_factory=list)
    provider: str = ""

    def format_sources(self) -> str:
        if not self.cited_sources:
            return "(no sources loaded)"
        return "\n".join(f"- {s.key}" for s in self.cited_sources)


def _build_context(sources: list[Source]) -> str:
    """Concatenate whole source files with clear delimiters for the model."""
    blocks = []
    for src in sources:
        body = load_source(src)
        blocks.append(
            f"===== SOURCE: {src.key} =====\n{body}\n===== END SOURCE: {src.key} ====="
        )
    return "\n\n".join(blocks)


def ask(
    question: str,
    *,
    client: ClaudeClient | None = None,
    sources: list[Source] | None = None,
) -> Answer:
    """Answer ``question`` grounded in the intelligence corpus."""
    client = client or ClaudeClient()
    selected = retrieve(question, client=client, sources=sources)

    if not selected:
        return Answer(
            text="No intelligence sources are available to answer from.",
            cited_sources=[],
            provider=client.active_provider(),
        )

    context = _build_context(selected)
    prompt = (
        f"{context}\n\n"
        f"=====\nQuestion: {question}\n\n"
        "Answer using only the sources above, with bracketed [path] citations."
    )
    text = client.generate(
        prompt=prompt,
        system=_ANSWER_SYSTEM,
        model_tier="strong",
        max_tokens=4096,
        temperature=0.2,
    )
    return Answer(text=text, cited_sources=selected, provider=client.active_provider())
