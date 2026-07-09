# Proposal — Evals & Guardrails Strategy (question generation first)

> Should the C01–C25 gates and E01–E20 criteria graduate from doc checklists to runnable
> eval suites + runtime guardrails, possibly on an LLM-ops platform (Agenta or similar)?
> **Yes to operationalizing — with a hard rule about where truth lives and a caution about
> what such platforms are actually good at here.** Proposal v1 — 2026-07-09.

## 1. Layer model (evals don't replace skills)

| layer | question it answers | we have today |
|---|---|---|
| Docs (knowledge) | what is true? | intelligence/ docs |
| Skills (procedure) | how should an agent work? | question-item-craft |
| **Eval sets** | did the output meet the bar? (offline, measured) | C01–C25 + E01–E20 as text |
| **Guardrails** | is this output allowed through? (online, enforced) | §2.6 generation gates as text |
| DSPy metric (Forge thread, locked) | what does the generator optimize against? | = deterministic gates + quality judge + reviewer verdicts |

Same definitions feed all of the bottom three: an eval set is the gate suite run offline over
golden data; a guardrail is the same gate run inline before an item reaches review; the DSPy
metric is the same suite scored. **One definition, three execution contexts.**

## 2. The decisive fact: most of our gates are CODE, not judgments

Sort the C-gates by how they're checked:

- **Deterministic (the majority, and the highest-value):** C01 execution, C02 key
  re-derivation, C03 FIB round-trip, C04 substitution/uniqueness probe, C10 key-balance
  stats, C11–C13 suite minimums + mutant-killing, C14 determinism scan, C15 whitespace,
  C16 rung conformance (static properties), C19 dedup budget, C23 runtime tag. These are
  **Python, not prompts** — a pytest-style harness that runs wherever generation runs.
  An LLM-eval platform adds nothing to these except a dashboard.
- **LLM-judged (the subjective slice):** stem clarity/register (C20), distractor
  plausibility beyond reachability (C08's judgment half), explanation/tutorial quality,
  beginner-safety, scenario appropriateness, E-series pedagogy conformance. **This** is
  where LLM-as-judge + rubric + calibration belongs — and where a platform earns its keep.
- **Human (irreducible):** reviewer verdicts (approve/edit/reject with C-rule ids) — which
  double as judge-calibration labels and DSPy gold demonstrations.

**Implication:** don't "move evals to Agenta." Build the deterministic harness in-repo as
the guardrail layer (it must run inline in Forge's pipeline), and use a platform for the
judge slice + human annotation queues + dashboards.

## 3. Why we're unusually ready: the golden sets already exist

From the mining work, we already hold labeled data most teams have to fabricate:

- **Golden NEGATIVES:** the do-not-port defect list (§4 of the question doc) — ~40+ real
  items with a known defect AND the gate that should catch each (wrong keys → C02,
  nondeterministic set prints → C14, single-visible-TC → C11, trailing-whitespace outputs →
  C15, non-firing traps → C08/C13…). This is a regression suite for the gates themselves:
  *every gate must flag its defects.*
- **Golden POSITIVES:** the best-exemplar ids named in every mining report (e.g. e359e188's
  11-case branch sweep, 9661f906's verbatim-ValueError options, 647934a2's precedence
  distractor set) — items the suite must pass and judges must score high.
- **Judge rubrics for free:** the misconception bank (distractor reachability = "which
  misconception produces this option?"), the register rules, the E-series text.
- **Calibration labels forthcoming:** reviewer verdicts from the Forge review flow, and
  empirical item stats from the ELP (discrimination ≈ ground-truth item quality).

## 4. Platform recommendation

- **Truth lives in git** — eval definitions, golden sets, judge prompts, thresholds are
  files in this repo; any platform consumes them **config-as-code** via API/CLI. If a gate
  exists only in a platform UI, it will drift from the docs and the skill. Non-negotiable.
- **Agenta** (self-hosted, prompt registry, eval runs, human annotation queues) is a
  reasonable pick for the judge slice + reviewer annotation + dashboards. Evaluate against
  two lighter alternatives before committing: **Promptfoo** (pure config-as-code, CI-native —
  best fit for the EOD loop and git-truth; weakest annotation UI) and **Langfuse**
  (open-source tracing + evals — best if we also want to trace Forge generation runs).
  Decision criteria in order: config-as-code fidelity → annotation queue quality (reviewer
  workflow) → self-host → DSPy interop (all fine via API).
- What a platform is NOT for here: the deterministic gates (in-repo harness), the docs
  (git), the skill (git), or prompt "management" of Forge's generator (that's the DSPy
  program + its gold demonstrations, versioned in-repo).

## 5. Build order (value-first, infra-last)

1. **Now, no new infra:** `evals/question_craft/` in-repo — extract golden_negative.jsonl
   (defect ids + expected gate verdicts) and golden_positive.jsonl from the corpus; implement
   the ~12 deterministic gates as a Python package with pytest; CI = "gates catch all golden
   negatives, pass all golden positives." This is ~80% of the value and doubles as Forge's
   inline guardrail module.
2. **Judge slice:** write judge prompts from the rubrics; score golden sets; measure
   judge-vs-reviewer agreement once review verdicts start flowing; tune until agreement is
   acceptable (fixed threshold per gate).
3. **Platform adoption:** when reviewer annotation volume + dashboard needs are real, stand
   up Agenta (or Promptfoo+Langfuse) reading the repo's eval files. EOD loop gains a step:
   run suite → digest regressions.
4. **DSPy optimization** (per the Forge thread) uses this same stack as its metric —
   nothing new to invent.
5. Same pattern later for pedagogy/session generation (E-series) and Echo answer quality.

## 6. Scope note on "guardrails"

Here guardrails = generation-side gates (pre-review). Delivery-side guardrails (AI-tutor
answer-leak prevention, adaptive-walk sanity bounds) are a separate, later scope — same
principle (deterministic where possible, judged where not), different pipeline.
