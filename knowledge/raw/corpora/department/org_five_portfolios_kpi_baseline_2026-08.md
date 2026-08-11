# Adopted org structure — five portfolios + revised KPI baseline (HOD paste, 2026-08-11)

> Verbatim archive of the HOD's summary from the org/PM thread. This is the ADOPTED
> structure (with named ownership and July roadmaps), superseding sketch-level inputs in
> earlier org discussions. Companion reconciliation: workbench/proposals/
> org_design_content_department.md §7 and kpi_system_v3_ownership.md §9–10.

## 1. Curriculum / Content organization

```text
Curriculum / Content Department
│
├── 🛠️ Developer Platform
│     Purpose: Build AI-powered engineering capabilities, developer tooling,
│       and platform services that improve engineering productivity.
│     Ownership: SDE 3 Engineering
│     July Roadmap: IDE Improvements · Agentic IDE
│
├── 🎓 Learning Platform
│     Purpose: Build reusable learning capabilities and student experiences
│       shared across all products and learning domains.
│     Ownership: 2 Product Managers
│     July Roadmap: Self Study · Revision Initiative · Practice Leaderboard ·
│       Adaptive Coding · Adaptive MCQs
│
├── 🤖 Agentic Content Platform
│     Purpose: Build AI-powered platforms and automation that accelerate
│       curriculum creation, content operations, and shared intelligence.
│     Ownership: SDE 1s Engineering
│     July Roadmap: MCP Server · 15 Agentic Workflows
│
├── 🚀 Product Learning Experience
│     Products: NIAT, Intensive, Academy
│     Purpose: Build product-specific learning experiences and interventions
│       that improve learner outcomes.
│     Ownership: 1 Product Manager
│     July Roadmap: GRIT Practice
│
└── 💡 Learning Domains
      Domains: MERN, Java FullStack, Programming, SQL & CS Core, GenAI, DS/ML,
        Aptitude, English, DS & Algo, Robotics
      Purpose: Drive domain-specific curriculum, pedagogy, and learning innovations.
      Ownership: 2 Product Managers
      July Roadmap: Programming Coach (Deep Coding)
```

## 2. Naming decisions

- **Product Learning Experience** (not "Program Experience"): NxtWave has products
  NIAT/Intensive/Academy; GRIT/BRAVE/MINT are experiences/mini-products within NIAT.
- **Agentic Content Platform** (not "AI Platform"): sits within the Curriculum/Content
  org; covers agentic systems supporting content/curriculum operations.
- **Learning Domains** covers: MERN, Java FullStack, Programming, SQL & CS Core, GenAI,
  DS/ML, Aptitude, English, DS & Algo, Robotics.

## 3. PM organization

- Learning Platform → 2 PMs · Product Learning Experience → 1 PM · Learning Domains →
  2 PMs · **Total: 5 PMs**
- Engineering-led portfolios: Developer Platform → SDE 3 · Agentic Content Platform → SDE 1s
- **Senior PM context:** Anurag currently ₹26 LPA; has an external offer of ₹36 LPA.
  Plan: replace with a Senior PM at ~₹33 LPA base — cross-portfolio prioritization,
  roadmap governance, cross-functional execution, PM mentorship.

## 4. Revised Learning Systems / Content KPI baseline (2026-08)

Deltas vs kpi_tracker_v2.csv are annotated ◄.

**Business Impact**
- % Learners in Ideal Engagement Segment — High Effort + High Value cell of the
  effort-value matrix (LE score × CME highest concept level, monthly). Leading indicator.
- Summative Skill Assessment Achievement Rate ◄ PENDING DEPRECATION (→ Ideal Engagement Segment)
- Formative Skill Assessment Achievement Rate ◄ PENDING DEPRECATION (→ Ideal Engagement Segment)
- Content-Assessment Alignment % ◄ redefined: delta between linked learning-assessment
  and FORMATIVE skill-assessment scores, learners who attempted both.
- NIAT Graded Assessment Achievement Rate — Mid-1/Mid-2/End-Sem, university-conducted.
- Launchpad Weekly Active Users ◄ mismatch RESOLVED as WAU: unique learners engaging
  with ≥1 learning unit per week; reported as monthly average. (Not leads.)

**Content Effectiveness**
- Learning Engagement Effort (LE) — passive 0.5 / active 1.0 / persistence multipliers;
  replaces DAU/WAU/MAU.
- Course Completion Rate ◄ PENDING DEPRECATION (→ LE)
- Pedagogy Initiative Impact — vs agreed baseline.
- Learner Accessed Content Completion Rate — video units opened → completed.
- Practice Attempt-to-Completion Rate — environment friction vs difficulty drop-off.
- Learning Environment Satisfaction Score — coding env / playground / cloud IDE.

**Content Velocity**
- Learning Content Hours Delivered ◄ renamed (was "No. of presentations & Cheatsheets
  Delivered"; hours definition wins).
- Vernacular Content Hours Delivered
- Practice & Assessment Content Pieces Delivered
- Branding Content Assets Delivered

**Content Efficiency**
- Cost Per Learning Hour Produced ◄ renamed (was Cost Per Presentation)
- Cost Per MCQ Generated
- Cost Per Coding Question
- Cost Per Branding Content Asset
- Platform Runtime Cost Per Active Learner
- Feedback Resolution Efficiency ◄ scope now "learning system issues"
- R&D Initiative Impact

**Content Relevance**
- Industry Update Adherence
- NIAT University Curriculum Compliance Rate
- Tech Stack Freshness Rate

**Stakeholder Alignment**
- Stakeholder Content Request Fulfillment Rate
- Cross-functional Sprint Delivery Rate

**Executive Ops**
- Operations & Growth Cost
- Creative Resource Utilisation Rate

**Content Systems & Infra (CSI)** ◄ NEW section (6 KPIs)
- NIAT Program Delivery Gap Rate — % planned NIAT program activities not
  scheduled/executed. Target 0%.
- NIAT BOS Credit Acceptance Rate — % CSI-proposed credits accepted into approved BOS.
- Cost Per BOS Approval — new approvals vs renewals separated where relevant.
- Issue Resolution TAT — university/program issues, by severity and university.
- Cost Per Vernacular Content Hour ◄ replaces "Cost Per Cheatsheet" (mismatch resolved)
- Framework Compliance Rate — Academy units vs NHQRF / Woolf frameworks.

## 5. Stated next task (from the HOD)

Map this baseline KPI library against (a) the five portfolios and (b) the NIAT
organizational KPIs. The NIAT organizational KPI list is NOT yet in this repo — pending.
