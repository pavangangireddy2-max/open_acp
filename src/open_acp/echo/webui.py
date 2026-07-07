"""Echo web UI — a single self-contained page (impeccable, product register).

Design notes (product register: the tool disappears into the task):
- One family (system-ui sans); fixed rem scale; restrained palette + one teal accent.
- Two modes: Ask (streamed grounded answer + citations) and Search (instant passages).
- Skeleton/streaming feedback, not a spinner. Motion is 150-220ms, state-only.
- No build step, no framework: plain HTML/CSS/JS, SSE for streaming.
"""

PAGE = r"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Echo</title>
<style>
:root{
  --bg:#0d1014; --surface:#151a21; --surface-2:#1b222b; --line:#242c37;
  --ink:#e8ecf1; --ink-dim:#9aa5b3; --ink-faint:#6b7482;
  --accent:#3fb6b2; --accent-ink:#052422; --gold:#d9b25b;
  --danger:#e2726e;
  --r:10px; --r-sm:7px;
  --ease:cubic-bezier(.22,1,.36,1);
}
*{box-sizing:border-box}
html,body{margin:0;height:100%}
body{
  background:var(--bg); color:var(--ink);
  font:15px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
  -webkit-font-smoothing:antialiased;
}
.app{max-width:820px;margin:0 auto;min-height:100%;display:flex;flex-direction:column;padding:0 20px}
header{padding:30px 0 18px;border-bottom:1px solid var(--line);position:sticky;top:0;background:linear-gradient(var(--bg) 78%,transparent);z-index:10}
.brand{display:flex;align-items:baseline;gap:11px}
.brand h1{font-size:1.55rem;font-weight:650;letter-spacing:-.02em;margin:0;color:var(--gold)}
.brand .tag{color:var(--ink-faint);font-size:.82rem}
.modes{display:flex;gap:4px;margin-top:16px;background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:4px;width:fit-content}
.modes button{
  appearance:none;border:0;background:transparent;color:var(--ink-dim);
  font:inherit;font-size:.86rem;font-weight:550;padding:6px 15px;border-radius:var(--r-sm);
  cursor:pointer;transition:color .15s var(--ease),background .15s var(--ease)}
.modes button[aria-selected="true"]{background:var(--surface-2);color:var(--ink)}
.modes button:hover:not([aria-selected="true"]){color:var(--ink)}
main{flex:1;padding:22px 0 40px}
form{display:flex;gap:10px;margin-bottom:22px}
.field{flex:1;position:relative}
input{
  width:100%;padding:13px 15px;border-radius:var(--r);border:1px solid var(--line);
  background:var(--surface);color:var(--ink);font:inherit;transition:border-color .15s var(--ease),box-shadow .15s var(--ease)}
input::placeholder{color:var(--ink-faint)}
input:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px color-mix(in oklch,var(--accent) 22%,transparent)}
.go{
  appearance:none;border:0;border-radius:var(--r);background:var(--accent);color:var(--accent-ink);
  font:inherit;font-weight:650;padding:0 22px;cursor:pointer;transition:filter .15s var(--ease),opacity .15s var(--ease)}
.go:hover{filter:brightness(1.08)} .go:active{filter:brightness(.95)}
.go:disabled{opacity:.55;cursor:progress}
/* answer */
.answer{
  background:var(--surface);border:1px solid var(--line);border-radius:var(--r);
  padding:20px 22px;white-space:pre-wrap;line-height:1.68;min-height:56px}
.answer.empty{color:var(--ink-faint);white-space:normal}
.answer .cursor{display:inline-block;width:8px;height:1.05em;vertical-align:-2px;background:var(--accent);
  margin-left:1px;animation:blink 1s steps(2) infinite;border-radius:1px}
@keyframes blink{50%{opacity:0}}
.answer code, .answer .mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.92em}
.cite{color:var(--accent);font-weight:550}
/* sources */
.sources{margin-top:14px}
.sources h3{font-size:.72rem;text-transform:uppercase;letter-spacing:.08em;color:var(--ink-faint);margin:0 0 8px;font-weight:600}
.chip{display:inline-flex;align-items:center;gap:6px;background:var(--surface-2);border:1px solid var(--line);
  color:var(--ink-dim);font-size:.78rem;padding:4px 10px;border-radius:99px;margin:0 6px 6px 0;
  font-family:ui-monospace,Menlo,monospace}
/* search hits */
.hits{display:flex;flex-direction:column;gap:10px}
.hit{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:14px 16px;
  transition:border-color .15s var(--ease)}
.hit:hover{border-color:var(--accent)}
.hit .top{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin-bottom:6px}
.hit .path{font-family:ui-monospace,Menlo,monospace;font-size:.78rem;color:var(--accent);word-break:break-all}
.hit .score{font-size:.72rem;color:var(--ink-faint);white-space:nowrap}
.hit .head{font-size:.82rem;color:var(--ink-dim);margin-bottom:5px}
.hit .snip{font-size:.9rem;color:var(--ink);line-height:1.55}
/* skeleton */
.skeleton{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:20px 22px}
.sk-line{height:12px;border-radius:6px;margin:0 0 12px;
  background:linear-gradient(90deg,var(--surface-2) 25%,var(--line) 50%,var(--surface-2) 75%);
  background-size:200% 100%;animation:shimmer 1.2s linear infinite}
.sk-line:last-child{margin-bottom:0;width:60%}
@keyframes shimmer{to{background-position:-200% 0}}
.meta{margin-top:14px;font-size:.74rem;color:var(--ink-faint)}
.err{color:var(--danger)}
.hidden{display:none}
@media (prefers-reduced-motion:reduce){*{animation-duration:.001ms!important;transition-duration:.001ms!important}}
</style></head>
<body><div class="app">
  <header>
    <div class="brand"><h1>Echo</h1><span class="tag">the intelligence layer, asked</span></div>
    <div class="modes" role="tablist">
      <button id="m-ask" role="tab" aria-selected="true">Ask</button>
      <button id="m-search" role="tab" aria-selected="false">Search</button>
    </div>
  </header>
  <main>
    <form id="f">
      <div class="field"><input id="q" autocomplete="off" autofocus
        placeholder="What is NIAT?"></div>
      <button class="go" id="go" type="submit">Ask</button>
    </form>
    <div id="out"><div class="answer empty">Ask a question — answers are grounded in the repo docs, with citations.</div></div>
  </main>
</div>
<script>
const f=document.getElementById('f'),q=document.getElementById('q'),go=document.getElementById('go'),out=document.getElementById('out');
let mode='ask';
const mAsk=document.getElementById('m-ask'),mSearch=document.getElementById('m-search');
function setMode(m){mode=m;
  mAsk.setAttribute('aria-selected',m==='ask');mSearch.setAttribute('aria-selected',m==='search');
  go.textContent=m==='ask'?'Ask':'Search';
  q.placeholder=m==='ask'?'What is NIAT?':'Find passages, e.g. FIB grading';
  out.innerHTML='<div class="answer empty">'+(m==='ask'
    ?'Ask a question — answers are grounded in the repo docs, with citations.'
    :'Search the corpus — instant passages, no waiting for prose.')+'</div>';
  q.focus();}
mAsk.onclick=()=>setMode('ask'); mSearch.onclick=()=>setMode('search');

function esc(s){return s.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}
function renderCites(t){return esc(t).replace(/\[([^\]]+\.(?:md|yaml|yml|json|txt|csv))\]/g,'<span class="cite">[$1]</span>');}
function skeleton(){return '<div class="skeleton"><div class="sk-line"></div><div class="sk-line"></div><div class="sk-line"></div></div>';}

f.onsubmit=async e=>{e.preventDefault();const question=q.value.trim();if(!question)return;
  go.disabled=true;
  try{ mode==='ask' ? await runAsk(question) : await runSearch(question); }
  finally{ go.disabled=false; }
};

async function runSearch(question){
  out.innerHTML=skeleton();
  const t0=performance.now();
  const r=await fetch('/search',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question})});
  const d=await r.json();const ms=Math.round(performance.now()-t0);
  if(!d.hits||!d.hits.length){out.innerHTML='<div class="answer empty">No passages matched.</div>';return;}
  const hits=d.hits.map(h=>`<div class="hit"><div class="top"><span class="path">${esc(h.source_key)}</span>
    <span class="score">${h.score.toFixed(2)}</span></div>
    ${h.heading?`<div class="head">${esc(h.heading)}</div>`:''}
    <div class="snip">${esc(h.snippet)}</div></div>`).join('');
  out.innerHTML=`<div class="hits">${hits}</div><div class="meta">${d.hits.length} passages · ${ms} ms · no LLM</div>`;
}

async function runAsk(question){
  out.innerHTML='<div class="answer"><span class="cursor"></span></div><div class="sources hidden"></div>';
  const ans=out.querySelector('.answer'),src=out.querySelector('.sources');
  let text='';
  const r=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question})});
  const reader=r.body.getReader();const dec=new TextDecoder();let buf='';
  for(;;){const {value,done}=await reader.read();if(done)break;
    buf+=dec.decode(value,{stream:true});
    let idx;while((idx=buf.indexOf('\n\n'))>=0){
      const raw=buf.slice(0,idx);buf=buf.slice(idx+2);
      if(!raw.startsWith('data: '))continue;
      let ev;try{ev=JSON.parse(raw.slice(6));}catch{continue;}
      if(ev.type==='sources'){
        if(ev.sources&&ev.sources.length){src.classList.remove('hidden');
          src.innerHTML='<h3>Sources</h3>'+ev.sources.map(s=>`<span class="chip">${esc(s)}</span>`).join('');}
      }else if(ev.type==='token'){text+=ev.text;ans.innerHTML=renderCites(text)+'<span class="cursor"></span>';
      }else if(ev.type==='error'){ans.innerHTML='<span class="err">'+esc(ev.text)+'</span>';
      }else if(ev.type==='done'){ans.innerHTML=renderCites(text);}
    }
  }
  if(ans.querySelector('.cursor'))ans.innerHTML=renderCites(text);
}
</script></body></html>"""
