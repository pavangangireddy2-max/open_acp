# Data Request — Item Co-Failure Analysis (Python, NIAT 2025 / Batch 3)

> **For the DA/DE team.** A single net-new analytic to add to the Python Learning-Behaviour
> ELP. Everything else we need (first-attempt rate, discrimination, option distributions,
> misconception prevalence, difficulty calibration) your ELP already derives as `Yes`. This
> is the one metric it does not have, and it is the one that tells us whether our course
> **node boundaries** are right.
>
> **This document is self-contained** — it defines the metric, the exact computation, a fully
> worked example, the guardrails, the output shape, and the open decisions we need you to
> settle with your tooling. Please brainstorm feasibility/cost on your infra and come back
> with (a) can you compute it, (b) at what pairing scope, (c) recommended confidence floor.
>
> **What we do NOT need from you:** any node/level/axis/difficulty tagging on the questions.
> Co-failure is unsupervised — it runs on the raw first-attempt matrix. Tagging is our job,
> done separately, and is not a prerequisite for this extract.
>
> Version 1 — 2026-07-08.

---

## 1. What we are trying to decide (why this exists)

We are rebuilding the Python question bank around a **node registry** — a graph of
key-takeaway "nodes" (masterable sub-skills), each of which will get its own pool of
practice items. We author the node boundaries from the course outline. But an outline is a
*teaching plan*, not a map of how the subject is actually learned. Two failure modes we
cannot detect from the outline alone:

- **Two declared nodes are really one skill** — if the same learners fail both, they are one
  masterable unit the outline happened to split across two sessions. → should be merged.
- **One declared node is really two skills** — if a node's items split into two learner
  groups with little overlap, the node hides a seam. → should be split.

Every other metric in the ELP describes **each item in isolation** (this item is hard, this
distractor is popular). **Co-failure is the only metric about the relationship *between*
items** — and a node boundary *is* a relationship between items. That is why we need it.

---

## 2. What the metric is

### 2.1 The input matrix

One row per learner, one column per item, cell = **failed on first attempt (yes/no)**:

```
                item_1  item_2  item_3  ...
learner_A         ✗       ✗       ✓
learner_B         ✓       ✓       ✗
learner_C         ✗       ✗       ✓
...
```

No tags of any kind. Just learner × item × first-attempt-correctness. The clustering
*discovers* the item groupings from this matrix; we do not tell it what the groups are.

### 2.2 The pairwise measure

For each **pair** of items (X, Y), we want an **association** measure, not raw overlap. Raw
overlap just re-finds the hardest items (everyone fails hard items together, trivially).
Association controls for base difficulty. Two equivalent statistics, please return both:

**Lift** — how much failing X raises the chance of failing Y above chance:
```
lift(X,Y) = P(fail X and fail Y) / ( P(fail X) × P(fail Y) )
```
- lift ≈ 1 → independent; failing X says nothing about Y → **different nodes**
- lift ≫ 1 → same learners fail both → **same latent skill (merge candidate)**
- lift < 1 → failing X makes failing Y *less* likely → **strongly separate skills**

**Phi coefficient** — correlation of the two binary fail/pass columns (−1 to +1). Same story,
normalized: +1 = perfectly co-failed, 0 = independent, −1 = mutually exclusive.

### 2.3 The output we cluster

We take your pairwise table and cluster items on the association (hierarchical clustering /
community detection). **The clusters are the empirical nodes.** We overlay them on our
outline-declared nodes: agreements confirm a boundary, disagreements are exactly the
merge/split decisions to review. **The clustering step is ours — you only need to produce the
pairwise table.**

---

## 3. Worked example — Loops module (with arithmetic)

Suppose the outline declares two nodes:

- **Node L1 — `for` loops & `range()`**
  - `i1` predict output of `for i in range(1,5): print(i)` (range bounds)
  - `i2` write a loop summing `range(n)` (range bounds, write context)
  - `i3` MCQ: what does `range(2,10,2)` produce (step argument)
- **Node L2 — `while` loops**
  - `i4` fix an infinite `while` (counter never increments) (loop-variable-update)
  - `i5` predict iterations of `while x < 5` with `x += 1` (loop-variable-update)
  - `i6` MCQ: when is a `while` condition re-checked (top-vs-bottom evaluation)

**A 10-learner slice** (✗ = failed first attempt; real extract ≈ 6,500 learners):

| learner | i1 | i2 | i3 | i4 | i5 | i6 |
|---|---|---|---|---|---|---|
| A | ✗ | ✗ | ✓ | ✗ | ✗ | ✓ |
| B | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| C | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ |
| D | ✓ | ✓ | ✓ | ✗ | ✗ | ✓ |
| E | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ |
| F | ✓ | ✓ | ✓ | ✗ | ✗ | ✓ |
| G | ✗ | ✗ | ✓ | ✓ | ✓ | ✗ |
| H | ✓ | ✓ | ✓ | ✗ | ✗ | ✓ |
| I | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ |
| J | ✓ | ✓ | ✗ | ✗ | ✗ | ✓ |

**Pair (i1, i2) — both inside Node L1:**
- fail i1 = {A,C,E,G,I} = 0.50; fail i2 = {A,C,E,G,I} = 0.50; fail both = 0.50
- lift = 0.50 / (0.50 × 0.50) = **2.00**, phi = **+1.0** → same skill ✓

**Pair (i1, i4) — the cross-node test:**
- fail i1 = {A,C,E,G,I} = 0.50; fail i4 = {A,B,D,F,H,J} = 0.60; fail both = {A} = 0.10
- lift = 0.10 / (0.50 × 0.60) = **0.33**, phi = **−0.5** → separate skills ✓

**The full table you would return:**

| pair | sessions | P(fail X) | P(fail Y) | P(both) | lift | phi |
|---|---|---|---|---|---|---|
| i1–i2 | L1–L1 | .50 | .50 | .50 | **2.00** | +1.0 |
| i1–i3 | L1–L1 | .50 | .20 | .10 | 1.00 | 0.0 |
| i4–i5 | L2–L2 | .60 | .60 | .60 | **1.67** | +1.0 |
| i4–i6 | L2–L2 | .60 | .20 | .10 | 0.83 | −0.2 |
| i1–i4 | L1–L2 | .50 | .60 | .10 | **0.33** | −0.5 |
| i2–i5 | L1–L2 | .50 | .60 | .10 | 0.33 | −0.5 |

### What we learn (and could learn *no other way*)

1. **L1/L2 boundary confirmed** — `for` and `while` are genuinely separate (lift 0.33). Keep
   two nodes.
2. **Both nodes hide a seam** — `i3` (range *step*) stands apart from i1/i2 (lift 1.0), and
   `i6` (while evaluation timing) stands apart from i4/i5. → each session is really **two**
   sub-skills; the registry splits them. The outline would have buried these.
3. **Counter-example (what a merge looks like):** had `i1–i4` come back at lift ≈ 1.9, it
   would mean there is no separate "for" and "while" mastery — just one "loop control flow"
   skill — and we would **merge** L1 and L2 into one node. No per-item metric could ever
   surface that; only co-failure does.

---

## 4. Guardrails — the difference between signal and artifact

These are the same landmines already documented in your ELP; applied to pairs they matter
more, because a bad row here fabricates a fake relationship:

1. **First-attempt only.** Later attempts are contaminated by hints/retries/copying —
   co-failure on those measures help-seeking, not skill.
2. **Engaged attempts only.** Drop implausibly fast answers (e.g. MCQ < 5s). A rush-guesser
   fails everything and manufactures fake co-failure across unrelated items.
3. **Aggregate clones by `content_hash`.** Duplicate content under different `question_id`s
   (we measured 19–34% duplication in this corpus) would otherwise show near-infinite lift
   with themselves and pollute every cluster. Same content = one item.
4. **Exclude known-defective items.** Items with wrong keys / non-firing traps (we hold a
   do-not-port list; can share) are failed by everyone and forge spurious association with
   their neighbours. Exclude or flag.
5. **Denominator = learners who attempted *both* items.** The legacy MCQ player served a
   **sample of 15 of ~30** per run, so many pairs were never shown to the same learner. Thin
   overlap = low confidence, not low association — carry the both-attempted count on every
   row so we can filter. (`question_start_datetime` exists, so exposure is derivable.)
6. **Cross-session pairs are the prize; same-unit pairs are noise.** Items in one unit share
   a stem/context and co-fail for trivial reasons. The valuable rows are **cross-session**
   (e.g. Loops items × Functions items) — those reveal hidden prerequisites and mergeable
   nodes. In-unit co-failure is expected; deprioritize or exclude it.

---

## 5. Requested output shape

One row per item pair:

```
co_failure_pairs:
  item_x_hash            # content_hash (not question_id)
  item_y_hash
  session_x, session_y   # so cross-session pairs are visible
  question_type_x/_y     # MCQ / FIB / textual / coding — pairing across types is fine
  n_both_attempted       # DENOMINATOR — learners who saw & first-attempted both
  p_fail_x, p_fail_y     # base first-attempt fail rates
  p_fail_both
  lift                   # P(both) / (P(x)·P(y))
  phi                    # binary correlation, -1..1
```

### One-paragraph spec for the query author

> From first-attempt outcomes (engaged attempts only — drop < 5s answers; aggregate clones by
> `content_hash`; exclude do-not-port defective items), for every item pair where
> `n_both_attempted ≥ N`: compute `P(fail X)`, `P(fail Y)`, `P(fail both)`, then
> `lift = P(both)/(P(X)·P(Y))` and `phi`. Return one row per pair with both `session_id`s,
> question types, and `n_both_attempted`. Prioritise **cross-session** pairs.

Source tables this is buildable from (already in your ELP's Source Tables sheet — **no new
instrumentation required**): `all_users_question_attempt_details_for_question_set_units` and/or
`all_users_question_wise_responses_summary_details_for_question_set_units` (first-attempt
correctness), joined to `content_question_set_units_questions_details` (item→session,
content metadata). This is the reason it is an incremental ask, not a pipeline.

---

## 6. Open decisions — please settle these with your tooling and report back

1. **Confidence floor `N`** — minimum `n_both_attempted` for a pair to count. With the
   15-of-30 sampler, overlap density varies. What is the realistic overlap distribution, and
   what `N` keeps pairs trustworthy? (Our starting guess: `N ≥ 300` for a ~6,500 cohort —
   your data density decides.)
2. **Pairing scope / cost** — all-item-pairs is O(n²) and may be expensive at ~5,000 items.
   Cheapest useful version: **within-module + adjacent-module pairs only** (Loops×Loops,
   Loops×Functions) — that is where merge/split decisions live. Which is cheaper on your
   infra: compute all pairs, or accept a module-scoped pairing list from us?
3. **Coding items** — first-attempt "fail" for coding = first-submit not accepted (per your
   funnel metrics; per-test-case detail is not synced and not needed here). Confirm you can
   emit a first-submit pass/fail flag so coding items can join the matrix; if not, we run
   co-failure on objective items only for v1.
4. **Engaged-attempt threshold** — is `< 5s` the right rush cutoff for MCQ, and is there an
   equivalent floor you would trust for coding/textual? Your call from the time distributions.
5. **Defective-item list handoff** — do you want our do-not-port list to exclude upfront, or
   would you rather flag-and-keep so we filter downstream?

---

## 7. What this is NOT (scope guard)

- **Not a tagging request.** No node/level/axis/difficulty labels needed on any question.
- **Not a new pipeline.** Built from tables you already query for the ELP.
- **Not clustering** — you produce the pairwise association table; we cluster it, because the
  cluster cut-points are node-design decisions we own.
- **Not blocked on our node map.** Co-failure is independent of and *prior to* our node
  authoring — that independence is the whole point (it lets behaviour check our boundaries
  rather than echo them).

---

## Appendix — how this fits the larger effort (context, not required reading)

This is one input to a Python **node registry** (a masterable-skill graph the new adaptive
question bank is built on). Companion asks, all already `Yes`/`Partial` in your ELP:
difficulty calibration (first-attempt-rate bands vs authored tags), discrimination /
broken-item rate, MCQ option-selection → misconception prevalence, coding acceptance funnel.
The only two things genuinely *not* derivable today (documented in your Tracking Gaps sheet,
parked as future instrumentation): per-test-case coding failure anatomy, and novelty-burn
(first-attempt-rate inflation over item age). Neither blocks this co-failure request.
