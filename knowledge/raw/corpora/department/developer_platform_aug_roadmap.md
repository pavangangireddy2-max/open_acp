# Developer Platform — Aug 2026 roadmap (HOD paste, 2026-08-11; verbatim structure)

All P0. Format: initiative → goal → metric (Aug target).

**n8n IDE**
- Proactive infra-saturation detection (concurrent usage, RDS CPU, ECS, health):
  100% of critical thresholds alerted; MTTD ≤10 min. [System Reliability]
- Cost visibility per EnrollPlan & per user: 0 → 100% attribution. [Business Impact]
- Feedback loop: categorize domain/platform/infra, route, resolve E2E; capture missing
  Workflow ID; **fix Question ID mis-tracking (Course ID currently captured as Question
  ID)**. TAT <2 days; recurring issues → 0. [Business Impact, Issue Recurrence]

**Compiler**
- Observability dashboard (cost/request, language-wise Avg/P95/P99 latency, failed evals,
  worker status, queue wait); alerts Avg>10s / P95>15s / P99>25s; Sentry critical >10 in
  5 min. Discovery < TBD sec; resolution <1 day. [System Reliability]
- Production isolation (Alpha→Tech account), CI/CD, no manual deploys; C++ P99: 10.28s →
  <5s. [System Reliability, Deployment Efficiency]

**Cloud IDE**
- Tail latency: Launch 548 users/6.7% affected → 0% (P99 121.6s→<60s) · Submit 483/9.6%
  → 0% (116.3s→<60s) · Publish 12/3.6% → 0% (98s→<60s) · npm install 590/11.6% → 0%
  (66.3s→<60s); close latency after tab close. [System Performance]
- Reliability & monitoring: detection TAT ≤1 day, resolution <2 days, observability 100%,
  all-stack dashboard, architecture docs. [System Reliability]
- Cost: terminate on tab close, per-unit cost dashboard; save $30–50 (1.8–3%). [Efficiency]
- Feedback quality: unclear feedback 32% → <15%. [Issue Resolution TAT]
- User-reported fixes (IDE preview highlight — ~30s launch avoided for 1,537 users; CCBP
  CLI docs — command doubts → 0); instant-solution flow; recurrence → 0.

**Engineering productivity**
- Branch workflow: checkout 5–10 min → 0; cherry-pick/testing ≤10 min. [Delivery Efficiency]
- Agent effectiveness: Skill UI output consistency (reuse components/colors, minimal
  manual fixes); plan-generation 30–50 min → −20%; track token usage. [Delivery Efficiency]
- Support investigation agent for CS/Ops (user-access, content/loading diagnosis from app
  context, DB, logs): internal issues same-day. [Business Impact, TAT]
