"""Echo CLI + web server.

  echo ask "your question"     # answer in the terminal
  echo serve                   # launch the simple web frontend

Registered as the `echo` console script. The web server uses only the stdlib
(http.server), so Echo adds no new dependencies.
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from open_acp.echo.ask import ask as ask_echo

app = typer.Typer(name="echo", help="Ask questions about the Open ACP intelligence layer.", no_args_is_help=True)
console = Console()


@app.command()
def ask(question: str = typer.Argument(..., help="The question to answer from the docs.")) -> None:
    """Answer a question grounded in the intelligence corpus, with citations."""
    with console.status("[bold]Echo is thinking..."):
        answer = ask_echo(question)
    console.print(Panel(Markdown(answer.text), title="Echo", border_style="cyan"))
    console.print(Panel(answer.format_sources(), title="Sources", border_style="dim"))
    console.print(f"[dim]provider: {answer.provider}[/dim]")


_PAGE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Echo</title>
<style>
  :root { --bg:#0f1115; --card:#1a1d24; --gold:#d4af37; --teal:#3fb6b2; --tx:#e6e6e6; --dim:#8a8f98; }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--tx); font:16px/1.6 -apple-system,Segoe UI,Roboto,sans-serif; }
  .wrap { max-width:820px; margin:0 auto; padding:40px 20px; }
  h1 { color:var(--gold); font-weight:600; letter-spacing:.5px; margin:0 0 4px; }
  .sub { color:var(--dim); margin:0 0 28px; }
  form { display:flex; gap:10px; margin-bottom:24px; }
  input { flex:1; padding:12px 14px; border-radius:8px; border:1px solid #333; background:var(--card); color:var(--tx); font-size:16px; }
  button { padding:12px 20px; border-radius:8px; border:0; background:var(--teal); color:#06201f; font-weight:600; cursor:pointer; }
  button:disabled { opacity:.5; cursor:wait; }
  .answer { background:var(--card); border:1px solid #2a2e37; border-radius:10px; padding:20px; white-space:pre-wrap; }
  .sources { margin-top:16px; color:var(--dim); font-size:14px; }
  .sources b { color:var(--tx); }
  .empty { color:var(--dim); }
</style></head>
<body><div class="wrap">
  <h1>Echo</h1>
  <p class="sub">Ask the Open ACP intelligence layer. Answers are grounded in the repo docs, with citations.</p>
  <form id="f"><input id="q" placeholder="e.g. What is the FIB grading rule?" autofocus autocomplete="off">
  <button id="b" type="submit">Ask</button></form>
  <div id="out" class="answer empty">Ask a question to begin.</div>
  <div id="src" class="sources"></div>
</div>
<script>
const f=document.getElementById('f'),q=document.getElementById('q'),b=document.getElementById('b'),
out=document.getElementById('out'),src=document.getElementById('src');
f.onsubmit=async(e)=>{e.preventDefault();const question=q.value.trim();if(!question)return;
b.disabled=true;out.className='answer';out.textContent='Thinking...';src.textContent='';
try{const r=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question})});
const d=await r.json();out.textContent=d.text||'(no answer)';
src.innerHTML=d.sources&&d.sources.length?'<b>Sources:</b><br>'+d.sources.map(s=>'&bull; '+s).join('<br>'):'';
}catch(err){out.textContent='Error: '+err;}finally{b.disabled=false;}};
</script></body></html>"""


def _make_handler():
    class Handler(BaseHTTPRequestHandler):
        def _send(self, code: int, body: bytes, ctype: str) -> None:
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:  # noqa: N802
            if self.path in ("/", "/index.html"):
                self._send(200, _PAGE.encode("utf-8"), "text/html; charset=utf-8")
            else:
                self._send(404, b"not found", "text/plain")

        def do_POST(self) -> None:  # noqa: N802
            if self.path != "/ask":
                self._send(404, b"not found", "text/plain")
                return
            length = int(self.headers.get("Content-Length", 0))
            try:
                payload = json.loads(self.rfile.read(length) or b"{}")
                question = (payload.get("question") or "").strip()
            except (ValueError, TypeError):
                self._send(400, b'{"text":"bad request"}', "application/json")
                return
            if not question:
                self._send(400, b'{"text":"empty question"}', "application/json")
                return
            try:
                answer = ask_echo(question)
                body = json.dumps({"text": answer.text, "sources": [s.key for s in answer.cited_sources]})
            except Exception as exc:  # surface errors to the UI instead of 500-crashing
                body = json.dumps({"text": f"Echo error: {exc}", "sources": []})
            self._send(200, body.encode("utf-8"), "application/json")

        def log_message(self, *args) -> None:  # quiet the default request logging
            return

    return Handler


@app.command()
def serve(host: str = "127.0.0.1", port: int = 8000) -> None:
    """Launch the simple web frontend."""
    server = ThreadingHTTPServer((host, port), _make_handler())
    console.print(f"[cyan]Echo[/cyan] serving at [bold]http://{host}:{port}[/bold]  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        console.print("\n[dim]Echo stopped.[/dim]")
        server.server_close()


if __name__ == "__main__":
    app()
