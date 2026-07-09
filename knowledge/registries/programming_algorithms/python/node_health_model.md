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
