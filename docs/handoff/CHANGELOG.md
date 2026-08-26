# Handoff Changelog

One line per change: date · doc · what · source.

- 2026-07-09 · (all) · migrated to scope-first structure v2 (program/ · intelligence/{global,stacks,products} · workbench/) per workbench/proposals/handoff_structure_v2.md; corpora + registries regrouped to <stack>/<course>; SLUGS.md added · this migration
- 2026-07-09 · workbench/proposals/evals_and_guardrails_strategy.md · new: evals/guardrails strategy (deterministic gates in-repo, judge slice on platform, golden sets from mined corpus) · user question re Agenta
- 2026-07-09 · workbench/proposals/evals_and_guardrails_strategy.md · decision: Promptfoo now / Langfuse at production / skip Agenta · user follow-up
- 2026-07-09 · .claude/skills/session-deck-craft · new skill: session/deck outline+review procedure over pedagogy intelligence (v1 outline-grade; generation gated on verdict pass + asset contract) · user question
- 2026-07-10 · workbench/proposals/org_design_content_department.md · new: dept org design (5 layers, seams-as-contracts, KPIs=system dashboards); pending merge of HOD's earlier roles/KPIs artifact · HOD ask
- 2026-07-10 · workbench/proposals/continuous_improvement_culture.md · new: never-twice culture (5-layer root-cause definition, 4-checkbox close, register+cadence for 91 ppl); org doc reconciled with real headcounts · HOD ask
- 2026-07-10 · workbench/proposals/kpi_system_v3_ownership.md · new: KPI ownership reconciliation (31 existing mapped, product + engineering lanes added, Owner column + Platform Engineering category, career-framework linkage); sources archived to corpora/department · HOD KPI files
- 2026-07-10 · reviews/review_cofailure_pilot.md + python/learner_behaviour.md · co-failure pilot delivered: review verified against raw pairs, 6-item Loops split adjudicated at content level (LP-04/LP-06 match, not clones, thin cells quantified); full-scale gates set · DE delivery
- 2026-07-10 · reviews/review_cofailure_pilot.md addendum-2 + python/learner_behaviour.md · raw re-run: DE computation exact to 1e-15; median-hides-pockets proven; 163 robust cross-session pairs = prerequisite coupling (ability-tercile stable); Loops split downgraded to content-plausible/under-powered; full-scale method spec v2 · raw pilot_extract from HOD
- 2026-07-10 · registries/python/node_proposals_s11_s15.md · new: node proposals for 5 pilot sessions from co-failure communities × misconception bank × outline (12 nodes, confidence-labelled, Depends_On candidates) · raw re-run
- 2026-07-11 · registries/python/node_health_model.md · added: rung policy (3 rungs + empirical sub-ordering, fail-band boundaries 15/40), pool-sizing derivation of >=3/cell, coding-items-same-nodes policy, per-node mastery gate config · s11 hard-cell gaps = first work orders
- 2026-07-13 · reviews/node_sme_validation_s11_s15.{md,csv} · new: SME validation instrument — all 174 clustered pilot items mapped node→cluster→question_id with fail% + code, 41 split/seam rows flagged; CSV has SME verdict columns (OK/MOVE/UNSURE) for per-question sign-off · HOD ask (validate each question's node attachment)
- 2026-07-14 · workbench/reviews/node_sme_validation_s11_s15.{md,csv} · v2 verification pass before SME handoff: 19 items moved with reasons (incl. s12 elif items N2→N3 — elif node is behaviour-backed after all), 16 seam rows flagged, per-move confirm list + 4 open SME questions · node_proposals s12 N3 upgraded C→B+C
- 2026-07-15 · workbench/requests/node_discovery_pipeline/ · new: runnable end-to-end pipeline (pairs → robust filter → communities → judgment-layer derivation) + README with checkpoints, for DE process validation; verified: 71,891 pairs match DE to 1e-16, 42/174 communities reproduce, membership MATCH vs SME instrument
- 2026-08-11 · corpora/department/org_five_portfolios_kpi_baseline_2026-08.md (new) + org_design §7 + kpi_system_v3 §9–10 · adopted five-portfolio structure reconciled (1:1 layer crosswalk, 5 PMs, Sr PM backfill); KPI baseline revision absorbed (3 deprecations, WAU/hours mismatches resolved, CSI 6-KPI section); baseline→portfolio mapping delivered; pending: NIAT organizational KPI list
- 2026-08-11 · corpora/department/niat_org_targets_jul2027.csv (new) + kpi_system_v3 §11 · NIAT org targets absorbed; four-tier cascade architecture (org outcome → dept KPI → portfolio → initiative) with linkage tags; dept↔org cross-map (CSI lane guards university CSAT; GRIT badge = PLE roadmap; NSPI definition pending); Developer Platform lane pending Aug roadmap
- 2026-08-11 · NSPI decoded (corpora/products/niat/nspi_decoded.md + pptx) + Dev Platform Aug roadmap archived + kpi_system_v3 §12 (7 sharpened DP KPIs; tail-latency user-impact formulation adopted; Question-ID mis-tracking flagged as spine contract-debt) · NSPI cross-map row updated with deprecation tension
- 2026-08-12 · kpi_system_v3 §13–14 + HOD one-pager · Developer Platform lane scorecard v1 (8 KPIs, four-slot template) for review; cross-HOD asks mechanism (first ask: 3 GenAI tool partnerships); workshops = short courses inside owning domain; domains +Python Django +Compliance Courses (12 tracks, 13th pending)
- 2026-08-12 · kpi_system_v3 §13-rev + one-pager · DP scorecard v1.1 approved & live (7 KPIs, TAT under reliability, Eng Productivity → HoT&P ask); asks for GD/VE heads; 13 domains; sub-departments section; tracker 36→41
- 2026-08-12 · corpora/department/kpi_tracker_fullstack_cscore_2026q1.csv (new) · live FullStack+CSCore sub-dept tracker with Apr–Jul'26 actuals/remarks (formative 10–52% univ spread; feedback SLA 25.6% w/ root causes; BOS 80% GRIT deferral) · one-pager: alignment/feedback descriptions updated, LACC + Framework Compliance product tags
- 2026-08-12 · one-pager · all 8 CSV description propagations applied; NEW Executive Ops KPI: Cross-functional Resource Utilisation (Eng/Product/Pedagogy/DA-DE/Product Designers) — tracker 41→42; Key Terms: Functions += DA/DEs + Product Designers, Support Teams += Performance Management
- 2026-08-12 · one-pager + corpora/department/kpi_tracker_csi_2026q1.csv (new) · lane chips on all 42 KPI rows (LD/LP/PLE/ACP/DP/PMO + legend); Univ Curriculum Compliance moved Content Relevance→CSI (sibling of Framework Compliance per CSI tracker); CSI descriptions enriched from live tracker (34 partners, first-pass solutioning, co-curricular in delivery gap); Ops&Growth desc expanded (checkins/roadmaps/1-1s/R&Rs/mentoring); freshness decision: domain env versions → LD freshness; DP infra-currency KPI proposed (pending); Content Issue Recurrence KPI proposed (pending)
- 2026-08-12 · one-pager · APPROVED+ADDED: Content Issue Recurrence (ACP, Content Efficiency, post-triage clause) + Infrastructure & Runtime Currency (DP, teach-current vs run-supported split) — tracker 42→44; PROPOSED (pending): Agentic Production Coverage 90% (design review in chat: per-type coverage, registered-workflow definition, video exclusion, quality pairing)
- 2026-08-12 · one-pager · Agentic Production Coverage APPROVED+ADDED (per-type coverage, registered workflows, 90% target) → 45 KPIs; NEW badges on the 3 additions; §6 target-mapping column now names exact KPIs with lane chips; June/July deliverable sheets requested for lane-scorecard baselining (not §6 live data)
- 2026-08-12 · one-pager §6 · target×lane matrix added above the detailed mapping (counts; PMO column dropped — internal-only by design; GRIT = initiative metric footnote); Academics CSAT row now includes DP's Availability & Tail-Latency alongside Env Satisfaction
- 2026-08-12 · one-pager §6 · Program Delivery Gap added to Academics CSAT mapping (students feel undelivered classes/workshops directly; one KPI may cascade to two targets, ownership stays single); BOS/compliance rows kept university-relations-only
- 2026-08-12 · one-pager restructure · NEW §5 'KPI categories — what each measures' (9 one-liners); Key Terms moved up to §2; ownership matrix moved down to §9 as internal-management view; final order: org → terms → complexity → baselines → categories → KPI list → targets → asks → matrix → sub-departments
- 2026-08-12 · kpi_system_v3 §15 + corpora/department/learning_platform/ (5 files) · Learning Platform scorecard v1 (6 KPIs w/ live baselines: tutor 24%, bookmarks 60% dead-clicks, practice 20%); discrepancy log (5 taxonomies, lane-spread roadmaps, ad-hoc targets); maintenance rules incl. adoption gate
- 2026-08-12 · learning_platform_capability_registry.md (new, v1 for review) · 28 capabilities across 4 user flows w/ live-on/instrumented/baseline/PM; retirement flags (Guiding Questions, gamified-vs-leaderboard); staff-facing marked; adoption-gate rule · one-pager reordered: baselines→terms→complexity→categories→list→targets→asks→org→matrix→subdepts
- 2026-08-12 · LP capability registry v1.1 · lens model formalized (capability=shared object, metric=lane-owned; LP/LD/DP/PLE lenses); domain anchors added (SQL env, DSA visualizer, n8n, NxtTalk, interactive Q-types, +ROS2 IDE row)
- 2026-08-12 · kpi_system_v3 §16 · remaining lane scorecards drafted (LD formalized w/ gold-tier + capability-outcomes; ACP w/ gate rate + judge agreement + coverage velocity; PLE w/ spread + lag + theme closure) — all 5 lanes complete, net-new only 7 rows
- 2026-08-12 · kpi_system_v3 §16 pruned per HOD: coverage velocity parked, freshness→ops dashboard, gate-rate+judge-agreement launch-gated w/ interim guard; theme closure kept (culture KPI, measurable now); ownership two-level rule (lane=KPI, item=PM/Eng/SME) affirmed
- 2026-08-12 · NEW artifact: dept operating view (own URL) — replaces tracker-v3 workbook idea per HOD; 6 sections: ownership rules (lens model, two-level ownership), 5 lane scorecards w/ LIVE/NEW/DRAFT/LAUNCH-GATED/PARKED statuses + baselines, category×lane matrix, full capability registry v1.1, operating rules (adoption gate, 4-checkbox, multipliers, commissioning-retire), parked decisions
- 2026-08-12 · ADOPTED: 5 metric categories v3 (Business Impact / Delivery / Adoption / Quality & Reliability / Efficiency & Cost — slot terminology, one question each; who-categories retired) · operating view updated: category table + 5×6 matrix (BI 12, Del 7, Adopt 2, Q&R 12, E&C 12 = 45 live), no old-category crosswalk per HOD; parked category-rename resolved · HOD one-pager NOT yet updated (inputs incoming)
- 2026-08-12 · corpora/department/niat_2026_asks_pavang.csv (new) + one-pager §7 · 3 cross-HOD ask rows added: Karthik/Univ Partnerships (academic operating conditions incl. 90 days/540 hrs, Topin exams, BOS-before-start, no adhoc holidays), Balabhaskar/Infra (WiFi 25Mbps, classroom spec, transport, sem-break info), Karthik/Program Ops (zero-deviation delivery, attendance, portal onboarding, in-class design adherence = SPI eligibility gates)
- 2026-08-12 · one-pager §7 · reconciled: 90d/540h canonical, induction ≤6d(3 NIAT), attendance = SPI gate 80%; NEW autonomy ask row (curriculum/teaching control, timetable, digital-exams-count-for-grading, AICTE subjects→Compliance domain, class 75-90); infra row upgraded to master spec (500Mbps+30/student, 85-95in display, socket/student, 5.0 Lab 600-700sqft) — 7 ask rows total
- 2026-08-12 · both artifacts · Feedback Resolution Efficiency RENAMED → Content Issue Resolution Efficiency (symmetric with Content Issue Recurrence); CSI Issue Resolution TAT REMOVED, replaced by cross-departmental pair: Product Issue Resolution Efficiency + Product Issue Recurrence (PLE, CROSS-DEPT tag, student-journey end-to-end) — 46 KPIs; tree+mechanism §6 redesign sent for review (not applied)
- 2026-08-12 · one-pager §6 · mechanism TREE replaces counts matrix (option A): 6 targets, lane-chipped branches with one-line mechanisms; Industry Update Adherence REDEFINED as Learning–GRIT delta → 0 (GRIT content = industry benchmark; % of GRIT-tested skills covered in course content at contest level) and wired into GRIT Novice Badges branch (delta→0 → pass 16→30% → 5,000 badges); operating view LD scorecard synced
- 2026-08-12 · one-pager · §7 renamed 'Asks FOR other departments'; GRIT glidepath branch removed from tree; NEW 8th ask: Sundar (GRIT Owner) to define GRIT feature KPIs (badge glidepath, pass 16→30%, mock-contest parity) — dept activities plan against them; operating-view parked note synced
- 2026-08-12 · one-pager §7 · GenAI partnerships target 3→≥5/year with sales logic (20+ tools committed over 4-year program); tree tone-pass proposed for review
- 2026-08-12 · one-pager · presentation tone pass applied (11 edits: neutral third person across tree + prose table; key-point punchline kept per recommendation)
- 2026-08-12 · CORRECTION (HOD): SPI authorship — dept authors ONLY classroom quiz (10%) + module quiz (15%) = 25%; skill assessments (25%) + FSA (50%) = 75% authored/conducted by the ASSESSMENTS DEPARTMENT. Fixed: one-pager tree branch, key-point, prose row, §5 summative/formative rows; nspi_decoded.md; kpi_system_v3 §11
- 2026-08-12 · one-pager §7 · 9th ask: Head of Assessments — blueprints/KPs per cycle + skill-assessment content changes ≥3 months ahead (content-production lead time); tree label synced to 'Learning Environment Satisfaction'
- 2026-08-12 · MODULE-QUIZ SCORE BANDS approved+added (LD, Business Impact): ≥80:30% · 70-80:40% · 50-70:30% · <50 skill-debt ~0%; one SPI band above org target (buffer for external 75%); alignment = honesty check; replaces gold-tier draft — 47 KPIs; Program Ops ask gains conduction-precondition sentence; LES-as-DP-headline (≥4.0/5) staged for HOD go
- 2026-08-12 · one-pager · Program Delivery Gap re-homed: OUT of Academics CSAT, INTO SPI bands (precondition branch: instructional days delivered → students sit assessments prepared); stays under University Relations. Summative Achievement target PROPOSED: ≥85% B3/B4 clearing by Jul'27 (5pp conversion buffer over 80% employability; glidepath from ~35% baseline) — on both artifacts
- 2026-08-12 · one-pager · SPI bands notation spelled out (tree + prose): 30% at ≥8.0 · 40% at 7.0–8.0 · 30% at 6.0–7.0
- 2026-08-12 · one-pager tree · SPI block rewritten as numbered FLOW (deliver→quiz→align→assess); both achievement branches now read as direct band-target translations (module quiz: 30/40/30 one band stricter; skill assessments: ≥85% B3/B4 clearing)
- 2026-08-12 · both artifacts · LES = DP headline @ ≥4.5/5, drivers bracketed with micro-phrases (caught-before-felt / feels-instant / fixed-fast / never-twice); Content–Assessment Alignment branch restored to clear delta definition with target = 0 (also §5 + operating view)
- 2026-08-12 · one-pager §6 · Employability target REMOVED from tree + prose table per HOD (dept story ends at SPI; buffer rationale stays in the Summative KPI definition); LES headline finalized ≥4.5/5 with bracketed driver micro-phrases; Alignment branch: clear delta definition, target = 0
- 2026-08-12 · one-pager+opview · Employability restored as LAST target block (nothing added inside — Summative leading branch only); Academics CSAT content branch explicit: Content Issue Resolution Efficiency ≥80% (fixed in 48 h — 2-day TAT) · Content Issue Recurrence = 0; Platform Issue Resolution TAT RENAMED → Platform Issue Resolution Efficiency (% within fixed 2-day TAT) across §5/tree/opview; stale Feedback-Resolution pairing reference fixed
- 2026-08-12 · both artifacts · Platform Issue Resolution Efficiency target set ≥80% (mirrors content; fixed 2-day TAT)
- 2026-08-12 · one-pager+opview · cross-dept pair on option C (baseline sets TAT; recurrence 0 day-one); SPI step-2 simplified w/ explicit marks bands; SPI step-1 detailed into precondition chain (lecture schedule adherence, classroom-quiz attendance/attempts/performance, practice schedule adherence & completion, module-quiz schedule adherence & integrity) with only-if-all-met → step-2 statement
- 2026-08-12 · both artifacts · BOS Credit Acceptance target 100% w/ cycle structure (~55 approvals B3-S3+B4-S2, counts TBC); module-quiz bands renotated on 10-point scale (≥8.0/7.0-8.0/5.0-7.0/<5.0) matching SPI band notation; Summative target re-derived FROM SPI bands (30/40/30 distribution per batch) — employability-derived 85% dropped
- 2026-08-12 · one-pager tree · second flow gate added after step 3 (only when 1–3 meet target does step 4 land); CDU sample metrics reviewed in chat (participation ~33%, conditional performance high — first-gate bottleneck)
- 2026-08-12 · one-pager §6 · Student Drop-off target removed from tree + prose per HOD (finance call for now); LE/IES stay as KPIs, unmapped to org target
- 2026-08-12 · corpora/department/bos_credit_acceptance_sem1_sem3.xlsx (new) + both artifacts · BOS targets set from data: 85% B3 (baseline 81.4%/17 univ) · 90% B4 (90.1%/36) replacing 100%; GRIT gains PLE upskilling branch; Employability mapping = yet-to-think placeholder
- 2026-08-12 · one-pager §7 · 10th ask: credit parity for NIAT subjects (no zero-credit demotions; named victims AI-for-Finance 59%/WAD-1 81%/QA 85%) — makes the 85/90 BOS targets reachable
- 2026-08-12 · one-pager §11 NEW: student-journey reference (10 rows class→SPI incl. revision loop + practice-availability; inherited rulebook on top; conditional quiz-participation threshold; sample lever targets; journey change rule for delivery redesigns — SPI 10% re-earn requirement); BOS B4 note: Bharath/PK Das/Visakha curriculum finalising (CSI); op-view LP pointer; naming: Sub-KPI retained, 'shared' in definition
- 2026-08-12 · one-pager · sub-dept homes CONFIRMED: Programming → Content-FullStack&CSCore; Robotics + Compliance Courses → Content-CSI (for now), pending note removed; journey row 1 rewritten as early-warning lever (LE/IES detect → Mentor Dashboard routes; targets: ≥90% breaches pre-flagged, actioned ≤7 days)
- 2026-08-12 · one-pager §11 · NEW journey row 10: skill-assessment schedule adherence (zero deviation · 100% participation, Assessments dept conducts, blueprint ask = our lever) — 11 rows; rulebook += 100% skill-assessment participation/FSA mandatory; row 5 lever names two failure modes (authored&loaded LD/ACP vs release-scheduling Ops); 'vs control' + LD/ACP-readiness explanations given
- 2026-08-12 · one-pager · row 2 += learning-asset SLA (PPT+video ready&loaded ≥1 month, Instructors-dept ask; production=LD, delivery=Ops) + rulebook row; row 10 corrected: skill assessments CONDUCTED by Program Ops, AUTHORED by Assessments dept — all remaining 'conducted by Assessments' → 'authored by' page-wide
- 2026-08-19 · docs/handoff/artifacts/ (NEW) · both artifact HTMLs recovered after scratchpad wipe (replayed 103 recorded ops from session transcript; verified against pre-wipe sentinels) and committed to repo — artifacts now survive temp-dir cleanup
- 2026-08-19 · both artifacts + kpi doc §17 · presentation-feedback round: alignment target |delta|≤10pp→≤5pp glidepath (zero unrealistic); recurrence ×3 → ≤2%/qtr; Summative/Formative → ORG outcomes, out of dept list (SPI contribution = MQ Bands + Alignment alone); IES → Engagement-Matrix Cell Migration (LP headline, SAMPLE 4→10/10→20 cell targets); §6 scoreboard-first; PLE += Journey Step Health + Capability Configuration Coverage; Univ Communication TAT NEW (ack ≤1bd, ≥90% in TAT); resolved = fix+notify; LP/PLE boundary + close-the-loop rules on op view; §7 challenges table (conduction adherence %s pending, attendance denominator); 47→48 KPIs
- 2026-08-19 · both artifacts · cell-migration window defined: 'term' → cycle = semester (NIAT) / quarter (rolling products) — cohort turnover follows semesters at NIAT, rolling products have no semester
- 2026-08-19 · docs/handoff/artifacts/kra_training_sheet.html (NEW, 🧭 44869dfd) · training sheet: 5 NIAT org KPIs as KRAs (targets in col 1) → 22 mapped dept-KPI rows w/ targets, KRA Team column (replaces 'Lane'), v3 metric category; markers ORG/CROSS-DEPT/SAMPLE/CASCADE; per-team session index (LD 3 · LP 1 · DP 5 · ACP 2 · PLE 8)
- 2026-08-19 · 🧭 training sheet v2 + kra_training_sheet.xlsx (NEW, editable master) · lanes ≠ teams fix: column renamed Lane (KPI owner) w/ definition; NEW 'Functions that move it' col (draft mapping: Product/Engineering/Content-SMEs/Pedagogy/DA-DE/CSI); session index re-cut BY FUNCTION w/ COUNTIF row counts; NEW Triggers col (Delivery Gap = journey-wise sub-metrics incl. asset SLA + skill-assessment conduction); NEW Funnel col (KPI→org causal chain per row); xlsx = 3 sheets (map/index/legend), Google-Sheets-ready
- 2026-08-19 · 🧭 training sheet v3 + xlsx · color layer for HOD/founder readability: 5 KRA color families (CVD-validated categorical order — blue/orange/aqua/yellow/magenta), band fill on KRA cell + hue accent bar + whisper tint on member rows + block separators; xlsx Legend gains color key; identity stays in text (validator pass, contrast WARN satisfied by labels)
- 2026-08-21 · 🧭 training sheet + xlsx · 'Triggers / sub-metrics' column renamed 'Dependent metrics' (header, how-to-read, xlsx C1 + legend) per HOD; tracker-alignment round begun — org KPI-tracker template located in repo (knowledge/raw/corpora/department/kpi_tracker_v2.csv, Head Abstract 2.4 family): S.No/Category/Product/Audience/MetricName/KPIName(convention Category:Product::Name)/Desc/Unit/Freq + monthly Budgeted-Actual-Variance-Remarks, variance = Budgeted − Actual
- 2026-08-21 · 🧭 training sheet + xlsx · KPI Tracker FY26-27 added — §3 on the artifact page and tab 4 of the workbook, in the org Head-Abstract format (S.No | KRA | Metric category | Product | Cohort | Metric name | KPI name convention `Category:Product:Cohort::Name` | Description | Unit | Frequency | Lane | annual Budgeted / Actual / Variance / Remarks). 27 numbered rows: bands-as-four-rows and per-batch rows split into B3/B4 (user-approved) — Module-Quiz Bands 8 rows, Content–Assessment Alignment 2, BOS 2 (85/90); Program Delivery Gap tracked once with CASCADE chip; Journey Step Health + Product Issue Resolution blank-budget (Q1 baseline, org precedent); variance = Budgeted − Actual as live formula; lower-is-better rows flagged in remarks; KRA color families + Arial + black header carried across; Legend gains tracker-convention rows. Builder + data committed (build_tracker.py, kra_data.json). Tracker Budgeted = number of record; map targets mirror it.

## 2026-08-21 — Training sheet + tracker merged into one sheet
- Merged the KRA-KPI map and the FY26-27 tracker into a single sheet: the tracker format is the base (per Pavan), with three training columns — Dependent metrics · Funnel → org KPI · Functions that move it — added as a collapsible column group (I:K), collapsed by default. Collapsed = org-format tracker; expanded = training view.
- Workbook is now 3 tabs (was 4): KPI Tracker FY26-27 (tab 1) · Session Index · Legend & Notes. "KRA-KPI Map" sheet removed; Budgeted is the single number of record (no cross-sheet sync rule needed anymore).
- Functions column re-vocabularied from the HOD one-pager §2 key terms (Content, Engineering, Product Managers, Pedagogy Experts, DA/DEs, Graphic Designers, Video Editors, Product Designers, Packaging Teams, SDIs + CSI team). Still a draft for red-pen.
- Session Index rebuilt: 7 rooms (asset-production room added), COUNTIF formulas re-pointed at tracker column K; counts are per metric (merged cells count once). Counts: Content 7 · Engineering 8 · PMs 5 · Pedagogy 2 · DA/DEs 4 · CSI 7 · Assets 1.
- Training narrative preserved as muted note rows (S&F under KRA 1, PDG-cascade pointer under KRA 3, GRIT, KRA 5).
- Artifact page regenerated: single 18-column table with a "Show training columns" toggle (collapsed by default), session index, updated legend text. Same URL.
- Files: kra_training_sheet.xlsx / .html / kra_data.json / build_tracker.py (all in docs/handoff/artifacts/).

## 2026-08-21 — Metric-category re-map: one vocabulary across tracker and one-pager
- **Why**: three category taxonomies had drifted apart (one-pager 9-set, org Head-Abstract 7, dept 3-way Delivery/Business Impact/Quality & Reliability), and two of the one-pager's nine were impostors on the category axis — Content Systems & Infra is a team, Developer Platform is a lane. Pavan's rule: category = what it measures · lane = who is accountable · functions = who does the work.
- **Approved vocabulary**: the org 7 (Business Impact · Content Effectiveness · Content Velocity · Content Efficiency · Content Relevance · Stakeholder Alignment · Executive Ops) plus three department "what" extensions — **Program Delivery**, **University Alignment**, **Platform Reliability**. The old dept 3-way is retired.
- **Tracker (🧭 xlsx + artifact)**: column C re-mapped on 15 of 18 metric blocks; all 27 KPI-name strings re-derived with the new prefixes (e.g. `Program Delivery:NIAT::Program Delivery Gap`, `University Alignment:NIAT:B3::BOS Credit Acceptance`, `Platform Reliability:All::Tail-Latency User Impact`, `Content Efficiency:All::Content Issue Resolution Efficiency`, `Content Effectiveness:All::Learning Environment Satisfaction`, `Content Relevance:NIAT::Industry Update Adherence`). Legend row 20 added documenting the vocabulary + axis rule. Session Index untouched (counts column K): 7/8/5/2/4/7/1 unchanged. kra_data.json ROWS categories updated to match.
- **One-pager (🎯)**: §4 — the two impostor rows replaced by three what-rows with descriptions, plus an axis-principle note. §5 — all 48 KPIs re-grouped: Program Delivery ← PDG, Journey Step Health, Product Capability Configuration Coverage; University Alignment ← BOS Credit Acceptance, University Communication TAT; Platform Reliability ← ASD, Tail-Latency, Platform Issue Resolution/Recurrence, Infrastructure & Runtime Currency; Content Efficiency ← + Cost per BOS Approval, Platform Runtime Cost per Active Learner, Cost-Attribution Coverage, Product Issue Resolution/Recurrence (all cost & issue-efficiency measures live in the one cost bucket, matching org 2.4 precedent); Content Relevance ← + Framework Compliance, University Curriculum Compliance; Content Effectiveness ← + Learning Environment Satisfaction. §9 matrix relabeled/split accordingly — row sums 5/6/4/14/4/2/3/3/2/5, lane totals unchanged (9/5/13/7/8/6, 48 KPIs); no KPI changed lanes.
- **Judgment calls flagged**: Infrastructure & Runtime Currency → Platform Reliability (its text is "run supported + patched within SLA" = hygiene, not teach-current relevance); the three platform/BOS cost KPIs → Content Efficiency rather than staying with their platform/university siblings — the bucket is the org's cost lens, already broader than content production.
- **Pending**: operating view (📋) category sync — deferred by Pavan ("Operating view is something we shall focus later").

## 2026-08-21 — Cadence corrections (Pavan): PDG weekly, Alignment monthly vs biweekly skill assessments
- **Program Delivery Gap [CASCADE]**: frequency Monthly → **Weekly** (tracker col N + one-pager §5).
- **Content–Assessment Alignment**: frequency Per cycle/Quarterly → **Monthly**, comparator named as the **Biweekly Skill Assessments** (tracker description, one-pager §5 description + §6 step 3). Target-tightening rule (≤5 pp after 3 clean cycles) unchanged — it is a threshold rule, not a cadence.

## 2026-08-21 — CROSS-FUNCTION rename + lane legend / axis one-liner
- Marker rename (Pavan): `CROSS-DEPT` → `CROSS-FUNCTION` on Product Issue Resolution Efficiency + Product Issue Recurrence — resolution spans functions (PMs, Engineering, Content), not departments. All surfaces: tracker xlsx metric cells + Legend B7, tracker HTML tags + key-point legend, builder TAG dict + descs ("resolved across functions, we route"; "regardless of which function owns the fix"), kra_data.json ROWS markers, one-pager §5 tags + §6 li + tag legend. Zero stale strings.
- Lanes now explained on both surfaces (gap Pavan flagged): tracker HTML gets a second key-point div — six lane one-liners (LD/LP/PLE/ACP/DP/Shared-PMO) + the axis line; xlsx Legend B3 rewritten with per-lane glosses + axis line (row height 70). One-pager §2 gains a "Lanes" key-term row (points at §8/§9) + a sectionlead one-liner under the table: category = what it measures · lane = who is accountable · function = who does the work.
- Pending (unchanged): operating view (📋) category + cadence + marker sync — deferred by Pavan.

## 2026-08-21 — JSH/PDG refinement + team-view tabs (CSI · FullStack & CS Core)

**🧭 Tracker (44869dfd…):**
- PDG desc: existence-only boundary ("a step that never runs counts here, not in Journey Step Health"); remark gains assembled-KPI line (named step owners, red 2 consecutive weeks → HOD-to-HOD).
- JSH desc: health-of-what-ran boundary (never-ran counts in PDG, not here); remark gains assembled-KPI line.
- Dependent metrics (col I) owner-tagged on PDG + JSH rows (Program Ops / Instructors / Learning Domains / LP lane / LD-ACP per step).
- NEW tabs 4–5: **CSI Team View** (A 8 inherited · B 3 owned · C 3 asks) and **FullStack & CS Core View** (A 18 inherited · B 25 owned · C 3 asks). Section A = live formula mirror of the tracker (blank-safe IF wrappers; shared cols reference block top-row, per-KPI cols reference own row; edit on tracker only). Section B = team-owned KPIs with own B/A/V columns (left blank for the team; Q1 Jul references in Remarks) + **Ladders to** column (direct / enabling / hygiene). Section C = asks of counterparties. CSI Section B re-homed to org vocabulary (CpBOS + CpVH → Content Efficiency, O&G → Executive Ops).
- Legend row 21: team-view explainer (dock-not-merge, ladder key, pilots). HTML subtitle → "5 tabs".

**🎯 One-pager (cd52be82…):**
- §5 PDG + JSH descriptions carry the same existence-vs-health boundary; JSH points at the §11 owner column + escalation rule.
- §6 JSH bullet updated (health of what ran).
- §11: NEW **Step owner** column on the journey table (11 assignments — Program Ops / Mentors / Instructors dept / Learning Domains / LP / LD-ACP); sectionlead rewritten (named owners, §7-ask governance, HOD-to-HOD escalation).
- Footnote: "9 categories" → "10 categories" (stale since the org-7 + dept-3 re-map).

Pending (unchanged): operating view (📋) category + cadence + marker sync — deferred by Pavan.

## 2026-08-21 — Go-package: lane moves, APC tracker row, University Alignment, worked-by map, §10 embedded functions, team-view Product/Cohort columns

**🧭 Tracker (44869dfd…):**
- **CIRE + CIR lane** → Learning Domains (they score the fixes; ACP builds the pipes). Rows r16/r17.
- **NEW r18 — Agentic Production Coverage** (Content Efficiency · All · ACP lane · 90% budget from §5's stated target): ACP's own tracker row; functions = "Content–Central + DA/DEs" (red-pen draft — Pavan's sketch said "Learning Domains"; chose Content–Central per §10's production-ops definition). Session Index gains a Content–Central room; bare-Content counts now exclude Content–Central (COUNTIF subtraction in xlsx, token-based fx matcher in team views — en-dash keeps "Content–Central" one token).
- **University Curriculum & Framework Compliance** category → University Alignment (KPI string re-derived). Marker vocabulary unchanged.
- **JSH functions** += Pedagogy Experts (journey design); Pedagogy session room notes JSH; DA/DE room notes APC instrumentation.
- **Remarks**: Cell Migration gains the Score-Bands arbitration rule (both red → bleeding cell names the lane); LES becomes the DP umbrella with CROSS-FUNCTION-style verbatim routing.
- **Legend row 22 — Lane ↔ working teams**: full worked-by (primary) map; staffing never ownership; counterparties reached through asks.
- **Team views: Product + Cohort columns added (12 → 14 cols)** — Pavan's flag: this is where Academy / Intensive-offline KPI rows slot in later. Section A live-mirrors tracker cols D/E (cohort ref hits the merged run's top cell); Section B parses product from "(NIAT)"-style name suffixes (Graded Assessment → NIAT, WAU → Launchpad, CSI CpBOS → NIAT, CpVH → NIAT + Academy; rest All); Section C ask/detail re-homed to name/description cols; freeze G4.

**🎯 One-pager (cd52be82…):**
- §4 University Alignment definition now covers partners **and regulators** (+ curriculum & framework compliance).
- §5: CIRE/CIR chips ACP→LD; Framework Compliance + University Curriculum Compliance rows moved Content Relevance → University Alignment (kept adjacent — they're explicit siblings). §6 scoreboard + mechanism-tree chips follow.
- §8: **Worked by (primary)** line on all five lane cards + closing legend (staffing ≠ ownership; many-to-many; Program Ops/Instructors/Mentors are §7 counterparties).
- §9 matrix: Content Efficiency LD 2→4, ACP 6→4 · Content Relevance PLE 2→0 · University Alignment PLE 2→4 · totals LD 9→11, ACP 7→5 (grand 48 unchanged — APC already counted in §5).
- **§10 retitled "Sub-departments & embedded functions"** (Pavan's ask, verdict yes): direct-reports table unchanged; NEW second table — Product Managers, Engineering, Pedagogy Experts (journey design at CSI · lesson-plan design in LD), DA/DEs, Graphic Designers · Video Editors, SDIs — business reporting read through the lanes they staff, line reporting to their own function heads; ties to the §7 execution-management asks (lines already there).

Pending: FS Section B relevance review (LE, Course Completion, Pedagogy Initiative Impact, Learner-Accessed CCR, Practice A-to-C — analysis delivered, Pavan to rule); Role cards / Career framework (Pavan attaching his earlier domain-specific versions — analyse → plan → then implement; title pattern shifting to "AI Engineer – FullStack Learning Systems" style); operating view (📋) sync still deferred — now also owes lane/category/APC + §10 changes.

## 2026-08-21 — FS Section B rulings applied: LE + Course Completion retired as budgeted rows

**🧭 Tracker (44869dfd…):**
- **Learning Engagement Effort (LE) — dropped from Section B.** Pavan's ruling on the relevance review: LE is the effort *axis* of the engagement matrix, not a KPI to budget — it already lives inside tracker Cell Migration. Stays as a dashboard instrument (the Section C ask still names it).
- **Course Completion Rate — dropped from Section B.** Completion is conduction-driven (Program Ops holds the lever); a content team can't be budgeted on it. Demoted to a read-only cut inside the "Engagement & LE dashboards" ask (detail extended to say so and to name the owned stickiness pair).
- **Pedagogy Initiative Impact — stays, ownership pinned.** Ruling: pedagogy initiatives live inside content departments; Pedagogy Experts may work on them but the KPI owner is the respective domain content SME. Remark added; ladder re-pointed off the retired LE row → module-quiz Bands + org KRA 2 Academics CSAT.
- **Learner-Accessed Content Completion Rate — stays** (access-conditioned denominator strips conduction effects → genuine content signal). Ladder re-pointed off the retired Course Completion row → tracker Cell Migration, video-stickiness leg of the value axis.
- **Practice Attempt-to-Completion Rate — stays unchanged** (strongest of the five: difficulty-calibration vs environment-friction split).
- FS view Section counts now **A 18 · B 23 · C 3** (was B 25); 23 variance formulas; no dangling ladder references (verified).

Role cards / career framework doc received (knowledge/raw/corpora/remixed-0bb5468a.html — "SDE Learning Systems Career Framework", Mar 2026): analysed this session, implementation plan proposed to Pavan — **no implementation yet** (his analyse→plan→approve rule). Open question posed by Pavan, discussion delivered, awaiting his call: domain-specific product work (evaluation environments, domain-specific LP capabilities) sits in content dept with no covering KPI — proposed generic→LP / domain-instance→LD rule + two candidate Section B rows (Evaluation Environment Coverage, Domain Capability Delivery), Section-B-first vs org-tracker-row question pending.

Pending: operating view (📋) sync still deferred — owes lane/category/APC + §10 + these Section B changes.

## 2026-08-21 — Domain Product Enablement: Section-B-first, boundary rulings recorded

Pavan's rulings on the domain-product-work question, applied Section-B-first (org-tracker row waits for a registry baseline — APC precedent):
- **FS view Section B — new category "Domain Product Enablement"** (before the Executive Ops tail), template for all future domain views:
  - **Evaluation Environment Coverage** (% · Quarterly) — item types × production-ready eval envs; domain configuration by the team's SMEs, platform build by PMs + Engineering. Ladders → PAtC env-friction leg + JSH 6–7 + LES. Remark: registry first, then budget.
  - **Domain Capability Delivery** (% · Quarterly) — domain-specific capabilities shipped vs committed; raised/accepted by SMEs, built by PMs + Engineering, accountability stays in the domain view. Ladders → PCCC + LP capability registry.
- **FS view Section C — new ask "Domain-specific capability build"** of Learning Platform (PMs + Engineering), detail carries the boundary points verbatim.
- **Legend row 23 "Domain product boundary"** — system-level record: domain-specific product work (incl. domain-specific learner-facing AI tutors/agents) = raised/accepted by domain SMEs, built by PMs + Engineering, KPIs in the domain's Section B under Learning Domains accountability · generic/reusable capability = Learning Platform lane, product-owned · ACP = content-facing production pipelines, domain product work = learner-facing systems · Section-B-first.
- **Legend B4**: "Packaging Teams (Content Systems & Infra)" — Pavan's naming clarification.
- FS view now **A 18 · B 25 · C 4**; 25 variance formulas; html byte-identical (team views are xlsx-only), so no artifact republish — URL content already current.

Role-cards plan: Packaging-Teams question resolved; still open — title set confirmation, comp bands in/out of shared sheet, FS pilot first. Implementation waits on those.

## 2026-08-21 — AI Engineer Ladder shipped: role cards v2 as a new artifact

"proceed with role cards implementation" — the March 2026 SDE Learning Systems framework translated into the KPI system and published as a NEW artifact (🪜): https://claude.ai/code/artifact/dc3ab90d-c4a4-448d-bdb5-fb43a9235734
- **Titles renamed** to the "AI Engineer – [Domain] Learning Systems" pattern: Associate AI Engineer / AI Engineer 1 / 2 / Lead / 3; source examples retitled, "formerly SDE …" kept on every card. Ladder is linear — 3 sits above Lead (30L+ vs 24–30L); the progression matrix stops at Lead by design (no dual-track needed).
- **KPI wiring added** (the v2 value): all 21 progression areas cite named tracker / FS-view rows or say "review-based — by design" (13 wired / 8 by design); rating pillars P1+P2 sublines read from named rows (P3/P4 stay review-based); Learning Systems Design wires to the new Domain Product Enablement pair.
- **Per-level metric surface**: Associate contributes to Section B → 1 answers module rows → 2 answers a domain slice incl. Evaluation Environment Coverage → Lead answers the team's full Section B + supports Section A lane numbers → 3 shapes org-tracker rows.
- **Vocabulary bridge**: doc Functions ≈ §10 embedded functions (Packaging Teams = Content Systems & Infra); Stakeholders ≈ §7 counterparties reached via Section C asks; "owns"/P&L language → axis rule (Lane = accountability · Functions = who works).
- **Pilot instantiated**: FullStack & CS Core — Full Stack 180h + CS Core 115h; High 2.0x / Medium 1.5x; metric surface = the team view (A 18 · B 25 · C 4).
- Files: role_cards.html + role_cards.xlsx (editable master, 5 tabs: Ladder / Progression Areas / KPI Wiring / Rating Framework / Calibration) + build_role_cards.py + role_cards_source.json (parsed source; the raw corpora html stays untracked).
- Defaults taken, all reversible: comp bands included (artifact is private — strip before wide sharing) · title set as above · FS & CS Core as pilot. Other domain teams get cards when their team views land.

## 2026-08-21 — Content OS: all three artifacts published as one site, high → low

"have all the three artifacts at one place like published in a website in a logical fashion, information should flow from high level to low" — NEW artifact (🗺️): https://claude.ai/code/artifact/ef86c2ad-4e52-494a-af7c-5416b579bde9
- **One scroll, four altitudes**: Level 1 Organization (HOD one-pager, full content) → Level 2 Department (KPI tracker + training-columns toggle, working) → Level 3 Team (FullStack & CS Core functional view, generated from kra_training_sheet.xlsx: 18 inherited Section A chips w/ T-numbers · full 25-row Section B table · 4 Section C asks · anatomy explainer) → Level 4 Individual (AI Engineer Ladder). Sticky nav, hero map of the four levels, black band per level naming the standalone artifact + master file.
- **Flow made explicit**: between every level, ▼ targets cascade (blue #004085) / numbers ladder up ▲ (teal #0e6e5c) — the system's own two accent colors used as the two directions.
- **Embeds are copies, not links**: each artifact's css scoped via native CSS nesting (#org/#dept/#ind; shared family body hoisted); Level 3 authored fresh since team views lived only in the xlsx. Standalone artifact URLs unchanged and linked from each band + footer. ⇒ MAINTENANCE RULE: republishing any child artifact now also requires rebuilding (build_site.py) + republishing the site.
- **Comp bands kept OFF the site** (wide-audience default, reversible): lvl-comp lines reduced to years-only; sectionlead/footnote rewritten to say where comp lives (standalone ladder artifact + role_cards.xlsx); build asserts no comp string survives.
- **Every embedded table wrapped in a scroll container** (.tscroll, 28 tables) — page never scrolls horizontally at any width (verified 0px overflow; 9 wrappers active at 723px).
- Excluded: 📋 dept operating view — stale (owes lane/category/APC/§10 + both Section B rounds); joins the site after its sync.
- Files: content_os.html + build_site.py (reads the four repo artifact copies + the xlsx).

## 2026-08-21 — Content OS: site-only ladder edits + downloadable xlsx masters

Same URL: https://claude.ai/code/artifact/ef86c2ad-4e52-494a-af7c-5416b579bde9

**Ladder section (#ind) now deliberately DIVERGES from the standalone ladder artifact** (directives 21 Aug, site only — role_cards.html/xlsx and the 🪜 artifact unchanged):
- All five "formerly …" sublines removed (regex, count-asserted = 5).
- "What changed in v2" dialogue removed; replaced by a neutral "How to read the cards" chip legend (the mono-chip explanation is load-bearing for the matrix, so the legend survives without any version-history framing).
- "AI Engineer 3 – [Domain Portfolio] Learning Systems" retitled **"Head of [Domain Portfolio] Learning Systems"** — card body opens "Directional for now — title and shape indicative, not finalized", example = "Head of FullStack & CS Core Learning Systems"; sectionlead + footnote level names follow (Associate / 1 / 2 / Lead / Head-of-domain (directional)); footnote's "in v2" phrasing dropped. Builder asserts no "AI Engineer 3" / "formerly" / v2 dialogue anywhere in the page.

**Downloadable masters**: kra_training_sheet.xlsx (33,129 B) + role_cards.xlsx (18,788 B) base64-embedded (page 169→240 KB); 5 green ⬇ buttons (dept/team/ind bands + footer pair) saved via the viewer's `downloads` runtime capability — republished with capabilities={downloads:true}. Buttons ship hidden; script unhides only when claude.use("downloads") resolves (plain <a download> is inert in the artifact viewer). Save flow: confirm dialog → "saved ✓" / declined restores label / other errors show "couldn't save — try again"; button disabled during the one-at-a-time prompt.

Verified over localhost: 0 page overflow, 28 tscroll wrappers intact, tracker toggle functional, no console errors, 5 buttons present + hidden on the null path, level titles Associate/1/2/Lead/Head-of.

Queued from same directives: KPI rows for every rating pillar/area (one at a time, later); the standalone ladder artifact keeps formerly-lines/v2/AI Engineer 3 until a future sync is ordered.

Files: build_site.py, content_os.html.

## 2026-08-21 — Metric evolution: R&D Initiative Impact retired, APC takes its row
- **R&D Initiative Impact retired everywhere** (Pavan: "make APC row instead of R&D"). Absorbed by Agentic Production Coverage (org row S.No 15, Budget 90) + the cost-per-item rows + Content Issue Recurrence — initiative counting is no longer a KPI anywhere. Removed: FS Section B tuple (build_tracker.py), one-pager §5 dept row + §9 matrix (ACP cell 4→3, column total 5→4, Total 48→47, footer "47 KPIs"), role-cards rating subline 4 KPI read + Production Systems / GenAI Orchestration progression chips.
- **APC cascaded into FS & CS Core Section A** at the same 90 budget via the FS view `twins` list (en-dash tokenization means "Content–Central" never matched `match:"Content"` — twins is the designed extension point). FS view now A 19 · B 24 · C 4 (APC = ref G18). CSI view untouched (A 8 · B 3 · C 3).
- **EEC/DCD kept for v1 with pre-agreed evolution trigger** recorded in remarks: at ~90% registry coverage or after two cycles, the pair folds into one funnel KPI (raised → accepted → delivered rate + TAT, capabilities-raised/quarter as non-budgeted context). EEC remark also records the gating: "Baseline first: build the item-type × environment registry, then set the budget (APC precedent)."
- **PII kept as-is with pre-agreed outcome form** recorded: becomes Domain Learning-Value Uplift (ability/band improvement across the domain's courses per cycle, HE×HV machinery) once per-course ability instruments are confirmed.
- **Legend & Notes row 24 added**: "Metric evolution (pre-agreed)" — all three forward moves in one place.
- Builders updated (build_tracker.py, build_role_cards.py, build_site.py — FS parser ranges A 5–23 / B 25–48, asserts 19/24/4); all outputs regenerated; site republished with capabilities omitted (downloads carried forward). All four artifacts republished to same URLs (🎯 cd52be82 · 🧭 44869dfd · 🪜 dc3ab90d · 🗺️ ef86c2ad).

## 2026-08-22 — Product Design added as embedded function (one-pager only)
- Pavan's Content–Central detail-out began: Content–Central = two people — a Business Ops owner (shared-resource P&L + the ACP builders, reports to HOD) with a PMO person under them. "PMO" name confirmed over "Executive Ops". Metrics list shown in chat for approval first — tracker/team views deliberately untouched (one surface at a time).
- One-pager: Product Design added to §10 embedded-functions table (UX/UI for learning products, read through LP capability builds + PLE journey work, no dedicated KPI rows yet) and to the §7 execution-management ask (now Product, Engineering, Product Design, Pedagogy). §2 Functions definition + §5 Cross-functional Resource Utilisation already listed Product Designers — no other surface touched yet.
- 🎯 + 🗺️ republished (site re-embeds the one-pager).

## 2026-08-22 — Content–Central team view lands (Section-B-first; org tracker untouched)
- **New xlsx tab "Content–Central View"** (amber, 6th tab) in kra_training_sheet.xlsx, built by the same
  `build_team_view` machinery — 14-col layout, Product+Cohort columns, frozen panes, live Section A mirror.
- **Section A (inherited, 1 row):** Agentic Production Coverage (org row S.No 15, budget 90) mirrored live via
  the Functions token "Content–Central". Its "Ladders to" cell carries the Central read: **units-at-bar — how many
  of the 5 learning-domain units hold ≥ 90 (a count, not a blended average)**; each domain owns its own slice in
  its own view (FS & CS Core wired). Implemented as a new optional per-view `a_notes` key appended to the
  provenance text — Section A numbers stay tracker-only.
- **Section B (owned, 5 rows — the approved start set):**
  · Business Ops — Shared Teams: **Shared-Team Deliverables Landed** (%, Monthly; enabling → dept Stakeholder
    Alignment) · **Shared-Team Spend vs Plan** (%, Monthly; enabling → dept Content Efficiency)
  · Agentic Content Platform: **Shared Tool Adoption** (%, Monthly; enabling → tracker APC; bar = ALL learning
    domains within a month of shipping)
  · PMO: **Check-ins Run** · **Actions Closed** (%, Monthly; hygiene — operating-rhythm guardrails)
  All budgets blank — baseline-first remarks (register/allocation built in Q1, budgets after one cycle).
  Deferred companions noted in the Actions Closed remark: spend → outcome map · tracker freshness · finance turnaround.
- **Section C (asks, 2 rows) = the §7 asks:** execution-management KPI tracking (Product, Engineering, Product
  Design & Pedagogy function heads) · creative delivery-management tracking (GD & VE team heads).
- Subtitle names the two-person shape: Business Ops owner (shared-team delivery + ACP builds; reports to HOD)
  with a PMO manager reporting to them — role titles pending.
- **Cross-functional Resource Utilisation verified NOT an org-tracker row** (dept §5 KPI only) — so Section A is
  APC-only; the earlier "APC + CRU" sketch was corrected. View = exactly the six approved metrics (1 inherited + 5 owned).
- Org tracker rows byte-identical (28 rows, max S.No 28, Legend 24); FS/CSI views untouched (site asserts A19/B24/C4 pass).
- Sync: training-sheet html subtitle + footnote now say 6 tabs (footnote's stale "3 tabs" fixed); site download
  card names all three team views; site xlsx b64 refreshed. 🧭 + 🗺️ republished to same URLs.

## 2026-08-22 — Utilisation rows join Content–Central Section B (5 → 7)
- Two owned rows added under **Business Ops — Shared Teams** (inserted after Spend vs Plan, category contiguous —
  the category now reads: what landed · what it cost · how fully the people were used):
  · **Creative Resource Utilisation — All Units** (%, Monthly) — GD & VE bandwidth across all sub-departments vs
    planned deliverables; Central reads aggregate + skew, day-to-day stays with unit PMs; enabling → dept Creative
    Resource Utilisation (§5, PMO lane). Domain slices stay (FS keeps its own row). Remark carries FS Q1 Jul
    reference (A 100% — stretched).
  · **Cross-functional Resource Utilisation — All Units** (%, Monthly) — embedded Engineering, Product, Pedagogy,
    DA/DE, Product Design bandwidth vs committed work across every unit; enabling → dept Cross-functional Resource
    Utilisation (§5, PMO lane).
  Both §5 PMO-lane KPIs thereby land their team owner for the first time. Baseline-first remarks: Q1 allocation
  register per unit; unit PMs supply reads, PMO manager collects, Business Ops lead owns the judgment.
- Renumbering only below the insert: Shared Tool Adoption → 5, Check-ins Run → 6, Actions Closed → 7.
- Untouched: org tracker (28 rows, Legend 24), CSI/FS views, one-pager (§5 rows already correct),
  kra_training_sheet.html byte-identical (no 🧭 republish). Site xlsx b64 refreshed → 🗺️ republished same URL.

## 2026-08-22 — Team Ops & People replaces Executive Ops in the team views (the PM layer gets its metric set)
- Approved in chat (talk-first design, then "Go"): the domain-view Section B category "Executive Ops" is renamed
  **Team Ops & People** and rebuilt around the Project-Manager-per-unit role — KPIs cascade Lead → PM (PM reports
  to the Lead). Applied to **FS & CS Core** and **CSI** tabs in one pass (both carried the category).
- The old single "Operations & Growth Cost" row (ops + hiring + market analysis in one ₹) is replaced by six rows:
  **Cost of Operations** (INR · Monthly — desc carries the full activity list: one-on-ones, Head-approved roadmap
  reviews, standups & learning hours, check-in scheduling & documentation, team assets, ClickUp adoption & status
  freshness, worklog capture, newsletters, outings, cycle appraisals + folded-in operational-efficiency/market-analysis;
  worklog capture named load-bearing — it powers deliverable costing; FS remark keeps continuity: Jul A ₹300,863 spans
  ops + hiring, worklogs split it) · **Roadmap Items Completion** (% · Monthly, cycle-anchored, Head-approved roadmap) ·
  **Hires Made** (Count · Monthly) · **Cost per Hire** (INR · Monthly, split out of the old combined row) ·
  **Team Retention Rate** (% · per appraisal cycle — trailing 12 months to smooth small-team noise; internal transfers
  don't count against; regrettable exits flagged by the Lead) · **Power Performers Created** (Count · per appraisal
  cycle — newly top-band; ladders to §5's "developing the best" intent; name converges with the ladder's existing
  Develop-the-Best pillar evidence). FS keeps Creative Resource Utilisation Rate as the category's 7th row.
- Content–Central PMO gains **Worklog & Status Hygiene — All Units** (% · Monthly), inserted before Check-ins Run so
  the PMO block reads as a pipeline: fed → held → closed. Central B now 8 rows.
- Counts: FS A 19 · B 29 · C 4 — CSI A 8 · B 8 · C 3 — Central A 1 · B 8 · C 2. Org tracker untouched (28 rows);
  one-pager §5 untouched by agreement (re-split later if wanted); kra_training_sheet.html byte-identical → no 🧭
  republish. build_site.py: B range/assert 24→29, C rows shift +5, subtitle now lists all three live views with counts.
  🗺️ republished same URL (capabilities omitted).
- Queued next surface (role cards 🪜): add the Project Manager role card (reports to Lead, carries this KPI set) and
  fix the now-stale "Operations & Growth Cost" chip on the Best Practices pillar (→ Cost of Operations).

## 2026-08-22 — Project Manager role card + Cost of Operations full ops register + KPI-wiring audit fixes
- **Cost of Operations remarks (both team views):** the row's remark now carries the full 11-activity ops register
  verbatim (one-on-ones · roadmap reviews + Head approval · standups/learning hours · check-in scheduling +
  documentation · team assets · ClickUp adoption · status freshness · worklog capture → deliverable costs ·
  newsletters · outings · cycle appraisals) "so nothing is forgotten" — FS View row 47, CSI Team View row 16.
  kra_training_sheet.html byte-identical → no 🧭 republish.
- **PM role card shipped (🪜):** role_cards.xlsx gains Tab 6 "Project Manager" and role_cards.html a matching section
  (between Pilot and Vocabulary bridge). Framed as the team's operating seat, not a sixth ladder level: title
  "Project Manager – [Domain] Learning Systems" (pilot: FS & CS Core) · reports to the team's AI Engineer Lead
  (KPIs cascade Lead → PM) · comp band pending with HR · owns the 7 Team Ops & People rows · runs the 11-activity
  register · interfaces Content–Central PMO (feeds Worklog & Status Hygiene — All Units) · progression/rating for
  the seat honestly marked not-designed-yet. Section passes all site-embed asserts (comp text carries no band).
- **KPI-wiring audit (post-metric-update) — 4 stale spots fixed:** Best Practices chip Operations & Growth Cost →
  **Cost of Operations**; Mentorship "review-based, no KPI row" → wired to **Power Performers Created**;
  Develop-the-Best rating sublines wired (Power Performers Created 30% · Hires Made + Cost per Hire 15% ·
  Team Retention Rate 20%; Timely Feedback + Growth Opportunities stay review-based by design); FS pilot surface
  line Section B 24 → 29. Subtitle/footer now "(6 tabs)". Footnote records the queue: CSI and Content–Central
  role cards to be built separately (Pavan's FYI).
- **Builder resilience (macOS TCC incident):** the app lost ~/Desktop access mid-session; work continued from the
  session scratchpad. build_role_cards.py now falls back to **comp_boxes_cache.json** (new, committed — round-trip
  proven against role_cards.xlsx; makes the builder clone-runnable since the raw source stays untracked) when the
  raw html is unreadable; build_site.py falls back to cwd copies when docs/handoff/artifacts/ is unreachable.
- 🪜 + 🗺️ republished same URLs (site: capabilities omitted, downloads carried forward; ind band + footer mention
  the PM card / 6 tabs). Org tracker rows, one-pager, 🧭 untouched.

## 2026-08-22 — KPI Flow Map artifact (new) 🕸️
- **New artifact "KPI Flow Map"** https://claude.ai/code/artifact/81cb774c-3cc4-4715-9f2b-b1fafdb72c4a — one
  interactive picture of how every KPI flows, per Pavan's ask ("some kind of graph… how all of the KPIs flow,
  connect across sub departments, Functions to Org KPIs"). Four columns: team Section-B rows (FS teal #0D9488 /
  CSI amber #B45309 / Content–Central violet #6D28D9, grouped by category) → dept §5 scoreboard (8 nodes:
  4 blocks + 3 rows + the Develop-the-Best intent marker) → org tracker (19 collapsed metrics, every node
  showing its Lane + the Functions that move it) → the five KRAs with weights.
- **Three edge kinds:** solid team-coloured = "ladders to" (36) · dashed from each team's Section A capsule =
  answers an org row directly (18 unique org rows: FS 10 / CSI 7 / CC 1) · grey = org row rolls into its KRA
  (20, incl. the Program Delivery Gap cascade edge into KRA 3). Hygiene rows (FS 6 / CSI 5 / CC 3 PMO) drawn
  dashed with deliberately no edges; Section C asks listed in the footer, not drawn as nodes.
- **Interactions:** hover previews / click pins a node's full upstream+downstream chain (rest dims); tooltips
  carry descriptions, unit·freq·budget, verbatim "Sheet says:" ladder prose, org Lanes + Functions, per-cohort
  budgets; team filter chips; collapsible all-74-edges table for red-pen review.
- Palette passed the dataviz six-checks validator (CVD + contrast on white; #0F766E and #0E7490 failed and were
  rejected). Builder docs/handoff/artifacts/build_kpi_graph.py reads kra_training_sheet.xlsx, asserts 19 org
  metrics / 45 team rows / zero unmapped ladder names, exits non-zero on drift — regen after any tracker or
  team-view change.
- One-surface-per-approval: published standalone; NOT embedded into the 🗺️ Content OS site pending a separate
  approval. No existing artifact touched.

## 2026-08-22 — Career Growth Map artifact (new) 🧗
- **New artifact "Career Growth Map"** https://claude.ai/code/artifact/a051587e-381c-4712-a501-9cfceaf75756 —
  the AI Engineer ladder read against the frozen KPI system, per Pavan's ask ("explain the Career growth
  framework design mapped with the frozen KPIs… visually"). Two parts on one page:
  **climb band** (5 level cards + the PM operating seat, dashed, explicitly "not a rung") with a widening
  teal beam per level — review evidence → your modules' rows → a domain slice → full Section B (29 rows) →
  §5 + org tracker — SURFACE text verbatim from the ladder; and **one canvas**: 21 progression areas
  (4 groups; 7 review-based areas dashed with no edges by design) → the frozen rows that evidence them
  (all 29 FS Section B rows + the 7 org-tracker rows the ladder reads + KRA 1) → the Lead rating math
  (19 weighted lines → 4 pillars 50/25/15/10 → Final Rating, calculation verbatim in the tooltip).
- **Shape honesty:** not a tree and not a pure hierarchy — a linear spine (levels) + a bipartite graph
  (areas↔rows share rows: APC read by 2 areas + a rating line) + one true tree (the rating roll-up). Three
  edge kinds: solid teal "area is evidenced by this row" (32) · dashed teal "rating line reads this row"
  (24) · grey "rolls up by weight" (23). 82 nodes / 79 edges; same hover/click-pin/tooltip grammar as 🕸️.
- **Muted, named in the footer:** the 5 team rows the ladder never cites (Branding Content Assets Delivered,
  Cost per Vernacular Content Hour, Cost per Branding Content Asset, Platform Runtime Cost per Active
  Learner, Roadmap Items Completion — the last one PM-seat-run) as a standing red-pen invite. Comp bands
  deliberately left in the 🪜 ladder artifact, not repeated here.
- Builder docs/handoff/artifacts/build_career_map.py **ast-extracts WIRING/PILLARS/SURFACE/PM_ROLE from
  build_role_cards.py** (stays in lockstep with the shipped ladder; repo path with scratchpad fallback) and
  resolves every read against kra_training_sheet.xlsx row names via a 9-entry alias map — unresolvable reads,
  wired/review drift (14/7), or a changed muted set fail the build loudly. Regen after any ladder or
  team-view change.
- One-surface-per-approval: published standalone; NOT embedded into the 🗺️ Content OS site pending a
  separate approval. No existing artifact touched.

## 2026-08-25 — AI Engineer Ladder v3: agent-first redesign (🪜 + 🗺️ + 🧗 republished, same URLs)
- **Ladder v3 shipped on Pavan's "Go"** — the five rungs are now: **Associate AI Engineer** (reframed as a
  6-month internship — manages agents from day one, A1–A2), **AI Engineer** (merger of AI Engineer 1 + 2;
  ≥1 year in role before Senior eligibility, A3), **Senior AI Engineer** (new force-multiplier rung, ≈2× an
  AI Engineer's complexity-weighted surface, A4), **AI Engineer Lead** (same seat — people outcomes define
  it; span ~5–8 ⚑HR), **AI Engineer 3** (unchanged, org surface). Titles keep "– [Domain] Learning Systems".
- **New machinery in the cards:** written **promotion gates** on every transition + a **stay bar** per rung
  (what it takes just to hold the seat); the **A1–A4 Agent Scope scale** grading agent work; two matrix rows
  rewritten agent-first via AREA_OVERRIDES (▲): **Production Systems** (manage/improve agents → build 2–3
  adopted agents → orchestrate agent systems → run the fleet through people) and **Learning Systems Design**
  (Pavan's "invent new ways to teach with agentic AI + rigorous measurement" line at Senior). Learning
  Systems Design now carries 4 read keys (Module-Quiz Score Bands + Summative/Formative Achievement added)
  — evidence edges 32 → 35.
- **Migration ruling (approved):** stretch-target yes · title-on-clearing yes · title-before-clearing no.
  **Comp:** numbers parked with HR — cards carry band-status lines only (stipend ⚑HR; merged band under
  review; Senior band new ⚑HR; Lead/3 inherit their bands). Strawman numbers never shipped.
- **🪜 republished** (label v3-agent-first): role_cards.xlsx + html regenerated, 7 tabs, "What changed in v3"
  box. **🗺️ site rebuilt + republished** (label ladder-v3-embed; capabilities carried forward): was-sublines
  and the v3 box stripped for the wide audience, comp bands kept off-site (they live in 🪜 + the xlsx),
  site-only retitle AI Engineer 3 → "Head of [Domain Portfolio] Learning Systems" (directional). **🧗
  rebuilt + republished** (label v3-ladder-sync): climb band retitled via NEW_TITLE, ramp-evidence beam
  label, ▲ tooltips carry the agent-first matrix text, 82 edges (ev 35 · rd 24 · tr 23).
- Builders: build_role_cards.py carries all v3 texts (canonical source); build_site.py sub1s updated
  (was-strip generalized); build_career_map.py now ast-extracts AREA_OVERRIDES too. comp_boxes_cache.json
  unchanged by the rebuild.
- Queued separately (not in this pass): standing Progression Policy doc, bus-factor register, goal-vs-reality
  memo, CSI + Content–Central role cards, comp numbers with HR/Varun.

## 2026-08-25 — Freshness row redefined + ladder lineage terms removed (all five artifacts republished)
- **Tech Stack Freshness Rate rewritten** (FS & CS Core Section B, row 18) on Pavan's approval. A **topic**
  is now defined in the row itself: PPT + recorded video session + practice content + quiz content (plus
  question pools, adaptivity and the domain learning environment where the topic carries them), and the
  **Domain Catalogue's hours ≈ the topic count**, so the catalogue is the surface of record. A refresh
  reworks the topic against the feedback that landed on it (reactive + proactive channels) and is
  **capacity-planned as a from-scratch rebuild, not a patch** — Pavan's assumption, stated as an assumption
  rather than a claim that everything changed. Version currency (tools, frameworks, libraries, IDE /
  playground / cloud setups on current stable or LTS) is audited inside every refresh. Row name, unit (%),
  frequency (Monthly) and the Q1 budget (100) are unchanged — the name is load-bearing in three builders.
- **Domain complexity now scales the target, inside the same row.** Workload standard recorded: one AI
  Engineer's surface ≈ **100 topics at FullStack / GenAI complexity per 6-month cycle**; Senior ≈ **2× that,
  complexity-weighted**. A lighter-refresh surface (English, Aptitude, programming fundamentals, CS Core,
  Mathematics, DS & Algo) carries **roughly double** the topic count, and those roles are weighed more
  aggressively on **Learning Systems Design** and **Production Systems** — the refresh costs less there, so
  the invention and the agent build are where the load sits. The Industry Upgrades wiring note carries the
  same definition so the ladder and the tracker can't drift.
- **Legacy ladder terms removed** from every output on Pavan's instruction — the v2/v3 lineage sublines
  ("was Associate SDE — reframed as a 6-month internship", "merger of SDE 1 + SDE 2 (AI Engineer 1 + 2 in
  v2)"), the `class="was"` render + its CSS, the "What changed in v3" box (replaced by "How to read the
  cards"), the ▲ tooltip's v3 reference, and the four remaining "v3" mentions in card copy. Audit method:
  base64 payloads stripped before pattern counting (the site embeds two xlsx as base64 — short tokens like
  `SDE` hit those payloads and read as false positives). Final audit clean across all five HTMLs + both xlsx.
- **New `INLINE_RETITLE` pass in build_role_cards.py** — ordered longest-first so "SDE 1+" resolves before
  "SDE 1"; it catches source-doc text that the v3 overrides don't replace (e.g. the Mentorship cell
  "Receives mentoring from SDE 1+"). **build_career_map.py now ast-extracts `INLINE_RETITLE` too** and
  applies it after `AREA_OVERRIDES`, with an assert — the map reads literals straight from the source, so a
  runtime transformation in the shipped builder is invisible to it unless replicated. That leak had surfaced
  in a node tooltip.
- **build_site.py:** the was-subline strip and its `assert n_was == 5` are gone — the source itself is clean
  now, so there is nothing left to strip. The two "What changed in v3" sub1s are gone for the same reason.
  All downstream guard asserts kept (no "formerly", no `class="was"`, no "AI Engineer 3", no "was Associate
  SDE", 5 download buttons, Section A 19 / B 29 / C 4).
- **Republished, same URLs:** 🧭 kra_training_sheet · 🪜 role_cards (`lineage-terms-removed`) · 🕸️ kpi_graph
  (`freshness-topic-surface`) · 🧗 career_map (`lineage-terms-removed`) · 🗺️ content_os
  (`freshness-row-lineage-clean`, `capabilities` omitted so the stored `downloads:true` and contract pin
  0.2.12 carry forward). 🎯 hod_kpi_onepager untouched. **Note:** the 🧭 training sheet covers org KRAs only
  and carries no team-view rows — the Freshness rewrite is visible on 🗺️ (FS team view row 18), on 🕸️ (node
  `t_fs_17`) and in the downloadable xlsx.
- **Held, not built:** the KRA 5 Employability placements-count input — Pavan asked to hold it, so no
  placements metric entered the tracker, the ladder or the framework draft.
- **Review draft, uncommitted:** `docs/handoff/workbench/proposals/role_progression_merit_framework.md` —
  the Sales BDM → ASM framework's first two sections (eligibility criteria + the 8-KPI / 12.5% merit matrix)
  adapted per rung. Delivered to Pavan for review; deliberately not committed and not shipped to an artifact.

## 2026-08-25 — Stay bars rewritten in merit-matrix terms + cost bars rebased (🪜 + 🗺️ republished, same URLs)

- **The ladder's "Holding the role" section now reads in the merit framework's terms** (Pavan's "Go, ship it
  with the glossary line" after preview). One rule under every bar, stated once in the section lead: your
  rung's eight scored rows at budget — 100%, no governance breach; below budget more than twice in 12 months
  breaks the bar; two consecutive cycles below starts a structured gap conversation with your Lead — a
  conversation, not a demotion. Per-rung bars rewritten to name the actual rows: Associate = the readiness
  scorecard on the ramp schedule + governance from day one · AI Engineer = the four output rows at budget
  (Freshness 100% on ≈ 200 CWT, CWT share of team velocity rows, APC 90%, Summative 35% + Formative 23%) +
  2–3 agents (A3) mandatory + the four governance rows never breached + rating floor · Senior = the ≈ 400 CWT
  surface held ("Senior isn't a medal, it's a load") + A4 live + mentorship on record · Lead = ≥ 85% of the
  team's owned rows at budget ⚑ + business impact + people outcomes as governance · AI Engineer 3 =
  directional until dept/org budgets land. Chain preserved: stay bar(R) = own matrix at baseline; the next
  rung's stay bar is what the peak trigger demonstrates pre-title.
- **Cost bars rebased (ruling 10, Pavan, all numbers explicitly adjustable):** an objective practice item —
  FIB, MCQ, MMCQ, any type — **≤ ₹3** · a coding question **under ₹100 baseline**, scaled by domain
  complexity: **~₹200 FullStack / GenAI** (a question is effectively a project) · **up to ₹300 DS & Algo**
  (editorials + brute-force + efficient solutions). Carried in the bars and in a STAY_NOTES line under the
  stay-bar table (html + xlsx). CpLH ₹10,000 unchanged.
- **CWT glossary shipped (the approved "glossary line"):** CWT — complexity-weighted topics: topic count ×
  the domain complexity multiplier; ≈ 200 per AI Engineer per 6-month cycle (= ≈ 100 topics at FullStack /
  GenAI 2.0×), Senior ≈ 400. Rendered under the stay-bar table in both outputs + a tie-in at the
  topic-surface key point. Second STAY_NOTES line carries the low-churn slot-swap (Freshness → LSD impact ·
  Business Impact → Pedagogy Initiative Impact; refresh audit still 100%).
- **Conversion gate softened per ruling 5:** "gold-standard comparisons, eval passes" → the responsible
  reviewer — their mentoring AI Engineer or Senior — confirms the intern's reviews catch what their own
  review would catch, sampled on real work through the ramp.
- **Republished, same URLs:** 🪜 role_cards (`stay-bars-matrix-terms`) · 🗺️ content_os (same label,
  `capabilities` omitted — stored `downloads:true` + contract pin 0.2.12 carried forward). 🧗 career map
  untouched (build_career_map.py consumes neither GATES nor STAY — verified by grep). 🎯 🧭 🕸️ untouched.
- **Framework draft updated in place (still uncommitted):** ruling 10 added to §10, the Associate + AI
  Engineer matrices' cost rows rebased to the new numbers, the "next surface" item marked shipped.
- **Known-stale, deliberately not touched:** tracker FS Section B still carries **Cost per MCQ ₹40** and
  **Cost per Coding Question ₹400** (visible on the 🗺️ team view and 🕸️). Ruling 10 implies a row rename +
  budget change — separate tracker surface, awaiting Pavan's call.

## 2026-08-25 — Stay bars reformatted as per-rung merit-matrix tables (🪜 + 🗺️ republished, same URLs)

- **Representation only — content unchanged.** Pavan: format the holding-the-role section for readability,
  "like the 8-KPI Matrix format in the sales doc … represent the points specific to domain in some coloring."
  Every number, gate and footer line from the 25 Aug stay-bar rewrite is preserved verbatim; what changed is
  the shape: prose paragraphs → one matrix table per rung.
- **Per-rung tables (html):** each of Associate / AI Engineer / Senior / Lead now renders as a 5-column
  table — Category (A — Output / B — Governance, rowspanned) · The row · The bar — hold at 100% · Gate ·
  Weight (12.5% each) — exactly 4 output + 4 governance rows per rung, asserted in the builder. Context line
  above each table, footer line (ramp cadence / rating floor) as a caption below. AI Engineer 3 stays a
  directional paragraph — it has no scored matrix by design.
- **Domain specifics as colored chips:** complexity carried by a sequential teal ramp — {lo} Low 1.0×
  English · Aptitude · Mathematics (200 topics) · {md} Medium 1.5× Programming · CS Core · DevOps (133) ·
  {hi} High 2.0× FullStack · GenAI (100) · {vh} Very High 2.5× System Design · DS & Algo · DS/ML (80) — same
  ≈ 200 CWT everywhere; slate {lc} chips mark the low-churn slot swaps (→ LSD impact · → Pedagogy Initiative
  Impact). A key line explains Gate semantics (Mandatory / breach zeroes the 12.5% slice + blocks
  eligibility / ⚑ number not locked) and the chip legend sits in the section lead.
- **xlsx: new Stay Bars tab (Tab 3, 8 tabs now).** Same per-rung matrices in sheet form (Category · Row ·
  Bar · Gate · Weight), key + legend up top, STAY_NOTES + CWT glossary at the end; the Gates & Scope tab's
  stay block is now the one-rule line + a pointer to the new tab. Chip tokens render as plain text in the
  sheet. All "7 tabs" mentions bumped to 8 (ladder subtitle, builder comment, site footer).
- **Single source of truth:** the STAY structure in build_role_cards.py now carries (level, context, footer,
  rows) with inline chip tokens; chip_html() renders the colored spans, chip_txt() strips tokens for the
  xlsx — both outputs read the same literals.
- **Republished, same URLs:** 🪜 role_cards + 🗺️ content_os (both `stay-bars-matrix-format`; site
  `capabilities` omitted — stored `downloads:true` + contract pin 0.2.12 carried forward, confirmed).
  Site retitle intact: the new stay h3s pick up the global "AI Engineer 3" → "Head of [Domain Portfolio]
  Learning Systems" replace (5 mentions, 0 raw). 🧗 untouched — build_career_map.py consumes neither GATES
  nor STAY. 🎯 🧭 🕸️ untouched.

## 2026-08-26 — Learning-conversion chain replaces quiz bands + alignment; cost rows renamed/rebased (all six artifacts republished)

- **The dept scoreboard's Module-Quiz Score Bands (8 budgeted rows) and Content–Assessment Alignment (2
  budgeted rows) are retired**, replaced by a three-stage learning-conversion chain — 6 rows, B3 + B4 × 3
  stages, at tracker rows 4–9. Pavan's ruling: "i am fine with those calls you have taken. also add those 3
  conversions. can retire content-assessment alignment may be. Lets use Summative, formative only for now.
  might change them later."
- **The three stages (per cohort):** Practice-Completed → Module-Quiz ≥ 8.0 (teaching effectiveness,
  monthly) · Module-Quiz ≥ 8.0 → Formative ≥ 8.0 (transfer / teach-to-the-quiz check, monthly, two-sided —
  Assessments-dept instruments) · Formative ≥ 8.0 → Summative ≥ 8.0 (cram-vs-retention, per semester —
  guards the 50% Summative weight in SPI, the lagging metric Pavan flagged). Anti-gaming pair: FS Practice
  Attempt-to-Completion Rate (B 38). Terminology is Summative / Formative only (biweekly SA = Formative,
  Grand SA = Summative); names may change later.
- **Budgets ship blank** — "blank until the first measured cycle" (org-tracker precedent): measure first,
  set bars after. The ≥ 8.0 bar sits one SPI band above the org target by design.
- **Band distribution + alignment survive as read-only DA/DE diagnostic cuts**, not scored rows; the
  tracker legend's forward-move entry (4) records the retirement.
- **Cost rows renamed + rebased in the same pass (clears the 25 Aug known-stale note):** Cost per MCQ ₹40 →
  **Cost per Objective Practice Item ₹3** (any objective type — FIB / MCQ / MMCQ …) · Cost per Coding
  Question ₹400 → **₹100 baseline / ~₹200 FullStack-GenAI (project-like) / ≤₹300 DS&Algo (editorials +
  brute-force + efficient)** — all "rebased Aug 2026, adjustable". Q1 Jul actuals preserved in remarks (MCQ
  B ₹40 · A ₹26 — 1,347 items / Coding B ₹400 · A ₹163 — 131 questions).
- **Surface deltas:** 🧭 tracker 24 numbered rows, 6 xlsx tabs · 🕸️ flow map 20 org rows, dept mirrors
  [11, 7, 1], 81 nodes / 77 edges · 🧗 career map 20 org metrics, 83 nodes / 82 edges ("Cost per MCQ" alias
  dropped) · 🪜 ladder evidence lists, GenAI progression area + LSD prose re-pointed at the chain (org
  scoreboard "SPI Score Bands" read kept — it names the org KRA 1 row, not the retired dept rows) · 🎯
  one-pager 14 passages replaced · 🗺️ site rebuilt from children (Section A 15 formula rows, B 29 rows,
  asks 4; both xlsx downloads re-embedded).
- **Republished, same URLs, all `conversion-chain-v1`:** 🧭 🕸️ 🪜 🧗 🎯 🗺️ (site `capabilities` omitted —
  stored `downloads:true` + contract pin 0.2.12 carried forward, confirmed). Note: 🎯 is link-shared with
  viewers pinned to an earlier version — republishing moves the live version only; the pin must be moved
  from the share menu for link viewers to see this update. 📋 dept OS sheet stays stale / deferred.
- **Framework draft updated in place (still uncommitted):** §2.1 QL → SR → ER mapping row now names the
  learning-conversion chain, unit-cost trend row renamed, Senior stay-bar note re-pointed, residue bullet
  closed out as a shipped-26-Aug record.

## 2026-08-26 — Stay bars rewritten in person language; low-churn slot-swap dissolved (🪜 🗺️ 🧗 republished)

- **Pavan's four rulings (the Go):** (1) Culture & Values comes OUT of the eight scored rows — it stays as
  a rating pillar (10%) and as the eligibility gate, never a matrix row. (2) Unit-cost trend: "−10% per
  year can be the direction may be… −40% per year is the target." (3) Associate feedback→backprop inputs
  glide to **zero by the final two months** of the internship (a glide, not a hard zero). (4) **Lead rows
  untouched this pass** — "lead inputs lets see after these are applied. its the same treatment for it as
  well." The Lead matrix gets the person-language rewrite in a later pass, after he reviews this one.
- **The redesign: each rung's stay bars now read as the eight things *this person* is answerable for**, not
  eight tracker rows with a name attached. Associate / AI Engineer / Senior fully rewritten (8 rows each);
  LSD + PII become standard occupants for AI Engineer and Senior. Dropped as matrix slots (they survive as
  review reads, not monthly rows): Hours + Pieces split, Summative + Formative conversion rows, the Senior
  catch-all row. The Associate's 25%-of-team-throughput share moves from monthly matrix row to **gate
  evidence** (⚑ 25% floor note on Gates req 3).
- **Low-churn slot-swap dissolved.** The {lc} chip and the swap paragraph are deleted everywhere; freshness
  is simply 100% of whatever the audit calls, agentic throughput 90% for everyone — freed low-churn
  capacity reads into LSD + PII instead of swapping rows.
- **Two new fixtures on every stay table:** a culture-gate line in the key ("a Culture & Values flag in the
  cycle blocks eligibility whatever the score — culture is rated in the pillars (10%), never scored as a
  row") and a decisive-slice footnote ("These eight are the decisive slice for this seat — the rest of the
  team view is answered at team level by the Lead (≥ 85% of rows in band) and run day to day by the PM.").
- **Scope ladder stated in three places** (stay bars · WIRING Foundation note · AREA_OVERRIDES "Scope of
  Work"): Associate = half a domain's surface ≈ 100 CWT across the internship · AI Engineer = a domain
  across all products ≈ 200 CWT/cycle · Senior = across domains, all products ≈ 400 CWT · Lead = the
  team's whole surface through people.
- **Surface deltas:** 🪜 ladder + xlsx rebuilt (8 tabs, 72 kpi chips) · 🗺️ site rebuilt from children
  (A 15 chips / B 29 rows / asks 4; both xlsx re-embedded; new stay text picks up the AI Engineer 3
  retitle) · 🧗 career map rebuilt — the AREA_OVERRIDES entry flows into node a0's tooltip ("Scope of
  Work ▲", 83 nodes / 82 edges unchanged). comp_boxes_cache.json byte-identical — untouched.
- **Republished, same URLs:** 🪜 🧗 `stay-bars-person-language`, 🗺️ `stay-bars-person-language-embed`
  (site `capabilities` omitted — stored `downloads:true` + contract pin 0.2.12 carried forward, confirmed).
  🎯 🧭 🕸️ untouched. 🎯 link-viewers remain pinned to their earlier version.
- **Framework draft mirrored in place (still uncommitted, 13 edits):** §§4–6 matrices replaced with the
  same eight person-language rows; §3.3 retitled "Low-churn domains — the slot-swap, dissolved (26 Aug)";
  §2.3 culture-not-a-row bullet + coverage-rule paragraph; §7 Lead matrix carries a pre-note that it
  predates this pass by ruling; §10 gains rulings 11–14 (now "Rulings — landed 25–26 August 2026").

## 2026-08-26 — Ladder slims (gates → policy doc), Content OS goes lean/link-based (🪜 🗺️ republished)

- **Pavan's ordered edits (from the nine-part message):** (1) Vocabulary bridge section cut from the
  ladder — not needed. (2) Promotion gates cut from the ladder — they move to a separate **Progression
  Policy & Merit Framework** artifact ("similar to sales doc. Draft one and keep it with you").
  (3) Content OS sections 2–4 stop re-rendering artifact content — reference the URLs instead, with the
  KPI Map and Career Growth Map hyperlinked in and the updated xlsx re-embedded, to save tokens; a full
  generated playbook may be asked for later, after all inputs land. (4) The "Carried verbatim from the
  framework except the rows marked ▲" explainer line removed from 21 Progression Areas. (5) The Associate
  stay-bar "their" wording dropped — rows renamed to "Topic surface", "Content issues", "Recurrence",
  "Unit costs".
- **🪜 ladder rebuilt** (build_role_cards.py −96/+26): gates block + vocab bridge deleted; STAY_LEAD now
  opens "How you climb lives in the Progression Policy & Merit Framework — its own document; this says
  what keeping the seat means."; intro + footnote point at the policy doc; xlsx Tab 2 renamed **Agent
  Scope** (was Scope & Gates), workbook stays 8 tabs; ▲ markers themselves KEPT (tooltip + xlsx key)
  — only the explainer sentence went.
- **🗺️ Content OS rewritten lean** (build_site.py full rewrite): the org one-pager stays the only
  embed; Levels 2–4 are now link-reference sections — 🧭 tracker, 🕸️ KPI Flow Map (dept + team ends),
  🪜 ladder, 🧗 Career Growth Map as refcards with standalone-artifact links; both xlsx masters
  (kra_training_sheet.xlsx + updated role_cards.xlsx) still embedded with download buttons; footer
  carries the full 5-artifact roster. Page 177,282 chars (was ~311KB). **Structural win: build_site.py
  now reads only hod_kpi_onepager.html + the two xlsx — child-artifact republishes no longer force a
  site rebuild** (only one-pager or xlsx changes do).
- **Policy draft created and held:** docs/handoff/workbench/proposals/progression_policy_merit_framework.html
  — the four promotion gates verbatim (their new home), composition + floors + merit mechanics, per-rung
  matrices, DRAFT banner. **Not published, not committed** — goes live only when Pavan calls for it.
- **Republished, same URLs:** 🪜 `gates-to-policy-lean`, 🗺️ `lean-link-sections` (site `capabilities`
  omitted — stored `downloads:true` + contract 0.2.12 carried forward, confirmed). 🎯 🧭 🕸️ 🧗
  untouched — git confirmed zero career-map ast inputs changed. comp_boxes_cache.json byte-identical.
- **Discussion items 6–9 (couplings, Associate repetition, the Lead rung) answered in chat — nothing
  shipped on them without a go.**
