# Item Co-Failure Analysis — PILOT Implementation Spec
**For: Claude Code**
**Prepared by: DA team**
**Scope: Pilot run before full-scale rollout**
**Source ask: Data Request — Item Co-Failure Analysis (Python, NIAT 2025 / Batch 3), v1, 2026-07-08**

---

## 0. Purpose

Validate the co-failure computation pipeline end-to-end on a small, real slice of data before
running it at full scale. This pilot must produce: a working item-pair co-failure table, a
session-pair roll-up, and answers to the open questions (confidence floor `N`, rush-answer
threshold, clone-duplication rate) using real numbers instead of placeholder guesses.

**This is not a scoped-down version of the method** — no session/item pairs are excluded.
All-pairs is computed in full, because at this size it's cheap. Scoping strategies are a
full-scale concern only (out of scope for this pilot).

---

## 1. Pilot scope

| | |
|---|---|
| Users | 4,812 |
| Questions | 584 |
| Sessions | 5 |
| Item pairs (all-pairs) | 584 × 583 / 2 = **170,236** |
| Session pairs (all-pairs) | 5 × 4 / 2 = **10** |
| Input matrix size | 4,812 × 584 ≈ 2.8M cells — trivial in memory |
| Output matrix size | 584 × 584 ≈ 341K cells — trivial in memory |

Expect this to run end-to-end in well under a minute on a standard machine. No batching,
chunking, or scoping logic is needed at this size.

---

## 2. Available SQL fields (as extracted)

| field | type | notes |
|---|---|---|
| `user_id` | STRING | learner |
| `exam_id` | STRING | not used in this pipeline |
| `course_id` / `course_title` | STRING | not used in this pipeline (single course assumed) |
| `topic_id` / `topic_title` | STRING | not used in this pipeline for now — potential future grouping level above session |
| `unit_id` / `unit_title` / `unit_type` | STRING | not used in this pipeline for now |
| `question_id` | STRING | item identifier |
| `first_attempt_result` | STRING | outcome of first attempt — needs mapping to C/IC (see §3.1) |
| `time_spent_till_first_submission` | INTEGER | **mostly NULL** — rush-answer filtering is deprioritized for this pilot (see §4.1); carried through unfiltered |
| `question_type` | STRING | MCQ / FIB / textual / coding etc. |
| `session_title` | STRING | **this is our session grouping field** — used as `session_id` throughout |

### 2.1 Known gaps vs. the original spec — flag, don't silently work around

- **No `content_hash` field is present.** The original request's clone-aggregation guardrail
  (duplicate content under different `question_id`s, 19–34% measured elsewhere) **cannot be
  applied in this pilot** — there is no content-hash equivalent available. Use `question_id`
  as the item key as-is. **Do not silently skip this guardrail without noting it** — flag it
  explicitly in the pilot output write-up as a known limitation, and ask the data engineering
  side whether a content-hash equivalent can be added before the full-scale run.
- **No explicit "attempted but not present" signal beyond row absence.** Whether a missing
  (user_id, question_id) row means "not shown to this learner" vs. "shown but not attempted"
  should be confirmed with whoever owns this extract — for this pilot we treat **row absence
  = not attempted (`NA`)**, consistent with the original spec.
- **`session_title` is a string label, not a numeric session_id.** That's fine — treat it as
  a categorical key throughout; no need to map it to an integer ID unless useful for readability.

---

## 3. Step 1 — Build the base table from the SQL extract

Required columns only (drop the rest for this pipeline — `exam_id`, `course_*`, `topic_*`,
`unit_*` are not needed here):

```python
import pandas as pd
import numpy as np

raw = pd.read_csv("pilot_extract.csv")  # or however the SQL extract is loaded

df = raw[[
    "user_id", "question_id", "session_title",
    "first_attempt_result", "question_type",
    "time_spent_till_first_submission"
]].copy()
```

### 3.1 Map `first_attempt_result` to fail/pass

Confirmed distinct values in this field (from source):

| value | meaning | mapped to |
|---|---|---|
| `CORRECT` | first attempt fully correct | pass → `0` |
| `INCORRECT` | first attempt wrong | fail → `1` |
| `PARTIALLY_CORRECT` | first attempt partially right | **treated as fail → `1`** — a partial answer still indicates the learner did not fully master the item on first attempt, which is the behavior this metric is meant to capture |

```python
result_map = {
    "CORRECT": 0,             # pass
    "INCORRECT": 1,           # fail
    "PARTIALLY_CORRECT": 1,   # fail (treated same as incorrect for this analysis)
}

df["failed"] = df["first_attempt_result"].str.upper().map(result_map)

# sanity check: anything that didn't map?
unmapped = df[df["failed"].isna() & df["first_attempt_result"].notna()]
assert unmapped.empty, f"Unmapped first_attempt_result values found: {unmapped['first_attempt_result'].unique()}"
```

Rows present in this table = attempted (`CORRECT` / `INCORRECT` / `PARTIALLY_CORRECT`). Rows
absent for a given (user_id, question_id) = `NA` (not attempted) — handled naturally by the
pivot in §6 (missing cell = NaN).

### 3.2 No first-attempt deduplication needed

The SQL extract already contains **only first-attempt details** (confirmed) — there is no
retry/multi-attempt data to collapse. One row per (user_id, question_id) is guaranteed by the
source query. No deduplication step is needed here; skip straight to §4.

---

## 4. Step 2 — Quality filters (guardrails)

### 4.1 Rush-answer filter — DEPRIORITIZED for this pilot

`time_spent_till_first_submission` is mostly NULL in this extract, so it can't meaningfully
filter most of the data right now. **For this pilot, do not apply a rush-answer filter** —
carry the column through unfiltered and unmodified (no imputation needed either, since we're
not using it as a filter yet).

```python
# no filtering applied on time_spent_till_first_submission for this pilot run
# column is retained as-is for a later descriptive check only (see below), not used to drop rows
```

**Still worth a quick look (informational only, not a filter):** check what fraction of rows
actually have a non-null time value, and what the distribution looks like where present — this
tells us whether this field will be usable at all for the full-scale run, without blocking the
pilot on it now.

```python
non_null_frac = df["time_spent_till_first_submission"].notna().mean()
print(f"Fraction of rows with non-null time_spent: {non_null_frac:.2%}")

observed_times = df.loc[df["time_spent_till_first_submission"].notna(),
                         ["question_type", "time_spent_till_first_submission"]]
observed_times.groupby("question_type")["time_spent_till_first_submission"].describe()
```

### 4.2 Clone aggregation — SKIPPED for this pilot (see §2.1)

No `content_hash` field is available in this extract. This guardrail is not applied here.
Flag this explicitly as a known gap in the pilot write-up — do not silently proceed as if
this guardrail were satisfied.

### 4.3 Defective-item exclusion — SKIPPED for this pilot

No do-not-port list has been provided yet for this pilot. Proceed without it, but note in the
write-up that this filter was not applied, and any unusually high-lift pairs discovered
should be checked against item quality before being read as a real behavioral signal.

### 4.4 Session-pair flag — both within-session and cross-session pairs computed and kept

Carry `session_title` through as-is. **All pairs are computed and retained for this pilot** —
within-session (`session_x == session_y`) as well as cross-session (`session_x != session_y`).
With only 5 sessions and 584 items, the data volume is small enough that there's no reason to
drop within-session pairs; they're useful here both as a sanity check (do they behave as
expected — mostly lift > 1?) and because within-session pairs are what reveal a session
hiding two sub-skills (a split candidate), which cross-session pairs alone can't show.

---

## 5. How the matrix and pairs are formed, and how to interpret the output

*(Read this before running the code in §6 — it explains the mechanics conceptually.)*

### 5.1 The matrix itself

After §3–4, you have a table with one row per (user, question) that was actually attempted,
and a `failed` flag (0/1). Pivoting this gives a **users × questions grid**:

```
                q_101   q_102   q_103   ...   q_584
user_1            1       0      NaN            0
user_2           NaN      1       1             0
user_3            0       0       0            NaN
...
user_4812         1      NaN      1             1
```

- `1` = failed that question on first attempt
- `0` = passed
- `NaN` = this user never attempted this question at all (common — no learner sees all 584 items)

This is the **only** input. Everything downstream is derived from this grid — no additional
data is used.

### 5.2 How a "pair" is formed

A pair is simply **any two columns (questions) from this grid**, e.g. `(q_101, q_102)`. With
584 questions, there are `584 × 583 / 2 = 170,236` such column-pairs — every question is
compared against every other question exactly once (we don't compare a question to itself,
and we don't count `(q_101, q_102)` and `(q_102, q_101)` separately — they're the same pair).

For **each pair**, we look only at the users who have a non-NaN value in **both** columns —
i.e., users who actually attempted both questions. That subset is what all the statistics
for that pair are computed from. A user who attempted `q_101` but never saw `q_102` simply
doesn't count toward the `(q_101, q_102)` pair's statistics.

This is why `n_both_attempted` (§6) matters so much — it's the sample size behind every
other number in that pair's row, and it will vary a lot from pair to pair depending on how
much overlap there was in who saw which questions.

### 5.3 What we compute per pair

For the subset of users who attempted both questions in a pair:

| stat | meaning |
|---|---|
| `n_both_attempted` | how many users this pair's numbers are based on (sample size) |
| `p_fail_x`, `p_fail_y` | how often each question is failed on its own, among that subset |
| `p_fail_both` | how often **both** are failed by the *same* user |
| `lift` | is `p_fail_both` higher or lower than you'd expect if the two questions were unrelated? |
| `phi` | same idea as lift, but expressed as a standard −1 to +1 correlation |

**Why lift instead of just `p_fail_both`?** Two genuinely unrelated hard questions will still
often be failed by the same people just because both are hard for everyone. Lift corrects for
that by dividing out each question's own difficulty — it isolates whether failing one
specifically predicts failing the other, beyond what raw difficulty would explain.

### 5.4 How to read a single pair's result

- **`lift ≈ 1`** → the two questions are behaving independently. Knowing someone failed X
  tells you nothing extra about whether they failed Y. → different skills.
- **`lift` well above 1 (e.g. > 1.5)** → learners who fail one tend to also fail the other,
  more than chance alone explains. → likely the *same underlying skill* — a merge signal if
  this happens across sessions, or an expected/uninteresting result if it happens within the
  same session (questions in one session naturally cluster around one topic).
- **`lift` below 1 (e.g. < 0.7)** → failing one makes failing the other *less* likely than
  chance — a genuinely strong separation. Rare, but a clean confirmation that two skills are
  distinct.
- **`phi`** tells the same story on a bounded −1 to +1 scale — useful for sorting/ranking
  pairs consistently, since lift is unbounded above (can technically go very high on tiny
  samples) while phi is easier to compare across pairs at a glance.

**Always check `n_both_attempted` alongside lift/phi before trusting a pair.** A pair with
`lift = 3.0` based on only 8 co-attempting users is not evidence of anything — it's noise.
The same lift based on 2,000 co-attempting users is a real signal. This is exactly why the
confidence floor `N` (§7.2) exists — it's a cutoff below which we don't trust the number at
all, regardless of how extreme it looks.

### 5.5 What the full output table looks like, and how to use it

The final table (§7.1) has **one row per question pair that cleared the confidence floor**,
with `session_x`/`session_y` attached so you can see at a glance whether a pair is:

- **within the same session** — expected to show lift > 1 fairly often (questions in one
  session share context). Useful mainly as a sanity check that the pipeline behaves as
  expected, and to spot sessions that might secretly contain two sub-topics (if some
  within-session pairs show lift ≈ 1 while others show lift ≫ 1, that session may not be as
  cohesive as assumed).
- **across two different sessions** — this is where the real find is. A cross-session pair
  with high lift is telling you: "these two sessions, despite being taught separately, are
  actually testing the same underlying skill in the learners' minds" — a potential merge
  candidate. A cross-session pair at lift ≈ 1 confirms the sessions are testing genuinely
  different things — the boundary is fine as-is.

The **session-pair roll-up** (§7.3) then summarizes this at the session level: for each of
the 10 session-pairs (5 sessions → 5×4/2 = 10 pairs, plus the 5 within-session groups), you
get a single row showing the median lift and what fraction of that session-pair's questions
showed a strong relationship — so you don't have to read all 170K rows to get the overall
picture, but the full table is still there underneath if you want to drill into specifics.

---

## 6. Step 3 — Build the matrix

```python
fail_pivot = df.pivot_table(
    index="user_id", columns="question_id", values="failed", aggfunc="first"
)
# cell values: 0 = pass, 1 = fail, NaN = not attempted (row simply absent for that user/question)

F = fail_pivot                          # users x items, {0, 1, NaN}
A = ~F.isna()                           # attempted mask, boolean users x items
Fz = F.fillna(0).astype(int)            # zero-filled, only meaningful combined with A

print(f"Matrix shape: {F.shape}")       # expect ~ (≤4812, ≤584) — some users/items may
                                          # drop out entirely if all their rows were filtered
                                          # in §4.1; check for this explicitly:
print(f"Users with zero attempts after filtering: {(A.sum(axis=1) == 0).sum()}")
print(f"Items with zero attempts after filtering: {(A.sum(axis=0) == 0).sum()}")
```

**Explicitly check the "both attempted" condition** (this is the core guardrail from the
original spec — do not skip):

```python
n_both_attempted = A.T.values.astype(np.int32) @ A.values.astype(np.int32)
# n_both_attempted[i, j] = count of users who attempted BOTH item i and item j
```

This is computed for **every pair in one matrix operation** — not a per-pair loop, not a
SQL join. This is the correct and only place this check happens.

---

## 7. Step 4 — Compute pairwise statistics

```python
both_fail_counts = (Fz.values * A.values).T.astype(np.int32) @ (Fz.values * A.values).astype(np.int32)
fail_counts      = (Fz.values * A.values).sum(axis=0)      # per-item fail count
attempted_counts = A.values.sum(axis=0)                    # per-item attempted count

items = F.columns.to_numpy()
n_items = len(items)

# per-item base fail rate
p_fail_item = fail_counts / attempted_counts   # length n_items

i_idx, j_idx = np.triu_indices(n_items, k=1)   # all unique pairs, i < j

n_both = n_both_attempted[i_idx, j_idx]
both_fail = both_fail_counts[i_idx, j_idx]

# avoid division by zero for pairs with zero co-attempted users
valid = n_both > 0

p_fail_x = p_fail_item[i_idx]
p_fail_y = p_fail_item[j_idx]
p_fail_both = np.divide(both_fail, n_both, out=np.zeros_like(both_fail, dtype=float), where=valid)

lift = np.divide(p_fail_both, p_fail_x * p_fail_y,
                  out=np.zeros_like(p_fail_both), where=(p_fail_x * p_fail_y) > 0)

# phi coefficient — standard binary correlation from 2x2 contingency table
# using: both_fail, x_fail_only, y_fail_only, both_pass  (restricted to co-attempted users)
x_fail_y_pass = fail_counts[i_idx] - both_fail  # approx — needs both-attempted restriction, see note below
```

**Note on phi:** compute phi directly from the 2×2 contingency table **restricted to
co-attempted users only** (not all users who attempted item i, some of whom never saw item
j). The cleanest way is to build the four contingency cells per pair directly from the
co-attempted subset:

```python
from scipy.stats import pearsonr

# vectorized phi via correlation on {0,1} vectors is equivalent to phi coefficient;
# for full correctness compute per-pair using only rows where A[:,i] & A[:,j] are both True.
# At 170K pairs this can be vectorized using the four contingency counts:

both_pass = n_both - both_fail - (fail_counts[i_idx] - both_fail) - (fail_counts[j_idx] - both_fail)
x_only_fail = fail_counts[i_idx] - both_fail   # NOTE: only valid if fail_counts[i_idx] itself
y_only_fail = fail_counts[j_idx] - both_fail   # is restricted to the co-attempted subset —
                                                 # for full correctness, recompute fail_counts
                                                 # per-pair from the co-attempted mask, not globally.
```

**Flag for Claude Code:** the phi calculation needs the four contingency cells computed
strictly within the co-attempted population for each pair, not the global per-item fail
count. The safest correct implementation:

```python
def phi_coefficient(a, b, c, d):
    # a = both fail, b = x fail y pass, c = x pass y fail, d = both pass (all within co-attempted subset)
    n = a + b + c + d
    num = (a * d) - (b * c)
    denom = np.sqrt((a + b) * (c + d) * (a + c) * (b + d))
    return np.divide(num, denom, out=np.zeros_like(num, dtype=float), where=denom > 0)
```

Build `a, b, c, d` per pair using masked matrix products restricted to `A[:,i] & A[:,j]`
(e.g., `a = both_fail_counts[i,j]`, `d = both_pass_counts[i,j]` computed the same way as
`both_fail_counts` but on the pass indicator, and `b`/`c` from cross terms) — do this via
matrix multiplication the same way as `both_fail_counts`, not via the shortcut arithmetic
above, to avoid the co-attempted-subset error.

---

## 8. Step 5 — Assemble output tables

### 7.1 Item-pair table (per original spec)

```python
co_failure_pairs = pd.DataFrame({
    "item_x": items[i_idx],
    "item_y": items[j_idx],
    "n_both_attempted": n_both,
    "p_fail_x": p_fail_x,
    "p_fail_y": p_fail_y,
    "p_fail_both": p_fail_both,
    "lift": lift,
    "phi": phi,   # from corrected calculation above
})

# attach session_title and question_type per item via a lookup
item_meta = df.drop_duplicates("question_id").set_index("question_id")[["session_title", "question_type"]]

co_failure_pairs["session_x"] = co_failure_pairs["item_x"].map(item_meta["session_title"])
co_failure_pairs["session_y"] = co_failure_pairs["item_y"].map(item_meta["session_title"])
co_failure_pairs["question_type_x"] = co_failure_pairs["item_x"].map(item_meta["question_type"])
co_failure_pairs["question_type_y"] = co_failure_pairs["item_y"].map(item_meta["question_type"])
```

### 7.2 Apply confidence floor N

```python
# for the pilot, first PLOT the distribution before picking N:
co_failure_pairs["n_both_attempted"].describe()
co_failure_pairs["n_both_attempted"].hist(bins=50)

N = ...  # decide based on the actual distribution observed — do not default to 300 blindly
co_failure_final = co_failure_pairs[co_failure_pairs["n_both_attempted"] >= N].copy()
```

### 7.3 Session-pair roll-up

```python
rollup = (
    co_failure_final
    .groupby(["session_x", "session_y"])
    .agg(
        n_item_pairs=("lift", "size"),
        median_lift=("lift", "median"),
        pct_lift_gt_1_5=("lift", lambda s: (s > 1.5).mean()),
        pct_lift_lt_0_7=("lift", lambda s: (s < 0.7).mean()),
    )
    .reset_index()
    .sort_values("median_lift", ascending=False)
)
```

With only 5 sessions (10 pairs), this table is small enough to read in full — no ranking
threshold needed at this stage, just eyeball it directly.

---

## 9. Pilot validation checklist

Use this pilot specifically to settle real numbers for the open questions in the original
request, before the full-scale run:

- [ ] **Overlap distribution** — histogram of `n_both_attempted` across all 170,236 pairs.
      Determine a realistic `N` from this data, not the placeholder `N ≥ 300`.
- [ ] **Rush-answer threshold** — check `time_spent_till_first_submission` distribution
      (non-imputed values only) per `question_type`. Confirm or adjust the 5s cutoff —
      especially since most values are NULL, this threshold is doing little filtering work
      in the pilot itself; note this explicitly.
- [ ] **`first_attempt_result` value mapping** — confirm all distinct values are correctly
      mapped to pass/fail (see §3.1) — do not assume only two clean values exist.
- [ ] **Clone-duplication gap** — flag explicitly that this guardrail could not be applied
      due to missing `content_hash`; note whether any `question_id`s look suspiciously
      identical in content (if question text is available anywhere) as a manual sanity check.
- [ ] **Within- vs cross-session pattern check** — confirm within-session pairs
      (`session_x == session_y`) skew toward lift > 1 (expected/trivial) and that the
      cross-session pairs show a real spread — validates the pipeline is producing sensible
      output before scaling up.
- [ ] **End-to-end run time** — record actual run time for each step to project full-scale
      (3,849 questions / 96 sessions / 4,920 users) resource needs.

---

## 10. Explicit non-goals for this pilot

- No session/item pair scoping or funnel logic — full all-pairs, as originally planned.
- No clustering of the output — that remains the requesting team's downstream step.
- No node/level/axis tagging.
- No attempt to backfill `content_hash` — flag the gap, don't invent a workaround (e.g. do
  not attempt fuzzy text matching on question content as a substitute without explicit sign-off).