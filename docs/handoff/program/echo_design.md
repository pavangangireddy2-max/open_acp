# Echo — Design Spec (v0)

> **Design doc, not code.** Echo is the standalone Agentic-RAG surface over the intelligence
> layer: ask questions about the handoff docs / Canon today, and (later) weekly-refresh the
> measured layer from the Learning Portal MCP behind an HITL gate. This spec is for review
> before any implementation. See [agent_family_architecture.md](agent_family_architecture.md)
> for where Echo sits in the family.
>
> Last updated: 2026-07-08.

## 1. What Echo is (and is not)

Echo is **the reader/refresher of the intelligence layer** — a surface over Canon + the
`docs/handoff/` corpus. It is **not** Canon (the store) and **not** one of the sense/produce
agents. In the family's grammar it's a writer-agent (refreshes truth from live usage) fronted by
a read-only Q&A UI.

**Two halves, deliberately decoupled:**

| Half | Needs Portal MCP? | v0 status |
|---|---|---|
| **Ask** — answer questions grounded in the handoff docs + manifests | No | **Build now** |
| **Refresh** — weekly ingest portal usage → propose doc updates → HITL → commit | Yes | **Stub the seam now, implement when MCP exists** |

Decision (2026-07-08): v0 built at **`src/open_acp/echo/`**. Retrieval upgraded from
whole-doc-load to **local embeddings** (sentence-transformers `all-MiniLM-L6-v2`, cosine
rank over an in-memory NumPy matrix, disk-cached; no vector DB) after the corpus grew past
the whole-load budget with raw sources added. This removed the LLM selection round-trip.
Added a **search mode** (ranked passages, zero LLM, ~0.4s warm) and **streaming** answers,
and an impeccable-designed web UI (Ask + Search). sentence-transformers is an optional
extra (`.[echo]`); without it Ask still works via a handoff+pedagogy fallback.

## 2. Retrieval: whole-doc into context (no vector DB)

The corpus is small and authoritative, so RAG infra is overkill. Echo's "retrieval" is
**document selection**, not chunk search:

1. **Manifest of sources** — a small registry (`echo/corpus.py`) listing every intelligence
   source with a one-line description and path: the `docs/handoff/*.md` docs,
   `knowledge/analyses/pedagogy/universal_principles.yaml`, `knowledge/manifests/**`, and the
   Central Stack Catalogue. (Descriptions can be lifted from the README index.)
2. **Selection step** — a cheap LLM call (`model_tier="cheap"`) is given the question + the
   source manifest (titles + descriptions only) and returns which sources to load. Falls back to
   "load the README + all `context_*.md`" if uncertain.
3. **Answer step** — load the selected whole files into the context of a `model_tier="strong"`
   call with a system prompt that enforces: answer only from provided sources, cite the file for
   each claim, say "not in the intelligence layer" rather than inventing.

Token budget: even loading every `context_*.md` at once (~250KB ≈ 65K tokens) fits comfortably in
the 1M-context models. So selection is an optimization, not a hard requirement — v0 can start by
loading all `context_*.md` and add selection only if latency/cost warrants.

**Upgrade path:** if Canon/portal data later makes the corpus large, swap the selection step for
real embeddings + vector search behind the same `retrieve(question) -> list[Source]` interface.
Nothing else changes.

## 3. Reuse of existing repo machinery (do not reinvent)

| Need | Use existing |
|---|---|
| LLM calls | `utils/claude.py::ClaudeClient.generate(prompt, system, model_tier, max_tokens, temperature)` — already has OpenRouter/OpenAI/Anthropic provider fallback + tiers. Echo makes **zero** new provider code. |
| HITL gate (Refresh half) | `gates/gate_runner.py::GateRunner.request_approval(gate_type, context) -> GateOutcome`; honors `settings.auto_approve_gates`. Echo's doc-update proposals go through this. |
| Config | `config/settings.py::get_settings()` (pydantic-settings, `.env`). Add Echo keys here if any. |
| Provider | Already OpenRouter-capable (`openrouter_model_strong/cheap`), matching the user's existing key. |

## 4. Module layout (`src/open_acp/echo/`)

```
echo/
  __init__.py
  corpus.py        # Source registry: path + description + loader; enumerates docs/handoff, manifests, yaml
  retrieve.py      # retrieve(question) -> [Source]; v0 = select-then-load (or load-all)
  ask.py           # ask(question) -> Answer{text, cited_sources}; the Q&A entrypoint (read-only)
  ingest.py        # STUB: UsageSource protocol; refresh(usage) -> [DocUpdateProposal]. MCP adapter fills this later.
  refresh.py       # STUB: runs ingest -> proposes doc edits -> GateRunner -> writes -> (caller commits)
  cli.py           # `echo ask "..."`  and later `echo refresh`
```

**The MCP seam** — `ingest.py` defines a `UsageSource` protocol (`fetch_since(date) -> UsageBatch`).
v0 ships two adapters: a `FixtureUsageSource` (reads a local CSV/JSON export the user drops in) and
a `PortalMCPUsageSource` **stub** that raises `NotImplementedError` until the MCP exists. Swapping
one for the other is the entire MCP-integration task later.

## 5. The Refresh loop (designed now, built when MCP lands)

```
UsageSource.fetch_since(last_run)          # portal usage: served/attempts/outcomes, joined by
   │                                        #   session_id/unit_id/question_id + content hash
   ▼
compute measured deltas (append-only,       # empirical difficulty, discrimination, misconception
   with provenance: source + timestamp + N) #   prevalence — NEVER overwrite authored reference facts
   ▼
draft doc-update proposals                  # e.g. "misconception M12 prevalence 4% -> 11% (N=2,310)"
   ▼
GateRunner.request_approval(DOC_REFRESH)    # HITL: human approves/edits/rejects each proposal
   ▼
apply approved edits to the DYNAMIC docs    # learner-behaviour doc + measured sections of question docs
   ▼
caller commits (git)                        # provenance trail = git history + in-doc timestamps
```

**Hard invariants (from the architecture threads):**
- Measured facts **append with provenance**; **authored reference facts and the locked
  non-negotiables** (FIB exact-match, do-not-port defects, Python 3.10, etc.) are **never**
  silently overwritten by Echo.
- The **dynamic docs** Echo may rewrite: `context_learner_behaviour_intelligence.md` (the 5th doc)
  and the *measured* sections of the per-course question docs. It gets rewritten each time a
  focused stack is mined — Echo is the mechanism that keeps it current.
- Every refresh is gated. There is no ungated write path.

## 6. What v0 delivers vs defers

**Build first (Ask, no MCP):** `corpus.py`, `retrieve.py` (load-all or select-then-load),
`ask.py`, `cli.py` → `echo ask "what's the FIB grading rule?"` answers with citations. Immediately
useful; the daily-driver surface over all the handoff work.

**Defer (Refresh, needs MCP):** `ingest.py` real adapter, `refresh.py` wiring. Ship the stubs +
`FixtureUsageSource` so the loop is demonstrable on a manual export, and the MCP adapter is a
drop-in when the portal team ships it.

## 7. Decisions (confirmed 2026-07-08)

1. **Frontend:** v0 ships a **simple web frontend** (ask box + answer with citations), not just a
   CLI. A minimal FastAPI/Flask endpoint wrapping `ask.py` + a single-page UI; the CLI stays as a
   thin alternate entrypoint.
2. **Commit policy:** **write-only.** Echo (Refresh half) writes approved doc edits to the working
   tree; **the human commits.** Echo never runs git.
3. **Corpus scope:** Echo reads **handoff docs + manifests + pedagogy YAML + `docs/architecture/`
   + raw sources** (`knowledge/raw/**` incl. extracted deck text and corpora). The user wants to
   query raw content inside the RAG, so `corpus.py` registers the raw text sources too. Note: raw
   PDFs aren't directly readable as text — Echo indexes the **`extracted_text/` `.txt`** versions
   and CSVs, not the binaries.
4. **Corpus-size consequence:** adding raw extracted text (~24 decks) pushes the corpus well past
   the ~250KB handoff set. Load-all-into-context no longer fits for raw queries → the
   **document-selection step (§2) becomes required, not optional**, for raw-source questions. The
   handoff-only queries can still load all `context_*.md`.

## 8. Pre-req

The ~1,400 lines of uncommitted `src/` engineering (task #6) should be committed/stashed before
Echo lands in `src/open_acp/echo/`, to avoid tangling commits.
```
