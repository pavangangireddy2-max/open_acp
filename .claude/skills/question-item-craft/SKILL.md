---
name: question-item-craft
description: Use when creating, editing, or reviewing practice/assessment questions for any NxtWave course (coding items, MCQs, FIB, predict-output, module quizzes) — Forge generation work, item review, or bank QA. Encodes the item-craft procedure and gates; the evidence and reference tables live in the intelligence docs it points to.
---

# Question Item Craft

You are writing or judging **born-tagged** items: every item is generated INTO a
(node × rung × axis) cell from a work order — tags are never retrofitted.

## Read first (progressive — only what the task needs)

1. **Universal craft + gates** (all courses):
   `docs/handoff/intelligence/stacks/programming_algorithms/courses/python/question_intelligence.md`
   §2 (item anatomy per axis, mechanical rung definitions, distractor rules, test-suite rules,
   generation gates, C01–C25 eval set). Until a second course splits the doc, §2 IS the
   universal layer — treat it as course-agnostic.
2. **Course overlay** (facts, not procedure): same doc §3 for Python — misconception bank
   (~310 entries; distractors MUST be tagged with these ids), platform format contracts,
   idiom norms by course stage, coverage gaps, §4 do-not-port defects.
3. **Node cells**: the course registry under `knowledge/registries/<stack>/<course>/`.
4. If platform behaviour matters (grading, reveal, players):
   `docs/handoff/intelligence/global/platform_student_experience.md`.

## Non-negotiables (fail = reject, cite the gate id)

- C01/C02: execute everything — code runs, reference passes its own suite, keys re-derived
  by execution. Never ship an unexecuted item.
- C04: FIB grading is EXACT STRING MATCH → blank must admit exactly one valid string
  (substitution-probe the category pool).
- C08: every distractor = one reachable wrong execution path, tagged with a
  misconception_id from the bank. No filler options, no "None of the above".
- C13: every test case kills a named mutant; edge-class checklist per input type.
- C14/C15: determinism (no unordered exact prints, no float-repr grading, no
  trailing-whitespace-bearing outputs). Runtime = Python 3.10.
- C17: Fix-axis bugs are catalogued misconceptions, never typo hunts.
- Item contract: coding items ship a 3-step Tutorial; objective items ship an Explanation
  (commented code + bullets).
- Delivery constraints: items are single-use once answered (≥3 fresh variants per cell);
  no statically-lintable bug as an error-item's answer (portal can't disable lint).

## Procedure (generate)

1. Take the work-order cell (node × rung × axis × role). Refuse cell-less requests.
2. Pick 2–3 reachable misconceptions for the node from the bank → these become the
   distractors / the bug / the discriminating operands.
3. Draft to the axis anatomy (§2.1) at the rung's mechanical definition (§2.2).
4. Run the gates (§2.6) — execution, uniqueness probe, mutant kill, dedup budget
   (≤2 per literal-normalized template per session; clone families ≤4 stem types).
5. Emit: item + tags + misconception-tagged distractors + suite + tutorial/explanation,
   in the platform format contract (§3.1).

## Procedure (review)

Judge against gate ids; verdicts are Approve / Edit (re-run gates) / Reject with C-rule ids.
Reviewer edits are gold demonstrations — preserve them verbatim in the review record.
