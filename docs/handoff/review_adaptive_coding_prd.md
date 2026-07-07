# Review — "Adaptive Coding Algorithm" PRD (Product one-pager)

> Evaluation of the IRT/Elo adaptive-coding brief for the Computer Programming course,
> against: the platform's confirmed behaviour (student-experience doc), the question-bank
> intelligence (rungs, pool math, single-use items), and the Forge/Canon/Crux architecture
> (node × rung × axis tags as the producer↔consumer contract). All numeric claims below are
> from **executing the PRD's exact formulas** (simulation, 2026-07-07). Reviewed by Claude
> for Pavan. Verdict first, evidence after.

## Verdict

The PRD gets the *product instincts* right — independence-weighted correctness, live item
recalibration, a dual-condition mastery gate, and carefully thought-through edge cases
(re-attempts, external solves, post-mastery freeze). Those should survive.

But the *engine as specified* does not do what the brief claims: the parameters were never
simulated, and four math defects make the published behaviour (smooth θ progression toward
mastery, "P(correct) near 0.5 for optimal challenge") unreachable. Separately, the design is
**node-blind**, which conflicts with the architecture the rest of the program is built on and
forfeits the diagnostic value that justifies adaptivity in the first place. All of it is
fixable with bounded changes; none of it should ship as written.

---

## What's genuinely good (keep these)

1. **Independence-weighted correctness** (`correct = score_ratio × independence`) is the
   best idea in the doc — it uses signals the platform actually has (AI-tutor invocations,
   answer views, submission counts) to make θ reflect *unassisted* ability. Nothing in our
   own proposal had this; adopt it.
2. **Live item recalibration** (d updates) is the right instinct — authored difficulties are
   uncalibrated guesses until real attempts arrive. (Execution needs fixing; see Issue 3.)
3. **Dual mastery gate** (ability AND volume floor) prevents trivial 2-question mastery —
   in fact it's the only thing that does (see Issue 2).
4. **Edge-case discipline:** highest-score re-attempt policy (prevents θ farming),
   post-mastery freeze, external-solve inclusion, onboarding, never-backward progress bar.
5. **Bounded difficulty normalisation** from the content team's raw 4–13 scale — sensible,
   assuming the raw scale exists and is roughly linear (question below).

## Critical issues (simulation-backed, ranked)

### 1. The sigmoid is nearly flat on these scales — the model can barely discriminate
With θ, d ∈ [0.05, 1.0], the exponent (θ−d) spans only ±0.95, so
**P(correct) is confined to [0.28, 0.72]** no matter how mismatched learner and item are.
The model believes a brand-new learner has a 28% chance on the hardest item in the course.
Real IRT operates on a logit scale several units wide, or adds a discrimination parameter.
**Fix:** `P = 1/(1+e^(−a(θ−d)))` with a ≈ 4–6 (then re-derive all thresholds), or keep the
formulas and move θ, d to a wider scale. Without this, update sizes and the mastery threshold
have no calibrated meaning.

### 2. K is an order of magnitude too large — θ is a coin-flip tracker, not an estimate
Executing the spec: a perfect no-help learner starting at θ₀ = 0.3 hits **θ = 1.009 after
two questions** (mastery θ crossed at Q2) and **θ = 1.98 by Q6** — θ exits the [0,1]
difficulty scale entirely, after which "nearest harder question" is undefined (nothing is
harder). Nothing in the spec clamps θ or d. For a *mediocre* learner (true ability 0.5),
**25% of runs cross the mastery-θ within 2 questions** and 28% oscillate back below 0.5
after crossing — θ whipsaws instead of converging. The θ ≥ 0.75 condition is therefore
noise; the 65% volume floor silently becomes the only real gate, which means the "adaptive"
engine mostly reduces to "solve ~two-thirds of the unit" — the same 80%-style rule it was
meant to replace, minus the transparency.
**Fix:** K in the 0.05–0.15 range on the current scale (or Elo-standard K on a logit scale),
clamp θ and d, and **make a simulation suite part of PRD acceptance** — trajectories for
perfect / mediocre / struggling / help-heavy learners must look sane before build. (Ours is
reusable.)

### 3. Shared item difficulty thrashes — a "hard" item goes NEGATIVE after 3 clean solves
d updates use the same oversized K, from *each learner's own* early-attempt K (0.70):
simulated, an authored-hard item at d = 0.80 drops to **0.398 → 0.083 → −0.21** after three
consecutive clean solves. Item difficulty is shared mutable state being rewritten by
single-digit evidence — early-cohort noise permanently corrupts the pool, and the drifting d
silently diverges from the Easy/Medium/Hard chip the UI shows for the same question.
**Fix:** separate K_item ≪ K_learner (~K/10); freeze d until an item has ≥30 attempts, then
batch-recalibrate (nightly), not per-submission; clamp to [0.05, 1.0]; version the d so the
UI chip and the engine can't disagree; define concurrency semantics (who wins simultaneous
updates).

### 4. Skip-as-incorrect punishes exactly the behaviour the platform defined as safe
Spec: skip → correct = 0 → θ −= K·P ≈ **−0.35, erasing a full solve** (simulated). But the
platform's owner-confirmed semantics (objective player) treat skip as *deferral with no
evidence*, and the PRD itself brands skip a "question change request." Punishing it teaches
students to fail-submit instead of skip (same 0, doesn't burn one of 2 skips) — a perverse
incentive.
**Fix:** skip = no θ update (no evidence), still capped at 2, still swaps to an easier item.

### 5. The engine is node-blind — it optimises difficulty, not learning
θ is one scalar per unit; items enter the engine as difficulty values only. The whole
program architecture (Forge thread, locked) makes **node × rung × axis tags the contract
between the bank and the delivery logic**, and this engine reads none of them. Consequences:
- **Mastery ≠ coverage:** a learner can clear θ ≥ 0.75 + 65% volume while the unattempted
  35% is exactly the one node they're weak on. The gate certifies effort, not concept mastery.
- **No diagnostic output:** the engine's product is "θ = 0.78," not "weak at nested-loop
  tracing" — so the mastery-map results screen, misconception feedback, and Crux's future
  root-cause routing all get nothing to consume. The PRD's own Future Scope ("inter-unit θ
  carry-over via KP tagging") concedes knowledge-point structure is coming — it should be the
  spine now, not a bolt-on.
**Fix (small, preserves the engine):** two-loop design. **Outer loop = node coverage**
(every node of the session must be served and cleared); **inner loop = this Elo engine**
choosing the next item *within* the target node by nearest-harder-d. Log per-node,
per-misconception evidence on every attempt regardless. This keeps 90% of the PRD and makes
it Crux-compatible.

### 6. The mastery volume gate assumes small static units — clashes with the Forge pool
The unit-size table (5–18 questions, "solve ≥65% of the unit") describes **today's static
units**, not the adaptive bank (40–60 reviewed items/session at ≥3 variants per
node × rung × axis — where 65% of the pool would mean 26–39 forced solves). So this PRD is
implicitly a **v0 over the existing bank**. That's a legitimate, shippable scope — but it
must be stated, and the gate must change when the Forge bank lands (mastery = per-node
clearance, not pool percentage). Right now the doc reads as *the* adaptive design, which it
can't be.

### 7. Independence table has a hole the size of the biggest leak: Public Submissions
Students can browse others' accepted solutions (owner-confirmed), yet the help taxonomy only
covers AI Tutor, "answer seen," and submission counts. Copy-from-public-submissions scores
as "No help = 1.00." Also underspecified: what counts as "answer seen" (Tutorial tab open?
— which is currently freely available and whose gating is itself a design decision), and
double-counting between submissions≥3 discounts and score_ratio already using best-of-N.
**Fix:** add public-submission views (≈ answer-seen tier, 0.2–0.4), define answer-seen =
Tutorial open, and decide tutorial gating (unlock after first failed submit) in the same doc.

### 8. Metrics reward the wrong thing
Primary = completion rate, secondary = effort saved. Both go UP if the engine gets *easier* —
Goodhart bait, with no learning-outcome check anywhere. Feedback is a self-reported 1–5.
**Fix:** validation metric = **module-quiz performance lift** (and θ-vs-quiz correlation);
completion rate demoted to guardrail; keep effort-saved as the efficiency claim.

### Smaller but real
- **K undefined for attempts 1–3** (table starts at "4–5"); ambiguous whether the count is
  per-unit or global.
- **"First question in the defined sequence must be solved before recommendations unlock"**
  contradicts adaptivity (a fixed forced entry point) — if it's a plumbing constraint, name
  it as such.
- **Progress bar** can sit near-full while unmastered ("solve the questions correctly to
  achieve mastery" state) — awkward; if mastery is per-node (Issue 5 fix), the node rail
  replaces this cleanly.
- **θ₀ = 0.3 uniform** — fine for v1, but prior-unit evidence exists and is a cheap upgrade.
- **No telemetry spec:** the attempt-event logging (node, misconception, failing test-case
  class) that the DA/DE request doc defines should be a PRD requirement, or the behaviour
  data for calibration never materialises.
- **External solves** count toward the algorithm — with what independence data? (Bank/search
  contexts may not log tutor usage the same way.)

## Questions for the author

1. Where does the **raw 4–13 difficulty scale** come from, and is it the same scale as the
   incoming difficulty-tagged re-export? (We need one canonical difficulty source.)
2. Is "questions attempted" for the K schedule **per unit or global**? What K applies to
   attempts 1–3?
3. What defines **"answer seen"** exactly (Tutorial tab? public submission view? diff view)?
4. How are **concurrent d updates** handled (two students submitting the same minute)?
5. On **re-attempt**, θ "recalculates normally" — against the item's *current* (drifted) d or
   the d at first attempt?
6. Is this PRD explicitly scoped as **v0 over the existing static bank** (5–18 items), to be
   re-based on the Forge cell-structured pool later? If yes, say so in the doc; if no, the
   mastery gate and pool assumptions need rework now.

## Recommended path (keeps the PRD's core)

1. Fix the math floor: discrimination parameter (a ≈ 5) or logit scale; clamp θ, d;
   K → 0.05–0.15 (learner) and ~K/10 (item, frozen until n ≥ 30, batch-updated).
2. Skip = no evidence.
3. Wrap the Elo engine in a **node-coverage outer loop**; log node + misconception evidence
   per attempt (Crux-ready from day one).
4. Patch the independence table (public submissions, answer-seen definition, tutorial gating).
5. Re-anchor metrics on module-quiz lift; completion becomes a guardrail.
6. Ship as **v0 on existing units** with the fixes, explicitly labelled; re-base the mastery
   gate on node clearance when the Forge bank replaces the pool.
7. Adopt **simulation acceptance tests** for any parameter change (suite available in repo
   history; happy to hand it over).
