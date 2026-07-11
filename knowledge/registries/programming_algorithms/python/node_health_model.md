# Node Health & Sufficiency Model

> **What makes a node "done".** The registry says which nodes exist and their L1–L5 ladders.
> This model says, per node, whether the question bank behind it is **sufficient** — or
> whether Forge should author more/better. A node is not finished when it's authored; it's
> finished when engaged learners reach mastery without running out of fresh items or getting
> bored.
>
> Metrics live in a **separate per-node health view joined on `Node_ID`** — the registry CSV
> stays structure-only; this view fills as data arrives. Two tiers: **supply** (measurable
> now, from the bank) and **demand** (needs learner data — pending from the DE team).
>
> Authored 2026-07-09. Companion: `module_01_introduction.csv`, the node registry.

## The one question this answers

> For node N: **do we need more/better questions, or is it enough?**

Everything below serves that verdict. The `Node_ID` is the join key every metric hangs off —
which is why the registry is authored first and kept clean.

## Tier 1 — Supply metrics (LIVE NOW, from the question bank)

Countable from the bank alone; no learner needed. These gate whether a node has *enough
shelf*.

| Metric | Definition | Signal |
|---|---|---|
| **Coverage depth** | Items per `(node × rung × axis)` cell vs the floor (**≥3 fresh** variants — retry + step-up needs them) | Cells below floor = the work order for Forge |
| **Rung coverage** | Are all of the node's authored L-rungs populated? | An empty L3 breaks the adaptive step-up |
| **Axis coverage** | Read / Fix / Fill / Tweaked all present where the node warrants them | Missing axis = learner can Fix but never Write |
| **Novelty** | Distinct templates ÷ total items (guards against clone-padding) | Corpus was 19–34% duplicates — 5 clones ≠ coverage of 5 |
| **Contract completeness** | Each coding item ships tests + tutorial; each objective ships explanation | Incomplete items can't be graded/served |

**Tier-1 verdict:** a node **meets the coverage floor** when every warranted cell has ≥3
distinct, contract-complete items. This is fully computable today from
`computer_programming_question_details.json`.

## Tier 2 — Demand / verification metrics (PENDING learner data)

This is the "student feedback decides if it's enough" tier. None are computable until the DE
team's learner-behaviour extracts land — each row below is effectively a line item in that
data request.

| Metric | Definition | "Need more/better" trigger | Data needed |
|---|---|---|---|
| **Mastery-reach rate** | % of engaged learners who reach the node's target level | Low → teaching/pool inadequate | per-learner × node attempts + outcomes |
| **Pool-exhaustion rate** | How often a learner runs out of fresh items before mastering | High → **author more** (the most direct signal) | served-item counts per learner × node |
| **First-attempt correct rate** (per rung) | Empirical difficulty of the rung | Too high → trivial/boring; too low → mis-taught or mis-rung | first-attempt correctness per item, served-denominator |
| **Boredom signal** | Composite: low variety + low difficulty-variance + drop-off + short time-on-task | High → **author better** (more variety/challenge), not just more | ratings, time-on-task, drop-off, sequence |
| **Explicit rating** | Item/session thumbs or stars, if the portal collects it | Low → review the node's items | rating events per item |
| **Discrimination** | Does the item separate strong from weak learners | Low → weak item, replace | attempt outcomes across ability spread |

**Note on served-denominator:** every per-item rate needs the *served* count, not just
attempts — the legacy player samples ~15 of ~30, so uncorrected rates are biased. (Locked
project-wide.)

## The sufficiency verdict (Tier 1 AND Tier 2)

```
if coverage_floor_met(node):
    if not learner_data_available(node):
        verdict = "COVERED — awaiting demand data"      # where we are today
    elif mastery_reach healthy AND exhaustion low AND boredom low:
        verdict = "SUFFICIENT — freeze, spend effort elsewhere"
    else:
        verdict = "AUTHOR BETTER"                        # more variety / harder / clearer
else:
    verdict = "AUTHOR MORE"                              # fill the coverage gap first
```

Rung calibration is a *side effect* of Tier 2: first-attempt-correct rates per rung tell us
whether the authored L1–L5 boundaries match reality, so the same data that verifies
sufficiency also **corrects the ladder** I'm currently authoring by judgment.

## Where this sits in the loop

```
registry (Node_ID)  →  Forge fills to COVERAGE floor (Tier 1)  →
learners use  →  Lens / DE extracts measure DEMAND (Tier 2)  →
per-node verdict (more / better / enough)  →  Forge tops up  →
Echo weekly refresh keeps the verdict current
```

The registry is the spine; this health view is what turns "we authored a bank" into "we know
the bank is working." It also **sharpens the DE data request**: every Tier-2 row names the
exact extract it needs, keyed by `session_id / unit_id / question_id + content hash`.

## Status today

- **Tier 1: buildable now.** A per-node coverage snapshot for Module 1 can be computed from
  the question JSON on request (deferred per 2026-07-09 decision until conventions are locked).
- **Tier 2: blocked** on learner-behaviour extracts (task #3). When they arrive, they populate
  this view and calibrate the registry's rungs — the registry `Node_ID` is the join key.
- **Boredom** is already anecdotally reported ("students felt bored"); Tier 2 makes it a
  measured, per-node number instead of a global impression.

## Rung policy, pool sizing, and the mastery gate (added 2026-07-11)

Answers four bank-design questions with the pilot evidence (s11–s15 co-failure run):
levels inside nodes, rung boundaries, per-cell counts, coding-item applicability, mastery.

### Levels vs rungs — two ladders, one mapping
- **L1–L5 (registry)** = capability statements per node, ragged (not every node earns 5).
- **Rungs (bank)** = 3 authored difficulty bands per node: easy / medium / hard, mapped onto
  the node's L-levels (typically easy≈L1–L2, medium≈L2–L3, hard≈L4+).
- **No authored sub-rungs** (no Easy-1/Easy-2 tags): authors demonstrably can't discriminate
  finer grades (corpus difficulty tags arrived 158 EASY / 3 MEDIUM / 179 untagged). Within-rung
  ordering is EMPIRICAL — sort by observed first-attempt fail rate; recalibrated continuously.
  Sub-rungs come free from data, cost nothing to author, and never drift.

### Rung boundaries — authored by features, validated by fail bands
Rung is assigned at authoring from a per-node feature checklist (e.g. s11 N4 ladder: easy =
2 ifs, else obvious · medium = 3 ifs, several fire · hard = TEXTUAL exact multi-line output).
Validation bands from pilot s11 deciles (p50 = 16%, p90 = 40% first-attempt fail):
**easy ≤15% · medium 15–40% · hard >40%.**
QA trigger: item outside its rung's band for 2 consecutive windows (n≥150 served) → re-rung
or rewrite. Pilot audit of s11 (evidenced items): N1 bands [9/6/0], N2 [2/13/4],
N3 [12/11/0], N4 [8/5/3] — **N1 and N3 have zero evidenced hard items** → first concrete
Forge work orders from this model.

### Pool sizing — the ≥3-per-cell floor, derived not asserted
Mastery gate window = 4 items at target rung; one remediation re-climb ≈ 4 more; single-use
after reveal → a learner can consume ~8–9 distinct items per node×rung. Spread over ~3
warranted axes ⇒ **≥3 per cell** (the Tier-1 floor above — now derived from the walk).
Per-node config block (defaults; registry may override per node):
```yaml
node_policy:
  target_rung: hard|medium      # core nodes hard, peripheral medium (registry column)
  gate: {window: 4, pass: 3, min_axes: 2, last_must_pass: true}
  volume_floor: 4               # PRD's dual-gate idea, kept — blocks 2-question mastery
  demote_after: 2               # consecutive fails at rung → drop rung + remediate
  pool_floor_per_cell: 3
  quiz_reserve_per_node: 3      # held out for module quiz — never served in practice
  mastery_halflife_days: 30     # stale mastery → revision re-probe
```
Rough per-node total: 3 rungs × ~3 axes × 3 + reserve ≈ 25–35 items (ragged cells reduce it).
s11 at 4 nodes ⇒ ~100–130 items; current inventory 174 but mis-distributed (hard cells empty).

### Coding questions — same nodes, different evidence semantics
Verified: the co-failure pilot extract contains **zero CODING items** (types present:
CODE_ANALYSIS_MCQ/TEXTUAL, MCQ, REARRANGE, FIB_CODING). Corpus holds 340 CODING items.
Policy: **nodes are skills; item types are evidence channels** — same registry, no parallel
"coding nodes". Three deltas:
1. Objective items are single-demand probes (1 node). CODING items are compositional →
   registry carries `primary_node` + `secondary_nodes[]`; Write axis = strongest evidence.
2. Coding first-attempt = all test cases pass (harsh). Richer attribution (per-test-case
   results, error class → misconception family, e.g. NameError→LP-06) is gated on the
   named contract-debt "per-test-case result sync".
3. Full-scale co-failure MUST include coding attempts as a **separate lane** — compositional
   items correlate broadly (ability-heavy phi); use them to validate Depends_On edges, not to
   discover nodes. Pending until the extract includes CODING.

### Mastery — a per-node decision, not a score
Consistent with the adaptive-PRD review (outer/inner loop) and the completion contract-debt:
- **Outer loop:** session complete = every CORE node mastered at its target rung
  (replaces the 80% rule — completion API as mastery predicate).
- **Per-node gate (deterministic, explainable):** ≥3 of last 4 first-attempts correct at
  target rung, on distinct items spanning ≥2 axes, most recent correct, ≥4 total attempts
  on the node. Demotion: 2 consecutive fails → drop a rung, remediate (tutorial/explanation),
  re-climb. Start at medium (easy if a Depends_On parent is weak). Never test a node before
  its Depends_On parents are mastered — walk order follows registry edges (the 163 robust
  cross-session pairs are the evidence base for those edges).
- **θ/Elo (PRD engine, with the review's fixes):** inner-loop item-selection heuristic only —
  picks the next item near the learner's level within the node. Never the mastery predicate.
- **Why not IRT/BKT now:** single-use burn means item-level parameters never stabilize.
  Upgrade path when full-scale ELP data lands: calibrate at **cell level** (variants within a
  node×rung×axis cell are difficulty-exchangeable by design; C-gates enforce distinctness,
  fail-band QA enforces exchangeability) — cell-level BKT slip/guess/learn is estimable.
- **Decay:** mastered nodes re-probed after `mastery_halflife_days`; failed re-probe →
  revision queue, not full re-climb.
- **The gate audits itself:** if learners mastered on node X still fail X's dependents at
  entry far above baseline, X's gate is too loose (tighten window/rung). Same robust-pair
  machinery, now pointed at the policy — thresholds become measurable, not vibes.
