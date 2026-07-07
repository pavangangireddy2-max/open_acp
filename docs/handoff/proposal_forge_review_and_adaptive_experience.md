# Proposal — Forge Review UX & Student Adaptive Practice Experience

> **Proposal v1 (2026-07-07), for your review.** Python course first, designed to generalize.
> Grounded in: the Forge thread's locked decisions (fresh tagged banks; adaptivity as a
> separate delivery layer; cell-directed generation), the Question Creation Intelligence doc
> (C01–C25 gates, misconception bank, pool math), the Platform Student Experience doc (real
> UX + all 16 owner answers), and the product/pedagogy context docs. Companion constraint set:
> items are single-use once answered; FIB grading is exact-match; public submissions leak
> solutions; lint markers can't be disabled; tutorials + explanations are part of the item
> contract; runtime is Python 3.10.

---

# Part A — Forge reviewer experience

**Design principles**
1. **Machines gate, humans judge.** Every item arrives at a reviewer only after the C01–C25
   automated gates ran; the reviewer sees gate evidence, not raw claims.
2. **Reject with rule IDs, not prose.** Verdicts are structured (C-rule picker + optional
   note) so review feedback becomes the DSPy optimization metric with zero re-labeling.
3. **Review the student's view.** Item previews render in the real player/workspace skins
   (split-pane, explanation modal, Tutorial tab) — reviewers approve what students will see.
4. **The cell matrix is the home screen.** Review exists to fill (node × rung × axis) cells
   to depth N≥3; coverage, not queue-emptying, is the goal state.

## A1. Home: the coverage matrix

A grid per session: **rows = nodes** (from the registry), **columns = rung × axis**
(e/m/h × Read/Fix/Fill/Write for coding; e/m/h × format for objective). Each cell shows
`approved / in-review / gated-out` counts against the target depth (≥3). Color: green = full,
amber = partial, red = hole. Actions: click a cell → its items; "Generate for holes" →
work-orders straight to Forge for every red cell. A bank-level header shows: total items,
% gate-pass rate, coverage vs the old bank's floor, and cutover readiness.

## A2. The review queue

Filterable list: session · node · axis · rung · gate status (all-green / has-warnings) ·
item family · generation batch. Default sort: cells closest to complete first (finish cells,
don't graze). Each row: stem preview, tags, gate chips, family link (siblings shown together
so near-duplicates get caught by eye — dedup gate C19 already caps them).

## A3. The item card (what a reviewer sees)

**Common header:** node chip · rung chip · axis chip · role (primary/secondary) · family id ·
"born-from" work-order cell. Tags are read-only — items are generated *into* cells, never
re-classified in review.

**Gate panel (always visible):** C01–C25 as pass/fail chips; failing chips expand to
evidence — execution stdout, the FIB substitution-probe table (every alternate token tried →
its output), the mutant-kill matrix (which wrong-programs each test case kills), key-balance
stats for the batch (C10), dedup matches (C19). An item with red gates never reaches the
queue; amber (warnings) items do, flagged.

**Per-axis body:**
- **Write (coding):** stem rendered as the Description tab (Input/Output/Explanation sections,
  Constraints block, two samples) · reference solution · test-suite table (visible/hidden,
  weightage, edge-class checklist coverage, per-case mutant kills) · **Tutorial preview**
  rendered as the Tutorial tab (step 1/2/3) — the tutorial is reviewed WITH the item.
- **Read/objective:** the split-pane player preview (code right, stem left) · each option
  annotated with its **misconception-id chip** and the *simulated wrong path* ("a student who
  believes `LI-08 index-one-based` computes exactly this option") · **Explanation preview**
  rendered as the modal (commented code + bullets) · a lint-leak check flag (C-gate) for
  statically-lintable error answers.
- **Fill:** code with the blank's AST node highlighted · the exact-match answer string ·
  uniqueness-probe evidence (why no alternate string can be correct) · round-trip invariant ✓.
- **Fix:** the bug biography — buggy code, the misconception it embodies, diagnose-item
  distractors (incl. the wrong-diagnosis one), the fix options with "runs-but-misses-goal"
  annotations.

## A4. Verdicts

- **Approve** → item moves to the bank's `draft-approved` pool.
- **Edit** → inline edit (stem, options, tests, tutorial, explanation); saving **re-runs all
  gates**; the reviewer's final version is stored as a **gold demonstration** for the
  per-course DSPy program.
- **Reject** → mandatory C-rule(s) + optional note; rejection distributions feed generation
  tuning ("this batch fails C08 distractor-reachability 40% of the time on Sets nodes").

Throughput affordances: keyboard-first (a/e/r), side-by-side sibling compare, batch-approve
for all-green families (with sampling audit: every Nth all-green item still gets full review).

## A5. Bank versioning & cutover

States: `draft → in-review → active → archived` (never delete — response history stays
joined to archived items, per the Forge thread). Cutover checklist per session unit:
coverage matrix green · old-bank floor diff (nothing narrower) · novelty scan vs public
submissions + old bank (no near-duplicates of leaked solutions) · spot-check pass. One-click
cutover swaps the unit's active bank; students only ever see `active`.

## A6. Review analytics (feeds the DSPy loop + staffing)

Reviewer throughput, C-rule rejection distribution by node/axis/batch, gate-catch rate
(items auto-killed before humans — should climb as the generator learns), edit-distance of
reviewer edits (shrinking = generator converging), inter-reviewer agreement on sampled items.

---

# Part B — Student adaptive practice experience

**Design stance: minimal delta on a UX that already works.** The player shell, explanation
modal, difference checker, AI Tutor, debugger, and coding workspace all stay. What's replaced
is the *internals*: the legacy 15-question sampler, the linear question list, and the 80%
completion rule.

## B1. What changes vs today

| today (static unit) | adaptive unit (v1) |
|---|---|
| 15 sampled from 30 (legacy tags) | walk over the session's **nodes**, served from the tagged bank |
| QUESTIONS ATTEMPTED: N/15 | **node progress chips** (each node with e·m·h rung dots) |
| SCORE: N (+1 cards) | keep the +1 feedback; score is per-run, mastery is per-node |
| pass = 80% of questions | **complete = every node cleared to its target rung** |
| wrong → reveal → NEXT (item burned) | same reveal (keep it — it's honest feedback), but the walk serves a **fresh variant** at the right rung next |
| SKIP → requeue at end | same, unchanged |
| PRACTICE AGAIN = same run again | **PRACTICE AGAIN targets only weak nodes** |
| results = score gauge vs pass score | results = **mastery map** (node × rung grid) + targeted next steps |

## B2. The walk (v1 baked-in logic — deliberately simple, per the Forge thread)

Per node, the student holds a current rung (start: easy for new nodes; later, prior evidence
can seed it). Serve one item at the node's rung, axis rotated for variety (Read → Fill →
Fix → Write for coding; format-rotated for objective):

- **Correct** → step the node up one rung; at target rung → node cleared, move to next node.
- **Wrong** → answer revealed + explanation (existing UX), node stays; next item for that
  node is a **fresh variant, same rung** (never the same item — single-use is a platform
  fact). **Second consecutive miss** → step down one rung; at easy, a second miss marks the
  node **"revise"** and deep-links to the exact Reading-Material section (`tutorials_data`
  order) and the video timestamp.
- **Skip** → defer to end of run (unchanged semantics), no evidence recorded.
- Session unit target rung = **medium**; the pre-module-quiz pass raises targets to **hard**
  for the module's nodes (this is how "gold on the module quiz" gets supplied).

Pool math this implies (already in the intelligence doc): ≥3 fresh variants per
node × rung × axis; ~40–60 reviewed coding items per session, similar for objective.

## B3. Progress & completion UI

Header swap: "QUESTIONS ATTEMPTED N/15" → a compact **node rail** (chips named by key
takeaway, each with three rung dots that fill as cleared). END PRACTICE keeps partial
progress (nodes cleared stay cleared). Unit tick flips when all nodes ≥ target rung —
replacing the 80% rule with a rule that *means* something per-concept. (Platform change
needed: completion API takes a mastery predicate instead of a percentage — everything else
reuses existing unit plumbing, still shipped as `mcq_practice` / `coding_practice` units.)

## B4. Results screen (replaces the score gauge)

- **Mastery map:** node × rung grid — green cleared, amber in-progress, red revise.
- **Misconception feedback:** for wrong answers, the distractor's misconception tag renders
  as plain feedback ("you treated `list_b = list_a` as a copy — it's the same list").
  This is the payoff of born-tagged distractors; no extra authoring.
- **Targeted actions:** per weak node — "Practice again" (weak-node walk), "Re-read §" (deep
  link), "Re-watch" (timestamp), "Ask AI Tutor" (pre-seeded with the node + missed
  misconception as context).
- Keep date/duration/attempt history for continuity with today's modal.

## B5. Coding adaptive unit specifics

- The unit opens into the walk directly ("Next question for you") instead of a static list;
  a list view remains available showing attempted items + their nodes.
- **Tutorial gating preserves the pedagogy** ("try before looking"): Tutorial tab unlocks
  after the first failed Submit or on node-revise — not before the first attempt.
- Workspace unchanged: Run (visible+custom) / Submit (full suite), diff view, debugger,
  AI Tutor. Public submissions stay OFF for adaptive-bank items until a rebuild cadence is
  agreed (leak management).
- Lint-leak mitigation is generation-side (no statically-lintable bugs as error answers), so
  no platform dependency.

## B6. Telemetry to emit from day one (feeds the learner-stats phase)

Per attempt: item id · node · rung · axis · verdict · **misconception-id of the chosen
distractor** (objective) / failing test-case class (coding) · time-on-item · skips ·
tutorial/explanation opens · AI-Tutor invocations. This is exactly the dataset that later
(a) calibrates rung definitions empirically (replacing the structural prior), (b) validates
misconception frequencies against real students, and (c) rolls up per-product learner
behaviour for the product-context updates you plan.

## B7. Rollout suggestion

Pilot on **one session with a fully reviewed bank** (Sequence of Instructions is the natural
candidate — richest corpus, misconceptions well mapped) as an A/B against the static unit.
Success metrics: module-quiz gold rate, time-to-clear, revise-loop engagement, and item-pool
burn rate (validates the ≥3-variants depth). Then expand session-by-session as Forge fills
matrices.

---

## Dependencies & open items

1. **Node registry (WHAT rail)** — the walk and the matrix are keyed by nodes; registry
   authoring (module 1 exemplar first) is now the critical path.
2. **Difficulty-tagged re-export** (incoming) — calibrates the mechanical rung definitions
   before the first generated batch.
3. Completion-API change (mastery predicate vs percentage) — the one platform ask; everything
   else fits existing unit types.
4. Rebuild cadence policy for leaked items (public submissions) — propose: rebuild a
   session's bank when >30% of its active items have public accepted solutions.
