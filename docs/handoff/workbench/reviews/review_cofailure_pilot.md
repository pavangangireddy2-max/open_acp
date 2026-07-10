# Review — Item Co-Failure Analysis (Pilot)

> Independent review of the DE team's co-failure pilot (`workbench/requests/cofailure check
> - share content/`). I read the writeup + `CLAUDE.md` spec + the code, and **re-ran the raw
> `co_failure_pairs.csv` (71,891 pairs) myself** to verify the headline claims rather than
> take the rollup at face value.
>
> **Verdict: the pipeline is sound and the method is right — but the writeup's two headline
> conclusions are stated on the *median*, which hides the actual signal. One conclusion holds,
> one needs correction. The split-candidate finding is solid.** Reviewed 2026-07-10.

## What's genuinely good

- **Method is correct.** Lift (difficulty-corrected co-failure) + phi + an `n_both_attempted`
  confidence floor is exactly the right instrument. The all-pairs matrix approach is clean and
  fast.
- **Honesty about gaps is exemplary** — the three flagged limitations are the *right* three,
  and they match our own locked non-negotiables:
  - **No content-hash** → the clone-merge guardrail couldn't run. This is the single most
    important gap (see below) and they flagged it, didn't paper over it.
  - `time_spent` 100% null → rush-answer filter couldn't run. Correctly deprioritized.
  - No defective-item exclusion → high-lift pairs need item-quality sanity-check. Correct.
- **The cross-session double-counting bug they caught and fixed** (unordered session pairs) is
  real and they handled it right.
- **The "Loops" split candidate is well-evidenced** — I confirmed the 6-item sub-cluster
  against the raw file: all 15 pairs lift>1, well-sampled (410–455 co-attempters), no filled
  placeholder data. This is a legitimate finding to send to curriculum.

## Correction 1 — "no cross-session merge candidates" is a MEDIAN artifact (overturned as stated)

The writeup concludes the 5 sessions "test genuinely different things" because every
session-pair's **median lift** sits in 1.07–1.18. But medians over thousands of pairs wash out
exactly the pairs a merge search is looking for. Re-running the raw file at the same N≥300 floor:

- **3,353 of 33,838** cross-session pairs have **lift > 1.5** (not "none").
- Top cross-session pairs reach **lift 6–7.85**, well-sampled (N=304–470) — e.g. `Loops ↔
  Conditional Statements` at 7.85, `Nested Conditional ↔ Loops` at 7.83.

So the claim "no cross-session pair reaches the merge bar" is **false at the item level** —
it's only true of the session-level medians. **The rollup is the wrong resolution for a merge
hunt.** A merge signal is a *sub-cluster* of high-lift cross-session pairs, not a shifted
median — the same logic the writeup itself used correctly for the *within*-session split hunt,
but didn't apply across sessions.

## Correction 2 — but those high-lift pairs are mostly RARE-ITEM ARTIFACTS (so the conclusion survives, for the right reason)

Before anyone chases those lift-7 pairs as merge candidates, the deeper check: **all 28 of the
lift>4 cross-session pairs involve an item with <5% base fail rate.** That's the same
`e4a74737` pattern the writeup flagged inside Loops — lift explodes when one item is almost
never failed, because the "both-failed" cell is tiny and unstable even at N>300. The tell:

- median **phi** among the lift>1.5 cross pairs is only **0.11**; among lift>4, **0.14**.
- Phi is the bounded, sample-robust measure. **High lift + near-zero phi = small-cell
  inflation, not a real shared skill.**

**So the writeup's *conclusion* (no cross-session merges) is probably right — but its *reason*
is wrong.** The sessions aren't clean because medians are ~1.1; they're clean because the
high-lift pairs are rare-item statistical artifacts with negligible phi. That distinction
matters enormously at full scale (3,849 questions), where "sort by lift" will surface a
thousand of these artifacts and someone will mistake them for findings.

## Recommendations

**To the DE team (before full-scale run):**
1. **Rank merge candidates by phi, not lift** — or require *both* lift>1.5 AND phi>~0.2 AND a
   minimum both-failed *cell count* (not just co-attempted N). Lift alone is unsafe at scale.
2. **Report cross-session findings as sub-clusters, not session medians.** Run the same
   clustering used for the within-session split hunt on the cross-session pair graph. The
   median rollup is fine as a dashboard, wrong as the merge detector.
3. **Content-hash is now the critical-path blocker**, not a nice-to-have. Without it, at 3,849
   questions the 19–34% clone rate means a large fraction of "high co-failure" pairs will just
   be *the same question under two ids* — which will read as a fake merge signal. This must be
   resolved before full scale. (This is our locked join rule: `question_id + content hash`.)
4. Add the **defective-item exclusion list** before scale — an unexcluded broken item co-fails
   with everything.

**To the curriculum team:**
- The **Loops 6-item split candidate** is worth a real content review — it's the one solid,
  phi-checked, well-sampled finding. Send those 6 `question_id`s. (But confirm `e4a74737` at
  0.8% fail actually shares the theme — it drives the two highest-lift pairs and is itself a
  rare-item case.)

## How this feeds our own work

- **Directly validates the node-registry premise.** A within-session split candidate = "one
  session secretly holds two nodes" — exactly what the WHAT-rail registry makes explicit. The
  Loops sub-cluster is empirical evidence that the registry's node boundaries won't always
  match session boundaries.
- **This is a Tier-2 demand metric arriving early.** Co-failure/discrimination is in the node
  health model (`knowledge/registries/python/node_health_model.md`) as pending learner data —
  this pilot is the first slice of it. When the full run lands (with content-hash), it joins
  the registry on `question_id → node` and calibrates which nodes actually co-fail.
- **Re-confirms content-hash as non-negotiable** across every consumer (Forge, Lens, this
  analysis). Worth escalating to data engineering as a shared blocker, not a per-request ask.

---

## Addendum (2026-07-10) — Content adjudication of the Loops 6-item split candidate

The writeup's recommended next step was "send these 6 question_ids to the curriculum team to
check whether they share an obvious theme." We hold the mined corpus, so the check is done —
all six items pulled and compared at content level:

| item | what it actually is | misconception-bank match |
|---|---|---|
| `3218ec78` | while counter<3 trace, offset print + post-loop "End" | boundary/trace family |
| `39ec96a0` | while over string indices from counter=2 (TEXTUAL, 42.7% fail) | boundary/trace family |
| `7fe10957` | `while a:` flag flipped false inside → "Working\nEnd" | LP-04 adjacent (runs-once semantics) |
| `a0081625` | `while number == 0:` increments → runs exactly once | **LP-04** (bank evidence item) |
| `dd4165ba` | `count = (count + 1)` uninitialized inside loop → NameError | **LP-06** (bank evidence item) |
| `e4a74737` | `while counter < 2:` counter never defined → NameError | **LP-06** (bank evidence item) |

**Adjudication:**
1. **Not clones.** All six are distinct snippets — the missing content-hash guardrail does
   NOT invalidate this particular finding (it remains critical for full scale).
2. **The theme is real and matches our authored misconception structure:** the sub-cluster
   is *while-loop control-variable state reasoning* — its two strongest seams are exactly
   bank families LP-06 (uninitialized variable → NameError) and LP-04 (runs-once semantics).
   The 16.1 pair is two *different* snippets sharing ONE misconception — precisely the
   "same latent skill" signal co-failure exists to find. Behaviour and content mining
   converge independently; this is the strongest possible validation of the method.
3. **But the headline numbers are thin-cell:** computed from the delivered pairs file,
   **11 of 15 cluster pairs rest on both-fail cells < 10 learners**; the flagship lift 16.1
   = a 2-learner cell; lift 9.7 = 2 learners; the robust anchor is `39ec96a0` (42.7% fail;
   cells 21–38). The cluster is directionally right, statistically fragile at the top.
   → concrete floor for full scale: require **both-fail cell ≥ 10** alongside phi ≥ ~0.2.
4. **`e4a74737`'s 0.8% fail rate is a platform artifact, not learner brilliance:** its
   correct option spells out the full NameError verbatim AND the read-only editor's lint
   marker flags the undefined-`counter` line (the documented lint-leak). A nearly
   un-failable item → tiny cells → inflated lift wherever it appears, including the top
   cross-session artifact pairs. Rare-item screens at full scale should check for
   answer-leak explanations before treating rarity as difficulty.

**Registry consequence (for the future Loops/s13 module):** plan the session as (at least)
two nodes — *while-loop trace & accumulation* vs *while-loop state & termination semantics*
(initialization/definition, runs-once, flag exit) — pending full-scale confirmation under
content-hash + cell-floor guardrails. Behaviour has now challenged a session boundary
exactly as the request intended; the registry is where the verdict lands.
