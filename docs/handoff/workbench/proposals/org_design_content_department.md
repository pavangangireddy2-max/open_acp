# Proposal — Content/Curriculum Department Org Design

> How to organize Content Stacks, their Product counterparts, and Engineering — for the HOD.
> Design principle: **the org mirrors the system's layer model already locked in this repo**
> (stack curriculum + product overlay + packaging = delivered experience; born-tagged cells
> as the production contract). Conway's law, used on purpose: every team owns a layer, every
> seam between teams is a contract that already exists as an artifact.
> Reconciled 2026-07-10 with the HOD's career framework + KPI system (sources in
> knowledge/raw/corpora/department/; reconciliation in kpi_system_v3_ownership.md).
> Proposal v1.1 — 2026-07-10.

## 0. The one-line model

```
Content Stacks (WHAT is taught)
  → Central Agentic Ops (HOW it is produced)
    → Student Learning Experience (HOW it is consumed)
      → Product Experience (FOR WHOM, packaged per product)
        on Platform Engineering (ON WHAT substrate)
```

Five groups, five layers, four contract seams. Nothing crosses a seam except through its
contract artifact.

## 1. The five groups (the HOD's sketch, sharpened)

### 1.1 Content Stack teams — own WHAT is taught
Teams (7): Full Stack · English · Aptitude · Physical AI · GenAI · DSA · DS/ML.
Each owns, for its stack: course outlines + key takeaways, **node registries** (the WHAT
rail), per-stack intelligence docs (question + pedagogy overlays + learner behaviour),
**review verdicts** (they are the human gate on generated items/decks — approve/edit/reject
with rule ids), misconception banks, and course-version decisions (cheatsheet/course
versions move HERE from SLE — versioning is a content decision, delivery is not).

**Team ↔ catalogue mapping must be published in SLUGS.md** (7 teams, 10 catalogue stacks).
Proposed: DSA team ← programming_algorithms + system_design · Full Stack ← fullstack +
cs_core + devops_testing · others 1:1. Decide once; every registry/corpus path follows it.

### 1.2 Central Agentic Ops — own HOW content is produced
The factory: **Slides/session workflow** (session-architect → deck craft → rendering) and
**Question workflow** (Forge: cell-directed generation → gates → review routing), plus the
shared machinery: skills, C/E gate harnesses + evals (Promptfoo now, Langfuse later), DSPy
programs + gold demonstrations, review tooling (coverage matrix UI), the **context-ops EOD
loop**, Echo, and **Content MCP** (moved here from SLE — it is the knowledge substrate
agents consume; SLE is a consumer, not the owner). Applied AI engineers live here.
Ops runs the factory; stack teams are its reviewers and its customers. Throughput and
quality-at-first-pass are Ops problems; correctness verdicts are stack problems.

### 1.3 Student Learning Experience (SLE) — own HOW students consume
AI Tutor · Adaptivity (delivery logic — the walk, NOT the banks) · Practice & Coding
players · Revision · Student integrity · Instructor LP experience (live quiz, activities).
"Learning redesign" is not a standing team — it's the initiative lane this group runs
(e.g. adaptive-replaces-80%-rule), each initiative with a stack + product counterpart named.
SLE consumes banks via the **item contract** and owns learning-outcome instrumentation
(with the DA/DE partner team via the data-request interface).

### 1.4 Product Experience teams — own FOR WHOM
Two pods matching product categories: **NIAT + GRIT** (degree/offline: universities,
sections, schedules, instructor ops, IRC) and **Academy + Intensive** (upskilling:
cohorts, live sessions, cheatsheet requirements). Each owns its product manifests +
packaging overlays, delivery-quality intelligence (feedback synthesis), delivery rhythm
(schedules), and the product-side acceptance of experience rollouts. They do NOT own
curriculum — they own the overlay and the ground truth of delivery.

### 1.5 Platform Engineering — own the substrate
IDE + compiler/grader · scaling & reliability · observability · AI infra (serving, cost,
tracing). Split the "AI Engineer" role deliberately: **applied** (workflows/evals/DSPy) →
Central Ops; **infra** (serving/cost/tracing) → Platform. Platform also carries an explicit
**contract-debt register** — the known gaps this program has already hit: per-item lint
control, completion API as mastery predicate (not percentage), per-test-case result sync,
grader normalization documentation. These become roadmap items with owners, not folklore.

## 2. The seams (each is an existing artifact, not a meeting)

| seam | contract artifact | flow |
|---|---|---|
| Stack ↔ Ops | **work-order cell** (node × rung × axis) + registry; verdicts back as rule-id rejections | stacks order + review; Ops produces |
| Ops ↔ SLE | **item contract** (born-tagged items + tutorials/explanations + gates passed) | SLE serves what passed |
| Stack ↔ Product | **packaging manifests + product overlays** (resolution semantics) | product adjusts delivery, never curriculum |
| SLE/Product ↔ DA-DE | **data-request docs + node map on the question spine** | evidence flows back to registries |
| all ↔ Platform | SLAs + contract-debt register | substrate guarantees |

Escalation rule: a dispute at a seam is resolved by changing the contract artifact (doc/
manifest/gate), never by side-channel agreement — otherwise the agents working these same
seams drift from the humans.

## 3. KPIs — the org's KPIs ARE the system's dashboards

No parallel spreadsheet universe. Each team is measured by metrics the system already
computes (or is being built to compute):

- **Stack teams:** registry health (coverage, node-clearance rates from ELP), module-quiz
  gold rate per course, release-over-release misconception-frequency reduction, review
  turnaround + verdict quality (edit-distance of their fixes trends down as Ops learns).
- **Central Ops:** approved items per week per cell (coverage-matrix fill velocity),
  first-pass gate rate, judge↔reviewer agreement, cost per approved item, workflow cycle
  time (outline→approved deck; order→approved item), EOD-loop compliance (digest freshness).
- **SLE:** adaptive-vs-static learning lift (module-quiz), node-mastery velocity, tutor
  containment/helpfulness, integrity incident rate, instructor-tool adoption.
- **Product pods:** delivery-quality themes trend (feedback synthesis), class-to-practice
  lag, engagement spread across universities/sections, product NPS.
- **Platform:** grader/IDE reliability + latency, cost per learner, contract-debt burndown.
- **HOD north stars:** learning outcome (gold-tier rate across products) · production
  economics (cost per approved item, trending down as DSPy learns) · freshness (intelligence
  docs current ≤24h) · seam health (disputes resolved by contract change, count).

## 4. Operating rhythm

- **Daily:** EOD digests (context-ops loop) per lane — the HOD reads one page.
- **Weekly:** Stack council (7 stack leads + Ops) — coverage matrices + verdict-quality
  review; SLE/Product sync on rollouts.
- **Monthly:** product councils (pods + SLE + stacks touching that product); contract-debt
  review with Platform; KPI review straight off dashboards.
- **Per initiative:** a one-page charter naming the stack, product, and eng counterparts —
  the answer to "who is the counter-product for a stack" is *per initiative*, not a standing
  1:1 shadow org (7 stacks × 4 products × N eng would be 28+ standing seams; charters keep
  it to the seams that are live).

## 5. Deltas vs the HOD's sketch (explicit)

1. Course versions/cheatsheets: SLE → **Stack teams** (content decision).
2. Content MCP: SLE → **Central Ops** (knowledge substrate; Platform serves it).
3. AI Engineer: split applied (**Ops**) vs infra (**Platform**).
4. Learning redesign: standing team → **initiative lane** in SLE with named counterparts.
5. Added: team↔catalogue stack mapping decision (SLUGS.md), Platform contract-debt
   register, DA/DE as a contracted partner seam, and doc/agent/eval ownership per team
   (each team owns its intelligence docs; Ops owns the machinery that keeps them fresh).

## 6. Pending

- ✅ Reconciled (2026-07-10): career framework (SDE Learning Systems ladder, complexity
  multipliers 1.0–2.5x, 4-pillar rating) + KPI naming convention + V2 tracker (31 KPIs).
  Full ownership mapping + new product/engineering KPI lanes:
  workbench/proposals/kpi_system_v3_ownership.md. Key adoption: Owner column (one team per
  KPI), 8th category "Platform Engineering", targets normalized by complexity multipliers.
- Headcount/sizing pass once roles land (Ops is deliberately small + leveraged; stacks
  scale with course count; SLE scales with surface count).
- **Actual team reality (2026-07-10, HOD):** Content 60 = Aptitude 7 · English 7 · DS&ML 10
  · DS&Algo 10 · FullStack 12 · GenAI 4 · Systems & Infra (CSI) 7 · Pedagogy 3; plus
  Product + DA 10 · Engineering 12 · Graphic Designers 9 — total 91. Mapping updates:
  CSI ≈ cs_core + system_design + devops_testing; the Pedagogy team (3) stewards E-gates +
  the verdict pass (sits with/behind Central Ops as calibration owners); Graphic Designers
  are the deck rendering/asset layer (the owner the deck asset-contract gap was waiting
  for); no Physical AI team yet. Companion: workbench/proposals/continuous_improvement_culture.md.
