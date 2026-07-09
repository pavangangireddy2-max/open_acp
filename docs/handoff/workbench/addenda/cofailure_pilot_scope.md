# Addendum — Co-Failure Pilot Scope (answers Section 6, decision #2)

> Companion to `data_request_item_cofailure_python.md`. DA/DE flagged that the all-pairs
> space is too large to compute. This note sizes the problem and scopes a **single-module
> pilot (Loops)** so we prove the method on ~74K pairs before deciding whether to run the
> rest. Version 1 — 2026-07-09.

---

## 1. Why whole-course is infeasible (the number)

Co-failure pairs grow as n²/2. Across all **4,963** questions in the Python corpus that is
**12,313,203 pairs** — the O(n²) blow-up. DA/DE are right to refuse it.

**The fix: pairs only form *within* a scope.** Co-failure is only meaningful between items in
the same skill area anyway (cross-module pairs are almost all independent — noise). So we
never compute the 12M. We compute **within-module** only:

| Scope | Questions | Pairs | vs whole course |
|---|---|---|---|
| Whole course (all-pairs) | 4,963 | 12,313,203 | 1× |
| Largest module (Sequence of Instructions) | 472 | 111,156 | 0.9% |
| **Loops (pilot)** | **386** | **74,305** | **0.6%** |
| Smallest module (Python Standard Library) | 107 | 5,671 | 0.05% |
| **All 17 modules, run independently (sum)** | — | **~866,000** | **7%** |

Two takeaways for DA/DE: (a) the **whole eventual job** is ~866K pairs, not 12M — 7% of the
naive cost; (b) **no single module exceeds ~111K pairs**, so it batches cleanly one module at
a time. The 386/74K figures are pre-dedup upper bounds — after `content_hash` collapsing of
clones (19–34% duplication) and defective-item exclusion, the real Loops count drops further.

---

## 2. The pilot: Loops module only

**Why Loops and not "first four sessions":** "first four sessions" straddles two modules
(Intro to Python = sessions 1–2, Sequence of Instructions = sessions 3–4), so within-skill
cross-session pairs get split across the window boundary. A **module** is the coherent skill
unit co-failure is meant to test. Loops is the best single pilot because:

- it has **real merge/split questions** — `for` vs `while` vs nested, exactly the boundary
  decisions the method exists to resolve (see the worked example in the main doc);
- it is one of the **two dominant break clusters** in the behaviour data (highest value);
- at ~74K pairs it is mid-sized — a fair cost probe, not a trivially small one.

**Loops module composition** (from the session→unit→question mapping):

| Session | id (short) | Question sources | ~Questions |
|---|---|---|---|
| Loops | `3b64b5f7` | Quiz A 34 · Quiz B 27 · MCQ Practice 112 · Coding 11 | 184 |
| Understanding Coding Question Formats | `48f61d2d` | MCQ Practice 23 | 23 |
| For Loop | `f6a42c4e` | Quiz A 56 · MCQ Practice 84 · Coding 6+11+11+11 | 179 |
| **Module total** | | | **386** |

**Scope rule for the query:** pair items where **both** belong to the Loops module (the three
session_ids above). Report `session_x`/`session_y` on every row so the interesting
**cross-session** pairs (Loops-intro ↔ For-Loop) are visible — those are where merge/split
lives; same-session pairs are expected to co-fail and are lower value.

All guardrails from the main doc still apply unchanged: first-attempt only, engaged attempts
only (drop <5s), `content_hash`-aggregated, defective items excluded, `n_both_attempted` as
denominator on every row.

---

## 3. What the pilot decides (before we ask for more)

Run Loops, hand us the pairwise table, we cluster it, and we answer three things:

1. **Does the method work on your infra at acceptable cost?** (74K pairs is the probe.)
2. **Do the empirical clusters agree with our authored Loops nodes**, or do they show the
   merges/splits we expect (`range`-step and `while`-evaluation-timing standing apart)?
3. **Is the cross-session signal strong enough** to justify running the other 16 modules
   (~792K more pairs)?

If yes on all three → we roll out module-by-module (each module is an independent batch, so
you can pace them). If the cost or signal disappoints → we've spent 0.6% of the naive budget
to find out, and we rethink before scaling.

---

## 4. Open questions still on DA/DE (unchanged from main doc §6)

Only the scope decision (#2) is now settled. Still need your read on:

- **Confidence floor `N`** — min `n_both_attempted` per pair. With the 15-of-30 MCQ sampler,
  what is the actual pair-overlap density within Loops? That sets a trustworthy `N`.
- **Coding items** — can you emit a first-submit pass/fail flag so the 50 Loops coding items
  join the matrix? If not, pilot runs on objective items only.
- **Rush cutoff** — is `<5s` the right engaged-attempt floor for MCQ here?
