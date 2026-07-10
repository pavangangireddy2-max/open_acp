# Proposal — Continuous Improvement Culture ("never twice")

> For the 91-person Content/Curriculum department. Goal: a reported issue never recurs —
> fixed at root cause. The trick is that "root cause" must be **enforceable, not
> aspirational**: this doc defines it as an artifact change, wires the loop into the
> existing system (gates, docs, skills, contracts, digests), and sizes the cadence for
> 91 people. Proposal v1 — 2026-07-10.

## 0. Team reality (headcounts, 2026-07)

Content 60: Aptitude 7 · English 7 · DS&ML 10 · DS&Algo 10 · FullStack 12 · GenAI 4 ·
Systems & Infra (CSI) 7 · Pedagogy 3. Plus: Product + DA 10 · Engineering 12 · Graphic
Designers 9. **Total 91.** (Org-design reconciliation: CSI ≈ cs_core + system_design +
devops_testing stacks; the Pedagogy team (3) are the natural stewards of the E-gates and
the pedagogy verdict pass; Graphic Designers are the rendering/asset layer — the exact
owner the deck asset-contract gap was waiting for.)

## 1. The enforceable definition (the whole culture in one rule)

> **An issue is "root-caused" only if closing it changed at least one durable artifact.**

There are exactly five artifact layers a real fix can land in:

| the root cause was… | the fix lands in | example |
|---|---|---|
| knowledge was wrong/missing | an **intelligence doc / registry / manifest** | stale AI-tutor flag → manifest corrected |
| procedure was wrong | a **skill / SOP** | stems kept naming the answer → skill rule added |
| a check was missing | a **gate / eval + golden-negative entry** | wrong answer key shipped → C02 execution gate + the item added to golden negatives |
| a seam was ambiguous | a **contract artifact** (item contract, packaging manifest, data-request spec) | course_id join broke analytics → "join by session_id + content hash" made a non-negotiable |
| the substrate can't do it | a **platform contract-debt register item** | lint markers leak error answers → registered debt with owner + generation-side mitigation rule |

If a closure changed none of these, it was a patch — the register keeps it open at
class level. This single rule converts "be careful next time" (vigilance, decays) into
"this failure class is now impossible or auto-caught" (structure, compounds).

## 2. The loop (report → never again)

1. **Intake — one register.** Every issue (student-reported content error, instructor
   report, gate escape, data/id break, delivery complaint, process friction) lands in ONE
   issue register with: id · class · severity · scope (stack/course/product) · reporter.
   No WhatsApp/Slack-only issues — if it isn't in the register, it didn't happen.
2. **Triage (daily, minutes):** severity + one routing decision per the org seams
   (stack team / Ops / SLE / product pod / platform). Two flags decide depth:
   **escape?** (did it reach students?) and **repeat?** (class seen before?).
3. **Fix the instance** (fast lane — hours). Never blocked on the RCA.
4. **Fix the class** — escapes and repeats get a **15-minute blameless mini-RCA**
   (template: what happened · why ×5 · which artifact layer · what change). Output is a
   change in one of the five layers, by the owning team.
5. **Add the tripwire:** golden-negative entry, regression test, drift-audit rule, or
   EOD-loop check — whatever makes the class auto-caught next time.
6. **Broadcast:** one line in the CHANGELOG + the EOD digest's "made impossible this
   week" section. Learning that isn't distributed is local memory, and local memory quits,
   rotates, and forgets.

**Definition of Closed = four checkboxes:** instance fixed · artifact changed (which one) ·
tripwire added · broadcast line written. The register template enforces it.

## 3. Issue classes and owners (routing table)

| class | examples | owner of class-fix | tripwire home |
|---|---|---|---|
| content defect | wrong key, ambiguous stem, broken snippet | stack team (verdict) + Ops (gate) | golden negatives / C-gates |
| pedagogy defect | overloaded slide, missing recap, wrong lever | Pedagogy team | E-gates / session skills |
| gate escape | defect passed all gates to students | Ops (gate gap analysis — mandatory RCA) | new/patched gate |
| delivery/experience | player bug, adaptive misbehaviour, tutor error | SLE | eval or platform debt |
| product/ops | schedule mismatch, section-level complaint themes | product pod | delivery-quality doc + process |
| data/id | broken join, id drift, exposure bias | DA + Ops | non-negotiables + drift audit |
| platform | grader, IDE, lint, completion API | Engineering | contract-debt register |
| process friction | rework loops, unclear handoffs | lane lead | skill/SOP or seam contract |

## 4. Cadence at 91-person scale (deliberately light)

- **Daily:** triage by lane stewards (~10 min); EOD digest carries new issues + closures.
- **Weekly (30 min per lane):** review open classes, repeat-issues (any repeat = automatic
  agenda item), celebrate gate catches. Content lanes: the stack team. Ops/SLE/product/
  platform: their own.
- **Monthly (60 min, dept):** the recurrence review — HOD-chaired. Only three questions:
  which classes repeated (why did the tripwire miss?) · which escapes happened · which
  five-layer changes shipped. Not a status meeting; a systems meeting.
- **Full RCA is rationed:** only escapes and repeats. Everything else is class-tagged at
  triage so patterns surface in the register without ceremony. At ~91 people expect
  20–50 issues/week initially; the ration keeps RCA burden to a handful.

## 5. Roles (no new headcount)

- **Quality steward per team** (rotating monthly, 11 at a time): runs triage + weekly
  review for their lane. Rotation makes quality everyone's muscle, not a person.
- **Pedagogy team (3):** calibration stewards — own E-gate quality, judge↔reviewer
  agreement, the pedagogy verdict pass.
- **Central Ops:** owns the register tooling, gate harnesses, golden sets, and the
  escape-RCA discipline; publishes the monthly recurrence report from the register.
- **HOD:** chairs monthly recurrence review; protects blamelessness; arbitrates seam
  disputes (resolved by contract change, per the org design).

## 6. Metrics (all derivable from the register + system dashboards)

- **Repeat-issue rate** — the north star; classes recurring after closure. Target: →0.
- **Escape rate** — defects reaching students per release/course; and **catch rate** —
  % of defects stopped by gates before review/students (should climb as tripwires grow).
- **Time-to-class-fix** (report → artifact change), separate from time-to-instance-fix.
- **Tripwire count** (gates + golden negatives + audit rules) — should only grow.
- **% closures with an artifact change** — the culture's honesty meter; if it drops,
  people are patching.
- Recognition follows the metrics: celebrate reporters (finding is positive), gate
  catches, and class-closures — never punish the person nearest the defect.

## 7. Proof this already works here (tell these stories at kickoff)

1. **BODMAS letter-mapping item:** flagged DROP in the mining verdict layer → later
   observed live in a student's practice run. Instance: retire. Class: drop-rule in the
   question doc. Tripwire: golden negative. That item class can never re-enter a bank.
2. **Wrong-key family (`22657adf`…):** keyed SyntaxError, real behaviour TypeError —
   caught by *executing* the corpus. Class fix: C02 key-re-derivation gate. Now every
   key is executed before a human ever sees the item.
3. **Lint-marker leak:** error answers revealed by the editor. Root cause: platform
   can't disable lint (substrate). Fix landed in TWO layers: contract-debt register item
   (Engineering) + generation-side rule (no statically-lintable bugs as error answers).

The department has been doing "never twice" at the artifact level for a month. This
proposal just makes it the way all 91 people work.

## 8. Rollout (two weeks)

- **Week 1:** stand up the register (sheet or tracker — one, not many); publish the
  five-layer definition + 4-checkbox close; name the first 11 stewards; seed the register
  with the known open classes (do-not-port list, contract-debt items).
- **Week 2:** first weekly lane reviews; wire register → EOD digest ("made impossible
  this week"); schedule the first monthly recurrence review.
- **Day 30:** first recurrence report; adjust triage thresholds from real volume.
