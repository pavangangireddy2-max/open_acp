# Proposal — KPI System v3: Ownership Reconciliation

> Reconciles the HOD's existing KPI system (naming convention + V2 tracker, 31 KPIs, 7
> categories) and the SDE Learning Systems career framework with the org design — and adds
> the two ownership lanes the tracker is missing: **product-specific** and
> **engineering-specific** metrics. Sources archived at
> `knowledge/raw/corpora/department/` (career_framework, kpi_naming_convention,
> kpi_tracker_v2). Proposal v1 — 2026-07-10.

## 1. Census of the current tracker (the gap, quantified)

31 KPIs across 7 categories. Ownership as-implied today:
- **28 of 31 tagged "All"** — effectively content-team-owned averages.
- **Product-specific: 3** (NIAT Graded Assessment Achievement, NIAT University Curriculum
  Compliance/BOS, Launchpad WAU).
- **Engineering-owned: ~2** (Platform Runtime Cost Per Active Learner; half of Learning
  Environment Satisfaction).
- SLE, Ops, Pedagogy, Designers: implied but never named.

The HOD's instinct is right: the naming convention *supports* product/audience scoping
([Product]: [Audience]: [Metric]) but the tracker barely uses it, and engineering has no
lane at all.

## 2. The single structural fix: an Owner column

Add one column to the tracker: **Owner = exactly one org-design team** (Stack team ·
Central Ops · SLE · NIAT/GRIT pod · Academy/Intensive pod · Platform Eng · Pedagogy ·
Designers/PMO · HOD). Category stays a classification; Owner is accountability. A KPI with
two owners has none. Where a metric genuinely spans teams, the second team appears as
"informed", never co-owner.

## 3. Existing 31 → owners (+ flags found while mapping)

| # | KPI (tracker) | owner | note |
|---|---|---|---|
| 1 | % Learners in Ideal Engagement Segment | Product+DA | keep — good leading indicator |
| 2–3 | Summative/Formative Skill Assessment Achievement | Stack teams | per owned domains |
| 4 | Content-Assessment Alignment % | Stack + Pedagogy (informed) | |
| 5 | NIAT Graded Assessment Achievement | NIAT pod | |
| 6 | Launchpad Weekly Active Users | product pod | ⚠ **name/definition mismatch**: name says WAU, definition describes *leads generated* — pick one |
| 7 | Learning Engagement Effort (LE) | Product+DA | |
| 8 | Course Completion Rate | SLE | product pods informed |
| 9 | Pedagogy Initiative Impact | Pedagogy team | |
| 10 | Learner Accessed Content Completion (video) | SLE | diagnostic under #8 |
| 11 | Practice Attempt-to-Completion | SLE | Platform informed (environment friction) |
| 12 | Learning Environment Satisfaction | **Platform Eng** | move from content ownership |
| 13 | No. of Presentations & Cheatsheets Delivered | Stack teams | ⚠ name says count, definition says hours — fix |
| 14 | Vernacular Content Hours | Stack (CSI) | |
| 15 | Practice & Assessment Pieces Delivered | Central Ops | **refine: count APPROVED (gate-passed) only** |
| 16 | Branding Content Assets | Designers/PMO | |
| 17 | Cost Per Presentation | Ops + Stacks | ⚠ definition says per hour — align |
| 18 | Cost Per Cheatsheet | Stack (CSI) | ⚠ definition says vernacular hour — align |
| 19–20 | Cost Per MCQ / Coding Question | Central Ops | **refine: cost per APPROVED item, numerator includes rejected/regenerated attempts** — else the metric rewards shipping junk |
| 21 | Cost Per Branding Asset | Designers/PMO | |
| 22 | Platform Runtime Cost Per Active Learner | **Platform Eng** | move category too (§5) |
| 23 | Feedback Resolution Efficiency | Quality stewards (Ops-run) | companions added in §6 |
| 24 | R&D Initiative Impact | Central Ops | |
| 25 | Industry Update Adherence | Stack teams | |
| 26 | NIAT University Curriculum Compliance | NIAT pod | |
| 27 | Tech Stack Freshness | **split**: content references → Stacks; IDE/env versions → Platform Eng | |
| 28 | Stakeholder Request Fulfillment | product pods | HOD informed |
| 29 | Cross-functional Sprint Delivery | HOD/PMO | measures partner bandwidth |
| 30 | Operations & Growth Cost | HOD | |
| 31 | Creative Resource Utilisation | Designers/PMO | |

## 4. NEW — Product-pod owned KPIs (naming convention applied)

| KPI name | category | unit | freq | note |
|---|---|---|---|---|
| NIAT: B3: Module Quiz Gold-Tier Rate | Business Impact | % | Monthly | **the program's north star**, per course; extend to B4, then other products |
| NIAT: B3: Class-to-Practice Lag Median | Content Effectiveness | Days | Monthly | needs the teaching calendar (already a DE ask) |
| NIAT: B3: University Engagement Spread | Business Impact | Ratio (p90/p10 LE) | Monthly | across ~17 universities; spread, not average — averages hide dying sections |
| NIAT: Delivery Quality Theme Closure Rate | Stakeholder Alignment | % | Monthly | instructor/student feedback themes closed at ROOT CAUSE (culture loop's 4-checkbox close) |
| Academy: 2.0: Live Session Attendance Rate | Content Effectiveness | % | Monthly | live sessions are Academy's value prop |
| Intensive: Offline: Cohort On-Track Rate | Content Effectiveness | % | Monthly | cohort-paced product |
| [Product]: Content Satisfaction Score | Business Impact | Score | Monthly | per product, from existing in-app ratings |
| Launchpad: Content-Driven Leads | Business Impact | Count | Monthly | the fixed version of #6 (if leads is the intent) |

Adaptive rollout adds (when live, SLE-owned but product-scoped): [Product]:
Adaptive-vs-Static Learning Lift (%).

## 5. NEW — Engineering-owned KPIs (proposed 8th category: **Platform Engineering**)

The 7 categories have no home for reliability — stuffing SLOs under "Content Efficiency"
is why engineering has no lane. Add one category; move #12 and #22 into it.

| KPI name | unit | freq | note |
|---|---|---|---|
| All: Grader & IDE Availability | % | Monthly | the SLO students feel first |
| All: Submit-to-Verdict P95 Latency | Seconds | Monthly | |
| All: Platform Incident Rate / MTTR | Count · Hours | Monthly | pairs with the culture register |
| All: **Contract-Debt Burndown** | Count/quarter | Quarterly | the named debts: per-item lint control, completion-predicate API, per-test-case sync, grader-normalization docs |
| All: Data Sync Completeness | % | Monthly | events synced vs emitted (test-case results, question_start) — joint with DA/DE |
| All: AI Serving Cost per 1K Tutor Interactions | INR | Monthly | AI infra lane of cost |
| (moved) Platform Runtime Cost Per Active Learner | INR | Monthly | from Content Efficiency |
| (moved) Learning Environment Satisfaction Score | Score | Monthly | from Content Effectiveness |

## 6. NEW — Ops/system KPIs into existing categories

| KPI name | category | unit | note |
|---|---|---|---|
| All: First-Pass Gate Rate | Content Efficiency | % | generator quality; the GenAI-orchestration pillar made measurable |
| All: Approved Items per Week (Coverage-Fill Velocity) | Content Velocity | Count | replaces raw "pieces delivered" as the honest unit |
| All: Repeat-Issue Rate | Content Efficiency | % | the culture north star (→0) |
| All: Root-Cause Closure Rate | Content Efficiency | % | % closures with an artifact change — the honesty meter |
| All: Judge–Reviewer Agreement | Content Effectiveness | % | Pedagogy team; calibration health |
| All: Intelligence Doc Freshness (≤24h) | Executive Ops | % | EOD-loop compliance |

## 7. Career-framework linkage (ratings consume these KPIs)

- **Pillar 1 Performance (50%)** ← Business Impact + Effectiveness KPIs scoped to the
  person's portfolio (Impact on Learning Outcomes = gold-tier + assessment achievement;
  Feedback Resolution = #23 + Repeat-Issue Rate; Industry Upgrades = #25; Pedagogy R&D = #9).
- **Pillar 2 Role Competence (25%)** ← Velocity + Efficiency lanes; its **GenAI
  Orchestration (20%)** sub-pillar becomes measurable as First-Pass Gate Rate + cost-per-
  approved-item trend + team velocity multiplier vs baseline.
- **Pillar 4 Culture (10%)** ← Root-Cause Closure Rate + framework adherence.
- **Targets must be normalized by the framework's own complexity multipliers** (English/
  Aptitude 1.0x … System Design/DS&Algo/DS-ML 2.5x): raw velocity or cost comparisons
  between the English team (7, 1.0x) and DS&Algo (10, 2.5x) are meaningless without it.
  Publish the multiplier next to every velocity/cost target in the tracker.

## 8. Rollout

1. Add the **Owner column** to the V2 tracker and fill it from §3 (one sitting).
2. Fix the three name/definition mismatches (#6, #13, #17–18) before Q2 targets are set.
3. Add §4–§6 rows with Q2'26 budgets; create the **Platform Engineering** category.
4. Wire the system-computed subset (gate rates, repeat-issue, freshness, gold-tier) to
   auto-fill from dashboards as those land — hand-entry is interim, not the design.
