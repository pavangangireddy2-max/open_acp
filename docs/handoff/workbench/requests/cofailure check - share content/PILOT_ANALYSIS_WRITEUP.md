# Item Co-Failure Analysis — Pilot Results

**What this is:** a pilot run of a method to find pairs of exam questions ("items") that
learners tend to fail *together* more often than chance would predict. The goal is to
surface two kinds of findings: (1) sanity-check that the method works, and (2) spot cases
where two questions — sometimes from entirely different taught sessions — are effectively
testing the same underlying skill, or conversely where a single session secretly contains
two different skills bundled together.

**Scope of this run:** 4,812 learners, 584 questions, 5 sessions. This is a pilot on real
data to validate the pipeline before a full-scale run (projected: 3,849 questions / 96
sessions / 4,920 users).

---

## 1. What data we started with

We pulled 6 columns per learner-question attempt from BigQuery:

| column | what it is |
|---|---|
| `user_id` | the learner |
| `question_id` | the question ("item") |
| `session_title` | which taught session the question belongs to |
| `first_attempt_result` | outcome of the learner's first attempt |
| `question_type` | MCQ, textual, coding, etc. |
| `time_spent_till_first_submission` | how long they took (see gap below — this turned out to be unusable) |

Each row = one learner attempting one question for the first time. If a learner never saw a
question at all, there's simply no row for that pair — we treat that as "not attempted,"
not as a failure.

## 2. Turning attempts into pass/fail

`first_attempt_result` had three values, mapped as:

| value | meaning | mapped to |
|---|---|---|
| `CORRECT` | fully correct | pass |
| `INCORRECT` | wrong | fail |
| `PARTIALLY_CORRECT` | partly right | **fail** — a partial answer still means the learner didn't fully master the item on the first try |

## 3. Known gaps in this pilot (flagged, not silently worked around)

- **No content-hash field.** The original ask included a guardrail to merge duplicate
  questions that exist under different `question_id`s (measured at 19–34% elsewhere). This
  extract has no equivalent field, so that guardrail could not be applied. **Open ask to
  data engineering:** can a content-hash equivalent be added before the full-scale run?
- **`time_spent_till_first_submission` is 100% null** in this extract — not just "mostly
  null" as originally expected. The rush-answer filter (dropping suspiciously fast guesses)
  could not be evaluated at all in this pilot. This needs a different data source or extract
  fix before the full-scale run if that filter matters.
- **No defective-item exclusion list** was available, so no known-bad questions were
  filtered out. Any unusually extreme result below should be sanity-checked against item
  quality before being read as a real behavioral signal.

## 4. Building the "who failed what" grid

After the mapping above, we pivoted the data into a grid: one row per learner, one column
per question, and each cell is either **fail**, **pass**, or **blank** (never attempted).
No learner attempts all 584 questions, so most cells are blank — that's expected and normal.

## 5. Comparing every pair of questions

With 584 questions, there are **170,236 possible pairs** (584 × 583 ÷ 2 — every question
compared against every other question exactly once). For **every pair**, we looked only at
the learners who attempted **both** questions in that pair, and asked: do people who fail
one of these two questions also tend to fail the other, more than you'd expect by chance?

Two numbers per pair:

- **`lift`** — the core number. `lift ≈ 1` means the two questions behave independently
  (failing one tells you nothing about the other). `lift` well above 1 (e.g. 1.5+) means
  failing one strongly predicts failing the other — a sign they're testing the *same*
  underlying skill. `lift` below 1 is rarer and means failing one actually makes failing the
  other *less* likely — a clean confirmation the two skills are genuinely distinct.
- **`phi`** — the same relationship expressed on a standard −1 to +1 correlation scale,
  useful for ranking pairs consistently since `lift` has no upper bound on small samples.

Critically, every pair also gets an **`n_both_attempted`** count — how many learners the
pair's numbers are actually based on. A `lift` of 3.0 based on 8 co-attempting learners is
noise, not a finding; the same `lift` based on 2,000 learners is real. This is the whole
reason for the next step.

## 6. Setting a confidence floor (the "N" decision)

Before trusting any pair's numbers, we required a minimum number of co-attempting learners
behind it. Rather than pick a default, we looked at the actual distribution of
`n_both_attempted` across all 170,236 pairs:

| | value |
|---|---|
| median | 121 |
| 75th percentile | 309 |
| mean | 219 |
| max | 2,697 |

Typical fail rates across questions run ~20% (median 19.5%), so the "both failed" cell that
`lift`/`phi` are built from has an *expected* count of roughly `0.04 × n_both_attempted`
under independence — and that expected count needs to be at least ~10 for the statistic to
be stable rather than swing wildly on a couple of learners.

**We set the confidence floor at N = 300** (matching the 75th percentile of the observed
distribution, and independently justified by pushing the expected "both-fail" cell size to
a comfortable ~12), then also validated a more permissive **N = 150** for the follow-up
investigation below (kept 42% of all pairs, expected cell ~6 — noisier but still usable, and
confirmed all session-to-session comparisons remained represented at this floor).

## 7. Rolling the 170K pairs up to the session level

The 5 sessions produce 15 session-level groups (5 "within one session" + 10 "across two
different sessions"). For each group we report: how many item-pairs cleared the confidence
floor, the median `lift` across those pairs, and what fraction were strongly related
(`lift > 1.5`) or strongly separated (`lift < 0.7`).

**Note on a bug we caught and fixed:** the first version of this rollup double-counted each
cross-session pair — "Session A vs Session B" and "Session B vs Session A" showed up as two
different rows with two different numbers, because the underlying question ordering was
arbitrary. Fixed by treating session pairs as unordered before grouping, so each session
comparison now has exactly one row.

### Results (N = 150)

| Session A | Session B | # item pairs | median lift | % pairs lift > 1.5 | % pairs lift < 0.7 |
|---|---|---:|---:|---:|---:|
| Understanding Coding Question Formats | Understanding Coding Question Formats (within) | 253 | 1.44 | 42% | 0% |
| Conditional Statements | Conditional Statements (within) | 5,462 | 1.41 | 42% | 4% |
| Conditional Statements | Understanding Coding Question Formats | 3,650 | 1.18 | 18% | 6% |
| For Loop | For Loop (within) | 1,919 | 1.18 | 7% | 2% |
| Loops | Loops (within) | 3,846 | 1.16 | 11% | 7% |
| For Loop | Understanding Coding Question Formats | 2,394 | 1.15 | 11% | 6% |
| For Loop | Loops | 5,430 | 1.13 | 7% | 5% |
| Conditional Statements | For Loop | 6,357 | 1.13 | 13% | 4% |
| Conditional Statements | Nested Conditional Statements | 9,177 | 1.12 | 13% | 4% |
| Loops | Understanding Coding Question Formats | 3,151 | 1.11 | 10% | 5% |
| Nested Conditional Statements | Understanding Coding Question Formats | 2,806 | 1.10 | 10% | 5% |
| For Loop | Nested Conditional Statements | 5,526 | 1.08 | 6% | 4% |
| Conditional Statements | Loops | 9,431 | 1.08 | 13% | 10% |
| Nested Conditional Statements | Nested Conditional Statements (within) | 4,215 | 1.07 | 7% | 3% |
| Loops | Nested Conditional Statements | 8,274 | 1.07 | 6% | 4% |

**How to read this:** within-session rows are a sanity check — questions inside one taught
session naturally cluster around a shared topic, so `lift > 1` there is expected and mostly
uninteresting on its own. The two exceptions, `Understanding Coding Question Formats` and
`Conditional Statements`, show the *highest* internal cohesion (median lift 1.4+, ~42% of
their internal pairs strongly related) — those sessions are well "glued together" internally.

Cross-session rows are where the interesting findings would be: a cross-session pair with
high lift means two sessions taught separately are secretly testing the same skill (merge
candidate). **None of the 10 cross-session comparisons here reach that bar** — all sit in the
modest 1.07–1.18 range, meaning the 5 sessions are, at this level, testing genuinely
different things from each other. No merge candidates in this pilot.

## 8. Investigating "does a session secretly hide two skills?"

The flip side of the question above: does a session that looks *weakly* cohesive internally
actually contain two distinct sub-skills bundled together? Three sessions stood out as
candidates because their internal median lift was low and few of their own item-pairs were
strongly related:

| session | median lift (within) | % pairs > 1.5 |
|---|---:|---:|
| Nested Conditional Statements | 1.07 | 7.0% |
| Loops | 1.16 | 10.7% |
| For Loop | 1.18 | 6.5% |

For each, we pulled every within-session item pair and ran hierarchical clustering (forcing
a 2-way split) on the item-to-item `lift` values, to check whether a distinct sub-group of
questions co-fails tightly with each other but not with the rest of the session.

**A data-quality caveat that matters here:** even at the N=150 floor, 30–70% of the
theoretically possible within-session item pairs didn't have enough co-attempting learners
to clear the floor at all (worst case: "For Loop" lost 37 of its 116 questions entirely —
they had *zero* pairs with enough shared attempts to say anything). Missing pairs were not
silently treated as "no relationship" — they were filled with that session's own median
observed lift as a neutral placeholder, and every result below is checked against how much
of the data was real vs. filled.

### Result: Nested Conditional Statements — no split found
Forcing a 2-way split produced identical within-cluster and between-cluster median lift
(1.070 in both cases) — a sign the split is arbitrary noise, not a real structure. **No
action needed here.**

### Result: For Loop — no split found
Same pattern: within- and between-cluster medians identical (1.177). **No action needed
here.**

### Result: Loops — real split candidate found
A 6-question sub-group showed a median internal lift of **1.76**, clearly higher than the
1.16 median for the rest of the session — and unlike the two sessions above, this signal is
backed by real, well-sampled data (410–455 co-attempting learners per pair, all above the
confidence floor; none of it is filled-in placeholder data).

**The 6 questions and their relationships to each other:**

| item | question_type | avg fail rate |
|---|---|---:|
| `3218ec78-2c94-4a28-aa31-42c01ad467ad` | Code Analysis (MCQ) | 10.0% |
| `39ec96a0-12db-4223-8231-2d5c79bb9065` | Code Analysis (Textual/free-response) | 42.7% |
| `7fe10957-02be-4f81-b055-bb1030a4dc8e` | Code Analysis (MCQ) | 15.2% |
| `a0081625-1ec5-41e8-8cd1-d6a0fc31144a` | Code Analysis (MCQ) | 9.1% |
| `dd4165ba-0ddb-405d-9288-d234e74f2a53` | Code Analysis (MCQ) | 4.4% |
| `e4a74737-dc7d-4c93-b4a6-afbe4d522c78` | Code Analysis (MCQ) | 0.8% |

All 15 pairwise relationships among these 6 questions show `lift > 1` (every pair, no
exceptions) — several strikingly high:

| pair (shortened) | learners both attempted | lift |
|---|---:|---:|
| dd4165ba ↔ e4a74737 | 410 | **16.1** |
| 3218ec78 ↔ e4a74737 | 447 | **9.7** |
| a0081625 ↔ e4a74737 | 446 | 4.2 |
| 7fe10957 ↔ e4a74737 | 455 | 2.9 |
| 39ec96a0 ↔ e4a74737 | 411 | 2.3 |
| 7fe10957 ↔ dd4165ba | 449 | 2.0 |
| a0081625 ↔ dd4165ba | 427 | 1.9 |
| 3218ec78 ↔ a0081625 | 435 | 1.8 |
| 7fe10957 ↔ a0081625 | 442 | 1.5 |
| 39ec96a0 ↔ a0081625 | 419 | 1.4 |
| 3218ec78 ↔ 7fe10957 | 455 | 1.3 |
| 3218ec78 ↔ 39ec96a0 | 421 | 1.2 |
| 39ec96a0 ↔ 7fe10957 | 421 | 1.2 |
| 3218ec78 ↔ dd4165ba | 430 | 1.2 |
| 39ec96a0 ↔ dd4165ba | 430 | 1.1 |

**One thing worth a manual content check:** `e4a74737...` has a very low base fail rate
(under 1%) but drives the two highest-lift pairs in the table (16.1 and 9.7). Rare-but-
predictive is the classic signature of a hard, highly discriminating question — worth
confirming its content actually matches the shared theme of the other 5, rather than it
being a coincidence of a small "both failed" count.

**Recommended next step:** send these 6 `question_id`s to the curriculum team to check
whether they share an obvious theme distinct from the rest of "Loops" (e.g., a specific loop
pattern, a particular edge case) — this is the strongest, best-evidenced finding from the
pilot. The other two candidate sessions (Nested Conditional Statements, For Loop) can be
set aside; no internal split was found in either.

## 9. Bottom line

- **Pipeline works end-to-end** on real data at pilot scale (170,236 pairs computed in
  well under a minute).
- **No cross-session merge candidates** found in this pilot — the 5 sessions test
  genuinely distinct skills from each other.
- **One strong split candidate found**: a 6-question sub-cluster inside "Loops" that
  co-fails far more tightly with itself than with the rest of the session — ready for
  curriculum review.
- **Confidence floor recommendation:** N = 300 for a "trust this number" cutoff, though
  N = 150 was used for the split investigation above to retain enough data to detect
  sub-clusters, with results specifically checked to confirm they weren't driven by filled-in
  placeholder data.
