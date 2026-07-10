# Learner Behaviour Intelligence — Python Course

> **Standalone handoff document (the fifth intelligence doc).** How NIAT 2025 (Batch 3)
> learners actually moved through **Computer Programming using Python** across Semesters 1–2
> (Aug 2025 – Jun 2026) — the empirical layer that calibrates the WHAT rail (node registry:
> difficulty tiers, pool sizes, item counts per node × level × axis) and validates the
> pedagogy.
>
> **What this doc is NOT:** the node registry itself, nor the Forge generation rules (HOW
> rail — see `context_question_intelligence_python.md`). This doc is the *evidence base* the
> registry is authored against.
>
> **Provenance & status:** built against the DA/DE team's live **ELP** (Extraction &
> Learning-behaviour Product): `NIAT 2025 Learner Behaviour Summaries ELP.xlsx` (the
> derivation spec — 6 sheets: README, Unit/Topic/Course Level, Tracking Gaps, Source Tables;
> generated 2026-07-08 07:29 IST) and the `learning-behavior.md.docx` worked-example
> narrative. **This is not "spec a new pipeline" — it is "run an existing one for Python and
> tag it to our nodes."** Most of what the registry needs is already tracked.
>
> **Reading rule:** every metric below carries the ELP's own **Derivation Status** —
> ✅ **Yes** (derivable now), 🟡 **Partial** (derivable with a stated caveat/proxy),
> ❌ **Not tracked** (needs future instrumentation; do not design as if present).
>
> Generated 2026-07-08. Version 1.

---

## 1. The point of this doc: analytics → registry knobs

The node registry is authored from the Course Outline's key-takeaways (the WHAT rail). But
several of its parameters cannot be set from outcome statements alone — they are empirical.
This doc exists to set exactly those parameters. The spine:

| Registry knob (what we must decide) | Analytic that sets it | ELP status |
|---|---|---|
| **Easy / Medium / Hard cut points** | Continuous first-attempt-correct **rate** distribution per item + authored-vs-empirical mismatch | ✅ Yes |
| **Which misconceptions become mandatory items/distractors** | MCQ option-selection distribution → misconception prevalence per node; textual top-N wrong strings | ✅ Yes |
| **Axis emphasis per node** (Read/Fix/Fill/Tweaked) | Error-type distribution (syntax→Read/Fill; logic→Fix/Tweaked) — *proxy only* | 🟡 Partial |
| **Rung / transfer-difficulty need** | In-Course vs Exam gap per topic | 🟡 Partial (Sem-2 caveat, §6) |
| **# items per node × level cell** | Attempts/retries per learner; % repeated after failure | 🟡 Partial (per-node "fresh items to clear" not native) |
| **Whether an item earns a pool slot** | Discrimination (point-biserial / quartile delta); broken-item rate | ✅ Yes |
| **Pool-cleaning (drop dead slots)** | Course question-bank action list (retain/revise/drop/review) | ✅ Yes |
| **Node *boundaries* (empirical check on the outline)** | **Item co-failure clustering** | ❌ Not tracked — **our one net-new ask** (§5) |
| **Pool refresh cadence (novelty burn)** | First-attempt-rate inflation over item age vs public submissions | ❌ Not tracked — future (§7) |
| **Level L1–L5 depth** | — (design construct; behaviour only forward-validates ordering) | n/a |

**Honest limits, stated up front:**
- **Level (L1–L5) is not mineable.** It is a Crux design construct; no level tags exist in
  B3. Behaviour can only *validate the ordering* once Forge ships born-tagged items.
- **Axis is a prior, not a measurement.** B3 items carry no axis tags. Error-type split
  gives a per-node lean (syntax-heavy vs logic-heavy); it does not assign axes.
- **Coding is funnel-only** (§4). Per-test-case failure anatomy is explicitly not synced.

---

## 2. What the ELP already delivers (adopt as-is)

The DA/DE ELP is a three-grain product — **Unit → Topic(session) → Course** — with 23/13/15
metric rows respectively. These are already `Yes` and map onto our knobs; **we adopt them,
we do not re-spec them.**

### 2.1 Difficulty calibration — the core knob, already built ✅
- **First-attempt correct rate**, computed *separately by question_type*, per item
  (Unit level). This is the continuous rate our easy/med/hard cut points fall out of — not
  the docx's binary "≥50% needed ≥2 attempts" flag (which cannot separate medium from hard).
- **Authored-vs-empirical difficulty mismatch rate** (Topic/Course level): the ELP already
  compares authored e/m/h tags against empirical first-attempt bands and lists examples.
  → This directly validates or overrides the incoming difficulty tags. **The cut-point knob
  is productized; we consume its output, we don't compute it.**
- **Exposure denominator is derivable.** `question_start_datetime` **exists** (confirmed by
  owner, 2026-07-08), so opened/exposed-learner counts are available and the legacy
  **15-of-30 MCQ sampler is correctable** — every per-item rate can be reported on
  times-served, not times-answered. This is the precondition that makes calibration
  trustworthy; it is met.

### 2.2 Discrimination & bank health — the pool-slot gate ✅
- **Point-biserial** (or high-vs-low quartile correct-rate delta) per item.
- **Broken / low-discrimination item rate** per topic; **course question-bank action list**
  ranking every item retain / revise / drop / **review**.
  → This *is* the pool-cleaning knob (drop zero-information ceiling items and broken-key
  floor items). Registry pool sizes are counted **after** this filter, never before.

### 2.3 Misconception evidence — the item-authoring seed ✅
- **Option-selection distribution** by `option_id`, first-attempt and all-attempts,
  correct/distractor split.
- **Misconception prevalence per node**: distractor selections mapped to a misconception tag
  ÷ relevant attempts (this joins directly to our ~310-entry misconception bank in the HOW
  rail). Topic/course roll-ups sort nodes by prevalence.
- **Textual top-N normalized wrong strings** with counts and example variants → mines
  uncatalogued misconceptions and validates format-trap items (`2.0` vs `2`).
  → Each high-prevalence distractor becomes a **mandatory distractor** or a **Fix-axis seed**
  for its node.

### 2.4 Time, pacing, help, resources, cohort — free context ✅ (except where noted)
- **Time-on-question**: median, p90, **<5s answer rate**, long-tail rate (Unit). Covers your
  ">2 min coding floor / <5s rush" instinct natively. (No comet-browser field, but the <5s
  and long-tail rates are the rush/automation signal.)
- **Class-to-practice lag** ✅: the teaching-calendar table exists
  (`niat_and_intensive_offline_section_wise_daily_learning_schedule_details`). The
  most NIAT-specific pacing metric — flagged earlier as a likely-missing landmine — is live.
- **Help-seeking is already split into separate clusters** (this is what the docx's single
  "≥30% Help" column hides): **AI-tutor usage rate** ✅ (invocation %, turns, before/after
  attempt if timestamp chain joins), **tutorial-steps completion** 🟡 (proxy), **feedback /
  helpful / bookmark** ✅. Keep them separate — tutorial-before-attempt (good, try-then-look)
  and solution-peek (copy) are opposite signals and must not be re-aggregated.
- **Video watch-through** 🟡 (last-watched-% proxy; no true drop-off curve), **reading
  consumption** 🟡 (completion proxy, no scroll depth).
- **Cohort cuts** ✅ by university / branch / section / delivery mode on every headline
  metric — this is how the registry becomes batch/university-aware and how the
  struggling-cohort signature is built.
- **Retries** ✅: attempt_count, median attempts, % with >1 attempt, % repeated after failure.
  **Failed → practice-again vs proceed** 🟡 (partial) — the behaviour the mastery rule
  replaces.

---

## 3. Worked example — the ELP output shape (from the docx narrative)

The `learning-behavior.md.docx` is a **capability sample** (cohort size, session count, data
sources, known-gaps still `xx`/blank), so treat its specific numbers as *illustrative of the
report shape*, not delivered Python B3 values. But the shape is exactly what we consume, and
the two dominant findings are almost certainly real (they recur across every metric):

- **OOP cluster (Sessions 35–44) — the dominant break.** All 10 sessions flagged 🔴.
  Completed-users % falls to 54–63%; 25%ile completion 48–53%; rewatch 46–54% (vs ~20%
  baseline); doubts/100 triple. Sentiment negative, keywords *"video didn't match practice"*
  and *"too much jumped at once."* Named misconception tags with % share:
  `missing-self-parameter` (S35, 58% of wrongs, 64% syntax), `shared-state-confusion`
  (S38, 63%, 70% **logic**), `override-signature-mismatch` (S44).
- **Recursion cluster (Sessions 51–56) — most severe by completion floor.** 25%ile as low as
  40–47% (S53 = 43%, course low). `missing-base-case` (S51, 74% of wrongs);
  `recursion-iteration-conflation` (S53, 55%). S51 notable: 0 items crossed the help
  threshold — students retry independently, so in-course and exam numbers agree.

**How this drives the registry:**
1. **Node priority is decided.** OOP and Recursion nodes get the **deepest pools, most
   rungs, and every catalogued misconception turned into an item.** Foundational sessions
   (1–4, ~85% completion) get lean pools.
2. **Axis lean per node comes from the error-type split.** S35 = 64% syntax → OOP-intro
   nodes want **Read/Fill** items (spot the missing `self`). S38 = 70% logic (valid code,
   wrong behaviour) → those nodes want **Fix/Tweaked** items (shared-state bug hunts). This
   is the proxy, not an axis assignment.
3. **Misconception tags are directly item-authorable** — each becomes a mandatory distractor
   / Fix-axis seed for its node, joined to the HOW-rail bank.

---

## 4. Coding: funnel-only — the biggest correction to the brainstorm ⚠️

Stated three times in the ELP (README "Important limitation"; Tracking Gaps rows 1–3):
**raw submitted code and per-test-case pass/fail are NOT synced.**

**Derivable now (✅/🟡):** coding acceptance funnel — opened/attempted → first submit →
accepted; **first-submit pass rate**; submissions-to-accept; abandon-after-N. (ELP status
Partial — depends on which attempt tables carry the coding action grain.)

**NOT derivable (❌ — do not design as if present):**
- which **test_case_id** fails, and visible-vs-hidden split;
- **whitespace / format-only** failure rate (`2` vs `2.0`, missing line);
- raw code / clone detection.

→ The brainstorm items *"most failed test cases"* and *"most time to pass a test case"* are
**dead against current instrumentation.** They move to §7 (future). For now, coding
difficulty = first-submit pass rate + submissions-to-accept, and suite quality is inferred
from the HOW-rail design rules, **not** measured.

---

## 5. The one net-new ask: item co-failure clustering ❌→ask

Everything above is "run the ELP for Python." The single registry-critical analytic the ELP
does **not** have — and the only one worth a genuine new ask — is:

> **Item co-failure matrix / clustering:** for pairs (or clusters) of items, the degree to
> which the *same* learners fail them together (co-failure lift, or a learner×item wrong
> matrix reduced to clusters). Aggregate by **content_hash**, on **first-attempt** outcomes,
> engaged-attempts only.

**Why it is worth asking for specifically:** every other metric *annotates* the outline's
declared sessions/nodes. Co-failure is the only one that lets behaviour **challenge** the
node boundaries — if items the outline places in two different nodes are failed by the same
learners, they are empirically one node (or share a hidden prerequisite). It is the
difference between the registry describing the syllabus and the registry describing how the
subject is actually learned. It is buildable from tables the ELP already uses
(`all_users_question_attempt_details...` + first-attempt correctness), so the ask is
incremental, not a new pipeline.

---

## 6. Caveat to confirm before leaning on exam-gap

The docx's most valuable rung-design signal — **In-Course vs Exam gap** per topic (big gap =
hint-inflated solves that don't transfer → node needs harder/transfer rungs; small gap =
honest difficulty) — depends on
`curriculum_ops_niat_2025_users_batch_wise_skill_and_graded_assessment_scores`. The Source
Tables sheet notes: **"Sem-1 graded … Sem-2 onwards noted as offline/not present."**

OOP (S35–44) and Recursion (S51–56) sit **late** in the course — likely Semester 2. So the
exam-gap numbers in the docx for exactly the two dominant breaks **may not be derivable.**

**Action:** confirm the Sem-1/Sem-2 session boundary against
`niat_schedule_details_as_per_prod_sequence` **before** any registry rung argument rests on
exam-gap. If OOP/Recursion are Sem-2, treat their exam-gap as illustrative and fall back to
completion-floor + doubt-volume + error-type as the rung signal.

---

## 7. Future instrumentation (mirrors the ELP's own Tracking Gaps — do NOT design against)

Parked until the DA/DE team instruments them; listed so the registry doesn't assume them:

| Metric | Why parked | Table change the ELP itself specs |
|---|---|---|
| Per-test-case failure anatomy; visible/hidden split | Coding pass/fail not synced | `failing_test_case_ids`, `passed_test_case_ids`, visible/hidden flag, result type per submit |
| Format-only coding failures | No expected-vs-actual diff | `failure_reason` + normalized diff category (whitespace/precision/missing-line/type/logic) |
| **Novelty burn** (first-attempt-rate inflation over item age vs public submissions) | No item-age longitudinal join | item first-served date + public-submission-view events |
| Explanation open/dwell | Not tracked | `explanation_opened`, `dwell_time`, `reveal_ts`, next-same-node performance |
| Reading scroll depth/dwell | Only completion proxy | open, scroll depth, active dwell, section, before/after attempt timing |

---

## 8. The handoff DA/DE needs from us (our deliverable, not their ask)

The ELP's atomic grain is **Unit** and its aggregation grain is **Topic (= session)**. We
author the registry at **key-takeaway node** grain — a session holds several nodes. The
mismatch is ours to fix:

1. **Hand DA/DE our node map** (Node_ID · session_id · the questions/units under it),
   authored from the Course Outline key-takeaways. Their ELP already carries
   `course/session(topic)_id + unit_id` and can attach `content_hash`; adding our Node_ID as
   a tag on the question spine lets the next Python run land **per-question data on our
   nodes** with no re-plumbing.
2. **Scope by session_id lists, never course_id** (course_ids changed mid-lifetime — the
   ELP's own Join Caution). We hold the authoritative session lists from the outlines.
3. **Carry `content_hash`** so duplicated/cloned questions (19–34% dup) aggregate as one item
   — otherwise per-node stats fragment.

**Net sequencing:** we are not blocked on a new pipeline. We are blocked on (a) DA/DE running
the existing ELP for Python with real numbers, (b) our node map so it is node-tagged, (c) the
one co-failure ask (§5), (d) the Sem-1/2 boundary confirmation (§6). (a) and (b) can run in
parallel with registry authoring from the outline; behaviour then refines difficulty tiers,
pool sizes, and node boundaries on the draft.

---

## Appendix — source-of-truth files

- `knowledge/raw/corpora/NIAT 2025 Learner Behaviour Summaries ELP.xlsx` — the derivation
  spec (Unit/Topic/Course metrics with Yes/Partial/Not-tracked status; Tracking Gaps; Source
  Tables). **Authoritative for what is derivable.**
- `knowledge/raw/corpora/learning-behavior.md.docx` — worked-example narrative (Tier
  1/2/3; OOP + Recursion findings). Capability sample — shape real, numbers illustrative.
- `docs/handoff/workbench/requests/learner_behaviour_data.md` (v1) — the earlier 40-question
  data request. **Superseded in framing by this doc**: most of its Phase-1 asks are already
  ELP `Yes`. Retain for the export-shape appendix and the ID-crosswalk landmines.
- `docs/handoff/intelligence/stacks/programming_algorithms/courses/python/question_intelligence.md` — the HOW rail; the misconception
  bank this doc's option-distributions join to.


---

## Co-failure pilot — DELIVERED & ADJUDICATED (2026-07-10)

The net-new ask landed (DE team, Sonnet 5 pipeline; delivery in `workbench/requests/
cofailure check - share content/`, full review + content adjudication in
`workbench/reviews/review_cofailure_pilot.md`). Headlines for this doc:

- **Pilot scope:** 4,812 learners × 584 questions × 5 sessions (Conditional, Nested
  Conditional, Loops, For Loop, Understanding Coding Question Formats); 170,236 pairs
  computed; 71,891 delivered above floor. Pipeline is sound; N=300 confidence floor
  empirically justified (75th pct of overlap; expected both-fail cell ≈ 12).
- **No cross-session merges** — conclusion holds, but for the corrected reason: the
  high-lift cross pairs (up to 7.85) are rare-item artifacts (all 28 lift>4 pairs involve a
  <5%-fail item; median phi ≈ 0.11). Rank by **phi + both-fail cell ≥ 10**, never lift alone.
- **One split candidate confirmed at content level:** a 6-item sub-cluster in the Loops
  (while) session = *control-variable state reasoning*, whose seams map exactly to bank
  families **LP-06** (uninitialized → NameError) and **LP-04** (runs-once). Not clones.
  Registry consequence: s13 likely holds ≥2 nodes (trace/accumulation vs state/termination
  semantics). First empirical proof that session ≠ node.
- **`e4a74737` rare-item lesson:** its 0.8% fail is an answer-leak artifact (verbatim
  NameError option + lint-marker leak) — rare-item screens must check for leak explanations.
- **Full-scale gates (before the 3,849-question run):** content-hash on the question spine
  (clone rate 19–34% would forge merge signals — critical path), defective-item exclusion
  (do-not-port list handoff), phi+cell-floor ranking, sub-cluster detection cross-session
  (not median rollups). `time_spent` was 100% null in this extract — rush filter needs a
  source fix if wanted.
