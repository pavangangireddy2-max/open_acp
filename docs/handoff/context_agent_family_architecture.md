# The Agent Family — System Architecture (Context Map)

> **Standalone handoff document.** Reconstructed from nine claude.ai design threads
> (Jun–Jul 2026) that predate this repo's handoff docs. This is the *system map*: the full
> cast of agents NxtWave (NIAT / Open ACP) is building, what each does, how they connect, and
> where the intelligence docs in this folder plug in. Every other doc in `docs/handoff/` is a
> component spec; this is the whole circuit.
>
> Design language across all threads: "Neo Kinpaku" (gold = authored/canonical source,
> patina/teal = live/moving, neutral = readers). Naming convention: **every agent is one real
> word with one precise function.**
>
> Last updated: 2026-07-08.

---

## The one-line circuit

```
Radar + Panel + Lens(cohort) + Loop(RCA) → Prism → Docket → Relay → Forge / slides / TR Docs
   → Canon ↔ Learning Portal (MCP) → students → Lens(per-student) → Crux → back to student
```

Sense → Decide → Produce → Truth → Deliver → Advise, with **Oversee** (Loop) as a rail
beneath, and the whole thing loops.

---

## The cast (10 agents + 2 commons)

### Commons (not agents — shared infrastructure)

- **Canon** — the authoritative, ID-addressed knowledge base. The single source of record every
  agent reads. Four layers, coarse → fine:
  - **Catalog** — domain → course list, Course IDs, prerequisites, the GRIT-skill bridge,
    Course Levels, Roles mapping (Track/Badge/Role/Package). ("Stack KB")
  - **Contents** — a course unpacked: modules, sessions (Session IDs), key takeaways, outline,
    source corpus. ("Packaged Courses KB")
  - **Graph** — the atomic layer: key-takeaway **nodes**, L1–L5 mastery levels, `Depends_On`
    edges, evidence assets tagged by node/level/role. ("Mastery Linkage KB")
  - **Manifests** — product families (NIAT/Academy/Intensive/GRIT/Launchpad/default), versions,
    batches, structure profiles, packaging profiles, feature flags, delivery modes. Holds the
    **resolver**: `stack × product × version → composed "cut"` (deep-merge over `default.yaml`,
    exactly `curriculum_context.py`).
  - ID thread through everything: `COURSE_ID → SESSION_ID → NODE_ID → ASSET_ID`.
- **Learning Portal** — the delivery surface where students consume content and where activity
  telemetry originates. Connected via the **Portal MCP** (to be built). Canon ↔ Portal stay
  mirrored through it.

### The three human planes + one instrument (how to communicate the family)

| Plane | Human at the counter | Agents |
|---|---|---|
| **Studio** | Content Dept members | Radar · Panel · Prism · Docket · Relay · Forge |
| **Classroom** | The learner | Crux (surfaces through the Portal) |
| **Bridge** | HOD · founder · ops | Loop |
| **Instrument** | *no one* | **Lens** (the only agent no human ever meets) |

*(Plane = named by who consumes the output, not what the output is. Studio agents are batch,
async, human-gated, allowed to be slow. Crux is the lone always-on, low-latency, ungated agent.)*

### Sense layer — four streams, each diffs its signal against Canon → emits a **gap**

Every gap has one shape: `(Canon anchor or missing anchor, evidence, source, severity)`.

1. **Radar** — *market intelligence.* Sweeps stack versions, API/syntax drift, tooling trends
   against Canon; emits version tickets (V-xxx) + content tickets (C-xxx) with rubric scores.
   Reads Catalog + Contents. *(Prototype built: the Market Intelligence Gap Analyzer — version
   audit + per-concept content audit against live docs, rubric 1–5, tickets, golden-dataset eval.)*
2. **Panel** — *interview intelligence.* Reads what interview panels ask per stack/role/round;
   diffs opportunity-weightage against Canon nodes/levels; finds missing + under-leveled nodes
   ("taught at L2, interviews demand L4"). Reads Catalog + Graph. *(= the Intensive Offline
   methodology, made a standing agent.)*
3. **Lens (cohort grain)** — *learner intelligence.* Aggregate per-student telemetry across a
   cohort → node-level failure patterns. Not a new agent — a roll-up view of Lens.
4. **Loop (RCA output)** — *reactive.* When an RCA lands on a curriculum cause, it routes into
   Prism rather than being fixed directly, so every curriculum change passes one gate.

### Converge → Decide

5. **Prism** — the insight engine ("Insight Creator"). Merges/dedupes gaps from all four
   streams (a gap seen by two streams outranks one seen alone), refracts each into one of two
   bands: **What to teach** (mutations to Canon's Graph — new/re-leveled/retired nodes, new
   courses) vs **How to teach** (mutations to delivery — session design, slides, analogies,
   practice mix). *What changes Canon vs How changes assets.* **Prism is product-blind** —
   insights land on the stack.
6. **Docket** — the implementation planner ("MOM loader"). Reads each approved insight against
   Canon, writes the implementation plan (scoped work items, sequence, owner-type, due window).
   **Docket owns the product fan-out**: for each insight it walks Manifests for every product ×
   version packaging the touched stack and returns a verdict per product — **Adopt · Adapt ·
   Fork variant · Defer/Skip**. Work items exit product-qualified. Human sign-off → hands to Relay.

### Produce

7. **Relay** — content production pipeline. Assigns owners, runs HITL gates. Fires the builders:
   **Forge** (practice units), slides workflow, TR Docs. **Relay pushes finished content to the
   Learning Portal AND syncs content metadata back into Canon over the portal MCP.** The one
   writer (with Forge) into Canon — through gates. Truth flows one way; scouts read, never write.
8. **Forge** — practice-unit builder. Per session, writes a **complete fresh** objective bank +
   coding bank, **born-tagged** to `node × level × axis`, human-reviewed, published as `active`
   while the previous unit is `archived` (never hard-deleted — keeps calibration/rollback).
   Ships coding items with test harnesses. Uses a **per-module DSPy program** that improves from
   reviewer edits (reviewer's final = gold demo). *This repo's question-intelligence + node-registry
   docs are Forge's HOW rail and WHAT rail.*

### Deliver + Advise (Classroom)

9. **Lens** — perception layer. Watches each student (engagement, behaviour), pulls performance +
   program-ops, resolves it all down to Canon node IDs, tags telemetry with the student's **cut**,
   hands Crux a diagnosis-ready per-student × per-node view. Its consumers are Crux and Prism —
   no human. Loop's program-ops output is one of Lens's inputs (same telemetry, opposite zoom).
10. **Crux** — mastery brain + student copilot. Key-takeaway nodes are the only ground truth;
    NSPI/readiness/root-cause/suggestions are derived. Walks the dependency graph to find the
    real gap below a failure, names the next move. **Arrives ~50% into a course, not day 1** —
    early delivery uses simple baked-in adaptive logic. *(Compass = the adaptive practice-delivery
    runtime that sits in front of Crux's scoring; deterministic engine, ~0 LLM cost at runtime.)*

### Oversee (Bridge)

- **Loop** — RCA → resolution pipeline (reactive) evolving into **Learning Intelligence**. Six
  stages: intake → draft RCA → **HITL gate** → group & route → generate tasks → track & resolve.
  Cross-stream items **route only** (suggested direction to the owning HOD, no task). Issue
  resolution ETA = MAX(task due dates). Adding proactive channels: **D3a** Learner Voice (R),
  **D3b** Learner Behaviour (P), **D4** Student Performance (P), **D5** Degree/Higher-Ed (R+P).
  Reactive + proactive converge on the shared RCA/theme core.

---

## Key locked concepts (cross-thread)

- **Nodes are product-agnostic; packaging is product-shaped.** A node is the same node in any
  product; only cadence/evidence-opportunities differ. Mastery lives on stack nodes → Crux is
  product-untouched. Lens normalizes product-shaped telemetry back to stack nodes.
- **The "cut"** = `stack × product × version` composed object = packaging profile + composition
  map. Three shaping levels: **Repack** (cadence/hours, structure untouched), **Recut**
  (include/exclude/insert modules & sessions — single-sourced in Contents, never copied), **Fork**
  (content diverges — new Contents branch). Cuts must be **dependency-closed** (removing a module
  can't orphan a kept node's prereq) and Crux's coverage **denominators go cut-relative**.
- **GRIT is the external north-star.** Shadow ladder: `GRIT Skill Level ← Course Quiz ← Skill
  Assessments ← Module Quiz ← Classroom Quiz ← adaptive practice`. Same gold band top-to-bottom
  (e.g. 85–100). The integrity risk is **shadow fidelity**: if internal gold doesn't predict GRIT
  gold, the shadow is broken. GRIT being external is what makes "prepare everyone to clear it at
  gold" legitimate rather than gaming.
- **Practice vs quiz firewall.** Generated practice is reps, never proof (Crux rule E4). Practice
  bank and quiz bank must be different items, same node/level/role tags.
- **Born-tagged, never retrofit.** Items are generated to fill a `node × level × axis` cell (the
  tag is an input coordinate), so the untagged legacy corpus never needs classifying. WHAT rail
  (node registry, authored fresh from course content — the React exemplar schema) and HOW rail
  (mined from the corpus) have opposite provenance.
- **Two taxonomies per bank, one node list.** Objective and coding banks get separate
  levels/axes/formats but share one node registry (per-node evidence flags: objective-only /
  coding-only / both), so mastery aggregates.
- **Cost at scale (28k students):** runtime is almost all deterministic (selection = lookup,
  grading = key-match / run-tests, mastery = streak rule). LLM cost only touches feedback —
  pre-authored default, opt-in live help. Sandbox fleet (sized by peak concurrency, not headcount)
  is the real recurring bill.
- **Session `skill.md`** — Anthropic-style skill file per session: machine-readable frontmatter
  (node refs + target levels, mastery rules, caps, Forge pool pointer, packaging) + prose body
  (teaching order, feedback tone). **Gate mastery on structured fields, never on prose parsing.**

---

## Where this repo's docs plug in

| This repo | Role in the family |
|---|---|
| `context_products_all.md` | Canon's **Manifests** layer (product cuts, resolution semantics) |
| `context_pedagogy_intelligence.md` + `universal_principles.yaml` | The **How-to-teach** knowledge; Prism's "how" band + Relay/slides generation grounding; a pedagogy *linter* + judge is the eventual build |
| `context_question_intelligence_python.md` | **Forge's HOW rail** (item craft, misconceptions, gates, formats) |
| node registry (WHAT rail, pending) | **Forge's WHAT rail** + Canon Graph authoring |
| `context_platform_student_experience.md` | Portal behaviour contracts (grading, completion) that Forge/Compass/Crux honor |
| `data_request_learner_behaviour_intelligence.md` | The **Lens/Loop** telemetry spec (D3b/D4/D5) — effectively the Portal MCP extract contract |
| `review_adaptive_coding_prd.md` + `proposal_forge_review_and_adaptive_experience.md` | **Compass/Crux** adaptive delivery design |

---

## Open architectural threads (from the design conversations)

- **Portal MCP** must be built (read-only usage extract first; content-push is a separate,
  gated, later capability — see Loop C note below).
- **Weekly self-updating intelligence loop** — a standalone Agentic RAG app that reads the Portal
  MCP weekly and refreshes the measured/learner-behaviour layer, regenerating affected docs
  behind a human gate. Requires the structured-vs-narrative split (facts in YAML/JSON/db,
  append-only with provenance; prose docs generated *from* facts). Never silently overwrite the
  locked non-negotiables or authored reference facts.
- **Loop C** (this repo's LangGraph loops) is a natural home for the content-production execution
  (Relay/Forge fan-out); the intelligence layer feeds it what to produce.
- Physical AI stack + several courses: unnamed, parked.
