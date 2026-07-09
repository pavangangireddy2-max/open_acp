# Data Request — Learner Behaviour Intelligence (NIAT B3, AY 2025-26)

> **The question set for DA/DE** to source the fifth intelligence doc: how NIAT B3 learners
> actually used the Semester 1–2 courses through 2025-26. Outputs feed four consumers:
> **(F)** Forge calibration — empirical difficulty, discrimination, misconception frequencies;
> **(A)** Adaptivity design — walk parameters, pool burn, completion behaviour;
> **(P)** Product context — NIAT B3 audience realities per university/branch/delivery mode;
> **(G)** Pedagogy validation — do the observed teaching patterns (20-min blocks, quiz cadence,
> try-before-look) hold up against real behaviour.
> Each question below is tagged with its consumer(s). Version 1 — 2026-07-07.

**Scope:** NIAT B3 cohort · academic year 2025-26 · Semesters 1 & 2 · courses:
Computer Programming using Python · Data Structures and Algorithms using C++ ·
Web Application Development · Frontend Development Using React · Backend Development Using
Node, MongoDB · Database Management Systems · Introduction to Software Development ·
Math for CSE.

---

## 0. Ground rules — identity, joins, and data contract (settle BEFORE any extract)

The single known landmine: **course_ids have changed mid-lifetime.** And from the content
side we already know **unit_ids are reused across sessions** (e.g. one Classroom Quiz B
unit id appears under two different sessions) and **identical question content exists under
different question_ids** (duplicate clones across Practice/Quiz A/B/C). So:

1. **What is the stable join spine?** Confirm stability (never re-issued, never re-pointed)
   for: `question_id`, `unit_id`, `session_id`(topic_id), `test_case_id`, `code_id`,
   learner id. Which of these are stable across the course_id change? Which are not?
2. **Provide an ID crosswalk table**: old course_id ↔ new course_id (and any session/unit id
   migrations), with effective dates. All behaviour extracts should carry the *stable* ids
   and NEVER be filtered/joined on course_id — scope by **session_id lists** (we hold the
   authoritative session lists per course from the outlines).
3. **Content catalog snapshot for all 8 courses** (the structural spine): course → module →
   session (id, no., name) → unit (id, kind, title) → question (id, type) → test_case (id,
   is_hidden, weightage), plus per-question **content hash** (hash of stem+code+options).
   The content hash is the fallback join for re-issued/cloned items — without it,
   per-item stats fragment across duplicate question_ids.
4. **Event grain and exposure:** what attempt/event tables exist, at what grain, since when?
   Critical: the MCQ player **samples 15 of ~30** per run — we need per-question
   **exposure counts** (times served), not just answer counts, or every rate is biased.
   Same for coding: is "opened question" logged, or only submissions?
5. **Timestamps and timezone** (IST?), event-schema version history (what changed when —
   the sampler tagging is "years old"; are old events comparable?), and known backfill gaps.
6. **Privacy:** pseudonymous learner ids only; university/branch/section as attributes; no
   names/contacts. Confirm what's permissible for cohort cuts.
7. **Teaching calendar:** does a per-university/section class-schedule table exist (which
   session was taught when, offline)? Without it, "lag between class and practice" — the most
   NIAT-specific behaviour metric — can't be computed. (P, G)

## 1. Enrollment, reach, and the completion funnel (P)

8. Per course (via session_id scope): enrolled learners; % who opened ≥1 unit; per-session
   funnel across the unit sequence Video → Reading → Quiz A → Quiz B (→ C) → MCQ Practice →
   Coding Practice → (Module Quiz): open rate, completion rate, median time between units.
   Where exactly does the funnel leak?
9. Unit completion vs the 80% rule: distribution of final scores per unit; % of learners who
   hit FAILED and chose **PRACTICE AGAIN** vs **PROCEED TO NEXT**; % who never completed but
   moved on. (A — this is the behaviour the mastery rule replaces)
10. Per-session **progress %** over time (the topic progress ring): time-to-100% distribution;
    sessions that stall cohort-wide (candidate content problems). (P, G)

## 2. Question-level performance — the Forge calibration core (F)

For every question_id (all types), with exposure denominators:
11. **First-attempt correct rate** (empirical difficulty) and attempt counts. We will compare
    this against the incoming authored difficulty tags and our mechanical rung definitions.
12. **Discrimination**: correlation of item correctness with the learner's overall
    unit/session performance (point-biserial or simple quartile split). Items with ~zero or
    negative discrimination are broken-item candidates.
13. **MCQ option-selection distribution** — count per option_id, not just right/wrong.
    This is the highest-value single extract: each distractor is misconception-tagged in our
    bank, so option distributions = **empirical misconception frequencies per node**.
14. **TEXTUAL wrong-answer strings** — top-N normalized wrong answers per question with
    counts. (Mines misconceptions we haven't catalogued; validates format-trap items like
    `2.0` vs `2`.)
15. **Time-on-question** distributions (per type × difficulty): median, p90, and the
    <5s-answer rate (guess/rush signal).
16. **Skip behaviour**: skip rate per question; % of skips answered on requeue; requeue
    correct rate vs first-serve correct rate. (A — skip = deferral evidence)
17. **Post-reveal learning**: after a wrong answer + reveal/explanation, performance on the
    next question of the same unit — and, where clones exist (same content hash, different
    id), performance on the sibling later. Does the reveal teach? (A, G)
18. **Explanation opens**: open rate after wrong vs after correct; dwell time; correlation
    with subsequent performance. (G — is the explanation earning its place?)
19. Classroom Quiz A/B/C (live, in-class) vs MCQ Practice (self-paced) on comparable items:
    correct-rate and time deltas. (G — in-class attention vs self-paced)

## 3. Coding behaviour (F, A, G)

Per coding question_id and per learner-attempt chain:
20. Funnel: opened → first Run → first Submit → accepted. Conversion and median time at each
    step; distribution of **submissions-to-accept**; abandon rate after N failures.
21. **First-submit pass rate** (empirical difficulty for Write items) + which **test cases
    fail most** (per test_case_id, visible vs hidden split). Hidden-only failures = the suite
    is discriminating; visible failures = spec-reading issues. (F — validates test-suite
    design rules)
22. **Whitespace/format-only failures**: Wrong Answer where output diff is
    trailing-whitespace/newline-only (the platform tolerates trailing ws, so any remaining
    format failures are real signals — e.g. `2` vs `2.0`, missing lines). Quantifies grading
    friction vs logic failure. (F)
23. **Run vs Submit ratio**; **custom test case** creation rate and whether custom-case users
    solve faster. (G — self-verification behaviour the pedagogy encourages)
24. **Tutorial tab timing**: opened before first attempt / after first failure / never —
    per difficulty. (G — "try before looking" adherence; A — tutorial gating design)
25. **AI Tutor usage on coding items**: invocation rate, chat vs voice, turns per
    conversation, position in the attempt chain (before first run? after N failures?), and
    solve-rate/time deltas for tutor-assisted vs not. (P — NIAT AI-tutor reality; A)
26. **Visual debugger usage**: launch rate, per difficulty, correlation with solve rate. (G)
27. **Public Submissions views**: % of accepts preceded by viewing others' solutions; time
    between view and accept (< a few minutes = copy signal). Also: identical-code detection
    rate across learners if available. (F — novelty/rebuild cadence; A — integrity)
28. **Session-position effects**: solve rates for question 1 vs 2 within a unit (fatigue/
    ordering; order = array position). (A)

## 4. Consumption of learning resources (G, P)

29. **Video**: watch-through %, drop-off curve by timestamp (validates the 20-minute
    attention rule from the pedagogy intelligence), pause/seek clusters (≈ Quiz-Time slide
    moments?), playback speed distribution, rewatch segments.
30. **Reading Material ("Cheat Sheet")**: open rate, dwell, scroll depth if available;
    opened before quiz attempts or as post-failure reference? Section-level views if
    `tutorials_data` order is tracked. (G — is reading load-bearing or skipped?)
31. Resource → performance: quiz/practice performance of watchers vs skippers (same
    session), controlling for prior performance. (G)

## 5. Temporal and pacing behaviour — the NIAT-specific layer (P)

32. **Class-to-practice lag**: days between a session's offline class date (needs the
    teaching calendar, Q7) and the learner's practice completion. Distribution + drift
    across the semester.
33. **When do learners study**: activity heatmap (hour × weekday) — campus/lab hours vs
    hostel evenings vs exam-cram spikes; weekend behaviour. Device/platform split if logged.
34. **Semester pacing**: weekly active learners per course across the year; drop-and-return
    patterns; exam-window spikes; the sem-1 → sem-2 continuity rate per learner.
35. **Streaks/бinge**: % of practice done in ≥2-hour binges vs distributed sessions;
    correlation with retention of performance in later modules. (G — spaced repetition
    reality check)

## 6. Cross-course and cohort structure (P, F)

36. Same-learner **cross-course correlations**: Math for CSE ↔ DSA C++; Python (sem 1) ↔
    DSA C++ (sem 2) — the C++ course is taught as a Python-bridge, so quantify how Python
    mastery predicts C++ performance (validates the bridge pedagogy). Web Dev ↔ React ↔
    Node chain likewise.
37. Cohort cuts on every headline metric: **university × branch × delivery mode**
    (co/full/hybrid — NIAT B3 spans ~17 universities). Where do delivery modes diverge?
    (P — this becomes batch/university-aware product context)
38. **Struggling-cohort signature**: for learners in the bottom quartile of module-quiz
    outcomes, what early behaviours differ (lag, skips, tutor usage, video drop-off)? —
    the seed for early-warning and for Crux's future routing. (A, P)
39. Outcome linkage: module quiz / semester exam / IRC-progress joins per learner (stable
    ids only). Which practice behaviours predict gold-tier module quiz results? (A — the
    "pass everyone with gold" contract)

## 7. Support & affect signals (P, G)

40. **Helpful / Give Feedback / Bookmark** rates per question and unit; free-text feedback
    export if it exists (top complaint themes per course).
41. AI Tutor conversation topics (if categorized) per course/session — what do learners ask
    about most; voice vs chat adoption over time.

---

## Proposed export shape (so DE can scope effort)

Event-level tables (pseudonymous learner_id everywhere; stable ids + content hash):
- `attempts_objective`: learner, question_id, unit_id, session_id, ts, served_position,
  run_id, answer(option_id or normalized text), correct, time_on_question, skipped,
  requeued, explanation_opened, explanation_dwell
- `attempts_coding`: learner, question_id, ids as above, ts, action(open/run/submit/accept),
  cases_passed, failing_test_case_ids, code_snapshot_hash, custom_cases_count,
  tutorial_opened_at, tutor_invocations, debugger_used, public_submissions_viewed_before
- `resource_events`: learner, unit_id, session_id, resource_type(video/reading), ts,
  event(play/pause/seek/complete/open/scroll), position
- `unit_runs`: learner, unit_id, run_no, started/ended ts, score, outcome(passed/failed),
  action_after(practice_again/proceed)
- `catalog_snapshot` + `id_crosswalk` + `teaching_calendar` (dimensional)

## Priority if we must phase it

**Phase 1 (unlocks Forge calibration):** Q1–5 (contract), Q11–14 (difficulty, discrimination,
option distributions, wrong strings), Q20–22 (coding funnel + failing cases), with exposure
denominators.
**Phase 2 (unlocks adaptivity design):** Q9, Q16–17, Q24–28, Q39.
**Phase 3 (product + pedagogy):** everything else.

## Known traps for the DA/DE (from the content-side mining)

- Never join on course_id (changed); scope by session_id lists we supply.
- Unit_ids are REUSED across sessions — always carry (session_id, unit_id) pairs.
- Duplicate question content exists under different question_ids — use the content hash to
  aggregate behaviour for "the same item".
- The MCQ player served a sample of 15 (legacy tagging) — every per-item rate needs the
  exposure denominator, and the sampling tag itself may be a confounder (which 15 got served
  was not random).
- A/B/C quiz forms are parallel forms, not difficulty tiers — don't treat form as level.
- Some items are known-defective (wrong keys, non-firing traps — do-not-port list in the
  question-intelligence doc): exclude or flag them in performance aggregates, since learner
  "errors" on them are not learner errors.
