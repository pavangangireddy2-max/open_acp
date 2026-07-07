"""Echo Ask — grounded question answering over the intelligence corpus.

Read-only. Selects relevant sources (retrieve), loads them whole into context, and
asks a model to answer using ONLY those sources, with citations. Supports streaming
(``ask_stream``) so the web UI shows tokens as they arrive.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import dataclass, field

import httpx

from open_acp.config.settings import get_settings
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


def _prepare(question: str, client: ClaudeClient, sources: list[Source] | None):
    """Shared retrieval + prompt assembly for ask / ask_stream."""
    selected = retrieve(question, client=client, sources=sources)
    if not selected:
        return None, ""
    context = _build_context(selected)
    prompt = (
        f"{context}\n\n"
        f"=====\nQuestion: {question}\n\n"
        "Answer using only the sources above, with bracketed [path] citations."
    )
    return selected, prompt


def ask(
    question: str,
    *,
    client: ClaudeClient | None = None,
    sources: list[Source] | None = None,
    model_tier: str = "cheap",
) -> Answer:
    """Answer ``question`` grounded in the intelligence corpus.

    ``model_tier`` defaults to "cheap" (fast, ample for grounded reading); pass "strong"
    for questions needing deeper synthesis at the cost of latency.
    """
    client = client or ClaudeClient()
    selected, prompt = _prepare(question, client, sources)
    if selected is None:
        return Answer(
            text="No intelligence sources are available to answer from.",
            cited_sources=[],
            provider=client.active_provider(),
        )
    # Cheap tier is used for the answer: the task is reading-comprehension over provided
    # sources (not open-ended reasoning), and the strong model is ~15x slower here for no
    # quality gain. Override to "strong" per-call if a question ever needs deeper synthesis.
    text = client.generate(
        prompt=prompt,
        system=_ANSWER_SYSTEM,
        model_tier=model_tier,
        max_tokens=4096,
        temperature=0.2,
    )
    return Answer(text=text, cited_sources=selected, provider=client.active_provider())


def ask_stream(
    question: str,
    *,
    client: ClaudeClient | None = None,
    sources: list[Source] | None = None,
    model_tier: str = "cheap",
) -> Iterator[dict]:
    """Stream an answer. Yields dict events:

    - {"type": "sources", "sources": [keys]}   once, before generation
    - {"type": "token", "text": "..."}         many, as tokens arrive
    - {"type": "done"} or {"type": "error", "text": "..."}

    Reuses ClaudeClient's resolved provider/keys/models but calls the chat endpoint with
    stream=true. Only the OpenAI-compatible providers (openai/openrouter) stream here;
    other providers fall back to a single non-streamed token event.
    """
    client = client or ClaudeClient()
    selected, prompt = _prepare(question, client, sources)
    if selected is None:
        yield {"type": "sources", "sources": []}
        yield {"type": "token", "text": "No intelligence sources are available to answer from."}
        yield {"type": "done"}
        return

    yield {"type": "sources", "sources": [s.key for s in selected]}

    provider = client.active_provider()
    settings = get_settings()
    try:
        if provider == "openrouter":
            base = settings.openrouter_base_url.rstrip("/")
            key = settings.openrouter_api_key
            model = client.openrouter_model_cheap if model_tier == "cheap" else client.openrouter_model_strong
        elif provider == "openai":
            base = settings.openai_base_url.rstrip("/")
            key = settings.openai_api_key
            model = client.openai_model_cheap if model_tier == "cheap" else client.openai_model_strong
        else:
            # Non-streaming provider: emit the whole answer as one token event.
            text = client.generate(
                prompt=prompt, system=_ANSWER_SYSTEM, model_tier=model_tier,
                max_tokens=4096, temperature=0.2,
            )
            yield {"type": "token", "text": text}
            yield {"type": "done"}
            return

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": _ANSWER_SYSTEM},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 4096,
            "stream": True,
        }
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json", "X-Title": "open_acp-echo"}
        with httpx.Client(timeout=120.0) as http:
            with http.stream("POST", f"{base}/chat/completions", headers=headers, json=payload) as resp:
                if resp.is_error:
                    resp.read()
                    yield {"type": "error", "text": f"provider error {resp.status_code}"}
                    return
                for line in resp.iter_lines():
                    if not line or not line.startswith("data: "):
                        continue
                    data = line[len("data: "):]
                    if data.strip() == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data)
                        delta = chunk["choices"][0]["delta"].get("content")
                    except (ValueError, KeyError, IndexError):
                        continue
                    if delta:
                        yield {"type": "token", "text": delta}
        yield {"type": "done"}
    except Exception as exc:  # surface to UI instead of dropping the stream
        yield {"type": "error", "text": f"Echo error: {exc}"}
