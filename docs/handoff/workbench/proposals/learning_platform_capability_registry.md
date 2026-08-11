# Learning Platform — Capability Registry v1 (for HOD review)

> The denominator for the Capability Adoption Rate KPI (LP-4, kpi_system_v3 §15).
> A capability isn't "shipped" until it has a row here with instrumentation — the
> adoption gate. Grouped by the User-Flows cut (taxonomy archived at
> knowledge/raw/corpora/department/learning_platform/). Sources: Anurag's roadmaps
> (Mar–Oct'25), Product↔Content requirements workbook, Jul+Aug'26 monthly roadmaps.
> Instr. = adoption/usage instrumentation exists. 2026-08-12.

## Flow 1 — Platform Discovery

| capability | live on | instr.? | baseline / status | PM |
|---|---|---|---|---|
| Course & dashboard discovery | all | ? | GRIT mis-surfacing fixed Jul; personalization unmeasured | Aryan |
| Content search | all | partial | works for curriculum topics; hidden-topic gaps known | Anjali |

## Flow 2 — Core Learning Outcomes (shared base)

| capability | live on | instr.? | baseline / status | PM |
|---|---|---|---|---|
| AI Tutor | all | partial (evals being built) | **24% weekly adoption** (Jul 13–Aug 3); agentic enhancement in progress | Lokeshwar |
| Live / Classroom Quiz | NIAT | being added (in-quiz events) | reliability defects known (throw-outs, freezes); module-quiz→quiz-code mechanics planned | Rohan |
| Video player + Hotspots | all | ? | improved-hotspots concept (predict-before-clip) unscheduled | — |
| Reading material / Tutorials | all | partial | load failures under high concurrency (fix in progress); podcast/interactive exploration clubbed into Revision | Aryan |
| Summary cheatsheets | all | ? | AI-tutor-for-cheatsheet concept (Anurag) unscheduled | — |
| My Notebook | Academy, Intensive, NIAT (Jul) | partial | **400 DAU Academy, low engagement**; V2 revamp approved | Aryan |
| Error reporting & feedback collection | all | partial | unclear-feedback 32% (IDE lane); in-quiz event capture planned | Rohan |
| Progress tracking / question bank | all | partial | question-bank enhancements in testing (filters, streaks) | Rohan |

## Flow 3 — Curriculum-specific learning

| capability | live on | instr.? | baseline / status | PM |
|---|---|---|---|---|
| Adaptive MCQs | rolling out (Aptitude → all) | dashboard on Aug roadmap | adoption unknown — the dashboard IS the fix | Anjali |
| Adaptive Coding | FullStack (to prod) | ? | multi-curriculum rollout under discussion | Sarthak |
| Programming Coach | pilot | offline evals planned | non-adoption being diagnosed; control-cohort framing | Lokeshwar |
| Bookmarks | all | yes | **~100 users/mo; 632 returners, 60% dead clicks**; target 50% adoption, +100% usage | Sarthak |
| Revision (preparatory) | building (NIAT first) | no | students leaving to external AI tools for revision; flashcards/NotebookLM asks clubbed here | Sarthak/Aryan |
| Practice Leaderboard (weekly, college-level) | NIAT rollout | ? | practice attempt rate ~20%, target +20–25pp | Sarthak |
| Gamified practice sessions | building | ? | overlaps leaderboard — consolidate | Sarthak |
| In-app code playgrounds (HTML/CSS/JS, Python, JS, Java, C++) | programming courses | via DP dashboards | usage vs IDE split unmeasured | — |
| Cloud IDEs & plugins (React, Node, Spring Boot) | FullStack | via DP dashboards | reliability/latency = DP lane | Sarthak |
| n8n learning environment ⚓GenAI | GenAI courses | partial | exam support blocked; 8-step submission friction; LLM-judge → testcase eval blocked | Lokeshwar |
| Public submissions · Publishing | web courses | ? | — | — |
| Guiding Questions ⚑ | programming | — | LMS-simplification lists it among obsolete-feature candidates — **retire or re-launch, decide** | — |
| NxtTalk (voice speaking practice) ⚓English | English/NIAT | no | latency 30s–2min (DP fixing to <1s); activity unit-type integration planned | Aryan |
| Interactive question types (FIB variants, drag-reorder; match-the-following) ⚓English/Aptitude | English, Aptitude | ? | in development | Anjali |
| SQL environment ⚓SQL | SQL courses | ? | outcome case owned by SQL domain; LP keeps only design-system/dark-mode consistency | Aryan |
| DSA visualizer ⚓DS&Algo | DSA | ? | outcome case owned by DS&Algo domain; LP lens = UX consistency + instrumentation | — |
| ROS 2 IDE (Gazebo + editor workspace) ⚓Robotics | Robotics | ? | shipped Jul; domain-anchored | Rohan |

## Flow 4 — Assessment & Evaluation

| capability | live on | instr.? | baseline / status | PM |
|---|---|---|---|---|
| Module quiz | NIAT | partial | integrity change: quiz-code onboarding like live quiz | Rohan |
| Exams (combined, IDE-based, contests) | NIAT/all | partial | IDE exam + combined-exam loading in requirements flow | — |
| Proctoring & integrity | NIAT | exploring | integrity-metrics doc done (Jul); Face ID gaps; honeypots; GPT-proof content types — candidate future KPI | Anjali |
| Coding evaluation & judges | all coding | partial | subtask-feedback redesign on hold; testcase 3–10x scale readiness; new compiler arch migrated | Rohan |
| Mentor Dashboard *(staff-facing)* | building (P0) | n/a student | early-support view of student activity/progress | Lokeshwar |
| Instructor activity tracking (English speaking) *(staff-facing)* | building | n/a student | activity logging + marks upload | Anjali |

## Cross-cutting experience properties (not capabilities — they move LE, not adoption)

Dark mode (coding done — 41% code at night; rest of platform pending) · new design system ·
top-bar redesign · mobile app experience (15% of sessions, 20-min avg) · offline downloads.

## The lens model (v1.1 — capabilities are shared; metrics are lane-owned)

One capability, up to four metric lenses — ownership attaches to the METRIC, never the
object, so the one-owner rule holds:

| lens | question it asks | owner of those metrics |
|---|---|---|
| Platform (LP) | is it adopted, engaging, consistent? | Learning Platform |
| Domain (LD) | does it teach — valid evaluation, real upskilling? | the owning domain |
| Infra (DP) | does it run — availability, latency, cost? | Developer Platform |
| Product (PLE) | is it delivered/configured right per product? | Product Learning Experience |

**⚓ Domain anchor**: a named anchor means the capability exists for one domain, which owns
its outcome case (build-vs-retire, pedagogy value). Anchored rows stay in this registry —
one registry, not per-domain lists — and LP's lens narrows to platform-wide concerns
(design consistency, instrumentation). Unanchored rows are cross-domain platform surfaces
where LP carries the full adoption case.

## Reading the registry

- **The "instr.?" column is the first month of work**: mostly `?`/partial. LP-4 (Capability
  Adoption Rate) can only report on instrumented rows — instrumenting the registry IS the
  Aug–Sep roadmap ask.
- ⚑ retirement candidates get a decision, not silence (Guiding Questions; gamified-practice
  vs leaderboard overlap).
- Staff-facing capabilities (Mentor Dashboard, instructor tracking) are registry rows but
  score on staff adoption, not student adoption.
- Every new roadmap row that ships a capability must add/update a registry row — same
  never-orphaned rule as the KPI list.
