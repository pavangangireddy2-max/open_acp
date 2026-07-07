"""Echo CLI + web server.

  echo ask "your question"     # streamed grounded answer in the terminal
  echo search "your query"     # instant ranked passages, no LLM
  echo serve                   # launch the web frontend (Ask + Search)

Registered as the `echo` console script. The web server uses only the stdlib.
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from open_acp.echo.ask import ask as ask_echo
from open_acp.echo.ask import ask_stream
from open_acp.echo.search import search as search_echo
from open_acp.echo.webui import PAGE

app = typer.Typer(name="echo", help="Ask the Open ACP intelligence layer.", no_args_is_help=True)
console = Console()


@app.command()
def ask(question: str = typer.Argument(..., help="Question to answer from the docs.")) -> None:
    """Answer a question grounded in the intelligence corpus, with citations."""
    with console.status("[bold]Echo is thinking..."):
        answer = ask_echo(question)
    console.print(Panel(Markdown(answer.text), title="Echo", border_style="cyan"))
    console.print(Panel(answer.format_sources(), title="Sources", border_style="dim"))
    console.print(f"[dim]provider: {answer.provider}[/dim]")


@app.command()
def search(
    query: str = typer.Argument(..., help="Find relevant passages (no LLM)."),
    top_k: int = typer.Option(8, help="Number of passages to return."),
) -> None:
    """Instant passage search over the corpus — embedding similarity, no LLM."""
    with console.status("[bold]Searching..."):
        hits = search_echo(query, top_k=top_k)
    if not hits:
        console.print("[dim]No passages matched.[/dim]")
        return
    for h in hits:
        head = f" · {h.heading}" if h.heading else ""
        console.print(Panel(h.snippet, title=f"{h.source_key}{head}  [{h.score:.2f}]", border_style="cyan"))


def _make_handler():
    class Handler(BaseHTTPRequestHandler):
        def _send(self, code: int, body: bytes, ctype: str) -> None:
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _read_json(self) -> dict:
            length = int(self.headers.get("Content-Length", 0))
            try:
                return json.loads(self.rfile.read(length) or b"{}")
            except (ValueError, TypeError):
                return {}

        def do_GET(self) -> None:  # noqa: N802
            if self.path in ("/", "/index.html"):
                self._send(200, PAGE.encode("utf-8"), "text/html; charset=utf-8")
            else:
                self._send(404, b"not found", "text/plain")

        def do_POST(self) -> None:  # noqa: N802
            if self.path == "/search":
                self._handle_search()
            elif self.path == "/ask":
                self._handle_ask_stream()
            else:
                self._send(404, b"not found", "text/plain")

        def _handle_search(self) -> None:
            question = (self._read_json().get("question") or "").strip()
            if not question:
                self._send(400, b'{"hits":[]}', "application/json")
                return
            try:
                hits = search_echo(question)
                body = json.dumps({"hits": [
                    {"source_key": h.source_key, "heading": h.heading, "score": h.score, "snippet": h.snippet}
                    for h in hits
                ]})
            except Exception as exc:
                body = json.dumps({"hits": [], "error": str(exc)})
            self._send(200, body.encode("utf-8"), "application/json")

        def _handle_ask_stream(self) -> None:
            question = (self._read_json().get("question") or "").strip()
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            try:
                for event in ask_stream(question):
                    self.wfile.write(f"data: {json.dumps(event)}\n\n".encode("utf-8"))
                    self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                pass  # client navigated away mid-stream
            except Exception as exc:
                try:
                    self.wfile.write(f'data: {json.dumps({"type": "error", "text": str(exc)})}\n\n'.encode("utf-8"))
                except OSError:
                    pass

        def log_message(self, *args) -> None:
            return

    return Handler


@app.command()
def serve(host: str = "127.0.0.1", port: int = 8000, warm: bool = True) -> None:
    """Launch the Echo web frontend (Ask + Search)."""
    if warm:
        # Build the index AND run one real query so the encoder is fully loaded — otherwise
        # the first user query pays the model-load cost (~10s). After this, search is <0.5s.
        with console.status("[bold]Warming Echo (embedding index + model)..."):
            try:
                from open_acp.echo.embeddings import build_index
                from open_acp.echo.search import search as _s
                idx = build_index()
                _s("warmup", top_k=1)  # forces the encoder to load now
                console.print(f"[dim]index ready: {len(idx.passages)} passages, model warm[/dim]")
            except Exception as exc:
                console.print(f"[yellow]warmup skipped: {exc}[/yellow]")
    server = ThreadingHTTPServer((host, port), _make_handler())
    console.print(f"[cyan]Echo[/cyan] serving at [bold]http://{host}:{port}[/bold]  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        console.print("\n[dim]Echo stopped.[/dim]")
        server.server_close()


if __name__ == "__main__":
    app()
