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

## 9. Baseline revision (2026-08-11) — deltas vs the v2 tracker

The HOD's revised KPI library (archive: `knowledge/raw/corpora/department/
org_five_portfolios_kpi_baseline_2026-08.md`) resolves items §3 flagged and adds a section:

- **Deprecations pending:** #2 Summative and #3 Formative Skill Assessment (→ % Ideal
  Engagement Segment), #8 Course Completion Rate (→ LE).
- **Mismatch #6 resolved as WAU** — "unique learners engaging with ≥1 learning unit/week"
  (opposite of §3's leads reading; the §4 "Launchpad: Content-Driven Leads" row is
  therefore optional/future, not a replacement).
- **Mismatch #13 resolved as hours** — renamed "Learning Content Hours Delivered".
- **Mismatches #17–18 resolved by renaming** — "Cost Per Learning Hour Produced"; #18
  superseded by CSI's "Cost Per Vernacular Content Hour".
- **New CSI section (6 KPIs):** NIAT Program Delivery Gap Rate (target 0%) · NIAT BOS
  Credit Acceptance Rate · Cost Per BOS Approval · Issue Resolution TAT · Cost Per
  Vernacular Content Hour · Framework Compliance Rate (NHQRF/Woolf).
- **Content-Assessment Alignment** redefined vs formative scores, attempted-both learners.

## 10. Baseline library → five-portfolio mapping (the "next task")

One owner-portfolio per KPI; execution notes where a central team does the work. The 20
§4–§6 additions slot into these same lanes when adopted (noted in brackets). NIAT
**organizational** KPIs are pending from the HOD — the cross-map to those is open.

| portfolio | owns (from the 36-KPI baseline) |
|---|---|
| 💡 Learning Domains | Summative & Formative Achievement (until deprecated) · Content-Assessment Alignment · Pedagogy Initiative Impact · Learning Content Hours · Vernacular Content Hours (CSI executes) · Cost Per Learning Hour (ACP informed) · Cost Per Vernacular Hour (CSI executes) · Industry Update Adherence · Tech Stack Freshness (content-reference half) |
| 🤖 Agentic Content Platform | Practice & Assessment Pieces Delivered (refine: approved-only) · Cost Per MCQ · Cost Per Coding Question · R&D Initiative Impact · Feedback Resolution Efficiency [+ First-Pass Gate Rate · Coverage-Fill Velocity · Repeat-Issue Rate · Root-Cause Closure · Judge–Reviewer Agreement · Doc Freshness] |
| 🎓 Learning Platform | % Learners in Ideal Engagement Segment · Learning Engagement Effort (LE) · Course Completion (until deprecated) · Learner Accessed Content Completion · Practice Attempt-to-Completion [+ Adaptive-vs-Static Lift on launch] |
| 🚀 Product Learning Experience | NIAT Graded Assessment Achievement · NIAT University Curriculum Compliance · Stakeholder Request Fulfillment · Launchpad WAU ⚑ · CSI program lane: Delivery Gap Rate · BOS Credit Acceptance · Cost Per BOS Approval · Issue Resolution TAT · Framework Compliance [+ Gold-Tier Rate · Class-to-Practice Lag · Engagement Spread · Theme Closure] |
| 🛠️ Developer Platform | Learning Environment Satisfaction · Platform Runtime Cost Per Active Learner · Tech Stack Freshness (IDE/env half) [+ Availability · P95 Latency · Incidents/MTTR · Contract-Debt Burndown · Data Sync Completeness · AI Serving Cost] |
| dept shared services | Designers/PMO: Branding Assets Delivered · Cost Per Branding Asset · Creative Utilisation. HOD/PMO: Cross-functional Sprint Delivery · Operations & Growth Cost |

Open flags: (a) **Launchpad WAU** — Launchpad is absent from PLE's stated product list
(NIAT/Intensive/Academy); confirm its portfolio home. (b) **% Ideal Engagement Segment +
LE** — assigned to Learning Platform as the engagement-system owner, product pods and
HOD informed; flip to PLE if the HOD wants outcome ownership product-side. (c) CSI KPIs
keep CSI as the executing team; the portfolio row is accountability, not execution.

## 11. Org-level cascade (2026-08-11) — NIAT targets ↔ department KPIs

NIAT organizational targets for Jul'27 received (archive: `knowledge/raw/corpora/
department/niat_org_targets_jul2027.csv`): employability per batch, CSAT (academics 4.5,
university relations 4 layers), NSPI bands, co-curricular counts (AI&Robotics 120, GSoC
200, ICPC 120, GRIT Novice 5,000, hackathons 200), dropout <1.5%, DSO.

**Four-tier architecture (proposed):**
- **Tier 0 — Org outcomes** (NIAT targets, Jul'27 horizon): owned by the NIAT org; the
  department is a *contributor*, never the owner.
- **Tier 1 — Department KPI library** (the 36-KPI baseline + additions, 8 categories):
  owned inside the department. Each KPI carries a **linkage tag** to Tier 0:
  `drives` (causal), `guards` (risk containment), `leads` (leading indicator), or
  `internal` (health metric with no org cascade — legitimate; forcing fake cascades is
  how KPI systems rot).
- **Tier 2 — Portfolio lanes** (§10): accountability for Tier-1 KPIs.
- **Tier 3 — Initiative metrics** (monthly roadmaps): every roadmap item ships naming the
  Tier-1 KPI it moves. (Developer Platform Aug roadmap pending — will populate its lane.)

**Department ↔ org cross-map (the dept-relevant Tier-0 rows):**

| NIAT target (Jul'27) | dept linkage | via (Tier-1 / portfolio) |
|---|---|---|
| Academics CSAT 4.5 | **drives** (dept-primary) | content satisfaction, LE, delivery-quality theme closure — LP + LD + PLE |
| Employability B3 80% / B4 80% | drives, lagged | skill mastery chain: gold-tier rate, assessment achievement, adaptive lift — LD + LP |
| NSPI/SPI bands (30/40/30) | **drives, dept-primary** | SPI = dept-authored assessments (classroom quiz 10% + module quiz 15% + skill assessments 25% + FSA 50%); gold-tier & mastery chain — LD + ACP + LP. ⚑ deprecation tension: Summative/Formative Achievement retire while SPI is 75%-weighted on them — keep an SPI-component view (decoded: corpora/products/niat/nspi_decoded.md) |
| GRIT Novice Badge 5,000 | **drives, direct** | PLE — literally its GRIT Practice roadmap item |
| ICPC Regionals 120 | drives | LD (DS & Algo domain) |
| AI & Robotics products 120 | drives | LD (Robotics domain) |
| GSoC selects 200 | contributes | LD (MERN/Java/open-source readiness) |
| Hackathons top-3 200 | contributes | LD (GenAI) + PLE |
| University Relations CSAT L1–L3 | **guards** | CSI lane: BOS credit acceptance, delivery gap, issue TAT, curriculum compliance — PLE |
| Student drop-off <1.5% | leads | LE / ideal-engagement segment as early-warning — LP |
| Non-academics/Infra/Parents CSAT, DSO | out of dept scope | program ops / finance |

Cadence bridge: Tier 0 is a 2-year target; Tier 1 is monthly. Quarterly review converts
"are the monthly KPIs on the glidepath to the Jul'27 number" — glidepath columns belong in
the tracker, not more KPIs.

**Terminology note:** "portfolio" retained as the umbrella for the five lanes (see org
doc §7 discussion) with the vocabulary rule: portfolio = accountability lane · product/
capability = what it ships · initiative = monthly roadmap item · KPI = Tier-1 measure ·
target = Tier-0 outcome.

## 12. Developer Platform lane, sharpened (2026-08-11, from the Aug roadmap)

Roadmap archive: `knowledge/raw/corpora/department/developer_platform_aug_roadmap.md`.
The team's own category vocabulary (System Reliability / Performance / Efficiency & Cost /
Issue Resolution TAT / Issue Recurrence / Engineering Delivery Efficiency) distills to
seven durable Tier-1 KPIs — this supersedes §5's generic list for this lane:

| # | KPI (Tier-1, monthly) | Aug Tier-3 evidence (targets) |
|---|---|---|
| DP1 | Learner-critical availability & saturation MTTD | 100% critical thresholds alerted; MTTD ≤10 min; Sentry criticals alerted in 5 min |
| DP2 | **Tail-latency user-impact %** (per surface SLOs) | IDE launch/submit/publish/npm P99 <60s, affected-users 6.7/9.6/3.6/11.6% → 0%; compiler per-language avg/P95/P99 <10/15/25s; C++ P99 10.28→<5s |
| DP3 | Observability & cost-attribution coverage | cost visibility 0→100% (per EnrollPlan/user/request/unit); IDE observability 100% |
| DP4 | Platform cost per unit (runtime cost per active learner + per-unit dashboards) | IDE −$30–50 (1.8–3%); terminate-on-tab-close |
| DP5 | Issue resolution TAT (user <2d; internal same-day) | feedback routing E2E; support-investigation agent; unclear feedback 32→<15% (input quality) |
| DP6 | Issue recurrence rate → 0 | platform instance of the culture Repeat-Issue KPI; "launching improvements for upcoming issues" |
| DP7 | Engineering delivery efficiency (NEW lane) | checkout 5–10min→0; cherry-pick ≤10min; agent plan-gen −20% + token usage; compiler CI/CD, no manual deploys |

Notes: DP2's "% users affected by tail" formulation is better than §5's plain P95 — adopt
it department-wide. DP7 is genuinely new (the portfolio's "engineering productivity"
purpose made measurable) — recommend unit: engineer-hours reclaimed/month.
**⚑ CRITICAL cross-link:** the n8n feedback fix "Course ID captured as Question ID" is a
join-key-integrity defect on the learner-data spine (everything joins on question_id) —
add to the contract-debt register and gate n8n-sourced analytics until fixed; also
capture-missing-Workflow-ID = Data Sync Completeness work.

## 13. Developer Platform lane scorecard — v1 for HOD review (2026-08-12)

First of the five lane scorecards (four-slot template: Impact / Adoption·Delivery /
Quality·Reliability / Efficiency). Derived from the Aug roadmap per the agreed method.
DP-8 is a commissioning metric — retires once it holds 100% for 2 consecutive months.
The n8n Question-ID fix is a one-time deliverable (contract-debt), tracked to done, not a KPI.

| slot | # | KPI | unit · cadence | current → target (Aug evidence) |
|---|---|---|---|---|
| Impact | DP-1 | Learning Environment Satisfaction *(moves from Content Effectiveness)* | Score/5 · M | baseline → up |
| Adoption/Delivery | DP-2 | Engineering Delivery Efficiency (hours reclaimed via tooling/CI-CD) | Eng-hrs/mo · M | checkout 5–10min→0 · agent plan-gen −20% · cherry-pick ≤10min |
| Quality | DP-3 | Learner-Critical Availability & Detection (MTTD) | % · min · M | 100% critical thresholds alerted · MTTD ≤10 min |
| Quality | DP-4 | Tail-Latency User Impact (% users outside SLO) | % · M | IDE launch/submit/publish/npm P99 <60s (6.7/9.6/3.6/11.6% → 0%) · compiler <10/15/25s · C++ P99 10.28→<5s |
| Quality | DP-5 | Issue Resolution TAT | Days · M | user <2 days · internal same-day |
| Quality | DP-6 | Issue Recurrence | Count · M | → 0 (never-twice) |
| Efficiency | DP-7 | Platform Runtime Cost per Active Learner *(moves from Content Efficiency)* | INR · M | per-unit dashboards; −$30–50 IDE (Aug) |
| Efficiency | DP-8 | Observability & Cost-Attribution Coverage *(commissioning)* | % · M | 0 → 100% (per EnrollPlan/user/request) |

## 14. Cross-HOD asks + workshops decision (2026-08-12)

**Asks of other departments** — a new artifact class: measurable dependencies on peer
teams, each tied to the department target it unblocks. Format: what we need · from ·
target · unblocks. First ask: Placement Partnerships → ≥3 GenAI tool partnerships
(n8n / Make / Base44) → enables tool workshops/hackathons inside academics → feeds SPI,
co-curricular, employability. Section added to the HOD one-pager (§7).

**Decision:** workshops/hackathons are NOT a new KPI type — each is delivered as a
**short course inside the owning domain** (first case: GenAI), inheriting the existing
course KPIs (content pieces, achievement, engagement). Keeps the KPI system closed.

**Domain list update:** + Python Django (FullStack family = MERN · Java Spring · Python
Django) and + Compliance Courses (Physics, Chemistry, Engineering Drawing, Quantum
Engineering…). Count now 12 tracks (HOD recalls 13 — candidate missing: Mathematics,
which appears in the complexity reference but not the domain list — pending confirmation).

### §13 revisions after HOD review (2026-08-12)
- **DP-2 Engineering Delivery Efficiency moved OUT of the lane scorecard** → added to the
  Head of Tech & Product cross-HOD ask ("Engineering Productivity incl. tooling
  time-reclaimed"). Rationale: management metrics about engineers belong to the manager of
  engineers; the lane keeps only what it ships to learners. Checkout/agent-planning numbers
  stay as Tier-3 initiative evidence.
- **Issue Resolution TAT confirmed under System Reliability** (not Business Impact).
  Rule: a number that can improve before students feel anything is operational; one that
  only moves when students feel it is impact. Renamed "Platform Issue Resolution TAT" to
  avoid collision with CSI's Issue Resolution TAT.
- **Developer Platform scorecard v1.1 (7 KPIs) APPROVED and live on the HOD one-pager**
  as a 9th category band; tracker count 36 → 41 (2 moves in: Env Satisfaction,
  Runtime Cost; 5 new: Availability & Saturation Detection, Tail-Latency User Impact,
  Platform Issue TAT, Platform Issue Recurrence, Cost-Attribution Coverage).
- **Second & third cross-HOD asks:** Graphic Design & Video Editing team heads (creative
  delivery-management: on-time %, turnaround TAT, rework rate, quality acceptance,
  utilisation, satisfaction); Head of Tech & Product scope narrowed to Product/Eng/Pedagogy.
- Domains: 13 (SQL and CS Core split; Mathematics scoped inside DS/ML at Low complexity;
  Compliance Courses added). Sub-departments section added to one-pager (7 direct-report
  units); vernacular cost moved CSI → Content Efficiency.
