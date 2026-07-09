---
name: session-deck-craft
description: Use when outlining, drafting, or reviewing a session slide deck (PPT) for any NxtWave course — concept sessions, bridge courses, STL/API sessions, markup/visual sessions, tool walkthroughs, project builds. Encodes the mined pedagogy procedure and E-gates; evidence lives in the pedagogy intelligence doc. v1 is OUTLINE/REVIEW grade — full rendered-deck generation is gated (see Limits).
---

# Session Deck Craft

You are composing a session from **observed, evidence-trailed patterns** — not inventing
teaching style. Every structural choice should cite a pattern id from the pedagogy doc.

## Read first (progressive — only what the task needs)

1. `docs/handoff/intelligence/global/pedagogy_universal.md` — the whole toolkit:
   6 principles, 12 strategies, 15 session flows, 23 cross-cutting patterns, E01–E20 gates.
   Its stack-overlay section (§4) picks the flow family and levers for the course's stack.
2. The course's WHAT: session Key Takeaways + Outline from the course outline
   (`knowledge/raw/corpora/<stack>/<course>/course_outline.csv`) and, where it exists, the
   node registry (`knowledge/registries/<stack>/<course>/`).
3. Packaging constraints for the product (quiz cadence, module shape):
   `docs/handoff/intelligence/global/products.md` — e.g. classroom quiz every ~20 min.
4. For practice/quiz slides: the course misconception bank via the question-intelligence
   doc — quiz moments and worked examples should target catalogued misconceptions.
5. Brand/runtime playbooks when styling matters: `knowledge/guidance/` (brand, pedagogy
   profiles, instructional patterns, presentation surfaces).

## Hard rules (fail = revise; cite the gate)

- **30–40 words per slide max; ONE new concept per slide** (E04). Progressive reveal for
  anything multi-part (build-up or annotation variant; token-level for syntax templates).
- **Bookend skeleton is mandatory** (E08): WELCOME → Recap (prior session) → Agenda
  (chevron) → …body… → Quiz Time! breaks per packaging cadence → Key Takeaways (mirrors
  agenda) → Practice → Next Session → THANK YOU / ALL THE BEST. Supplementary content goes
  AFTER the closing slides.
- **Analogy before abstraction** (E02): structurally-mapping everyday analogy precedes any
  formal definition. **Bridge from the known** (E03) with side-by-side comparisons where a
  prior language/framework exists — and DROP the comparison where no clean equivalent exists.
- **Motivation lever must match the domain** (E05): aspiration for foundational CS, urgency
  for fast-moving fields, industry-adoption proof for frameworks, career/salary for
  job-track skills; every statistic carries a named on-slide source.
- **Mirror pairs teach boundaries**: paired slides/examples with flipped facts
  (`print(name)` vs `print("name")`; valid vs error one token apart).
- **Code slides**: language pill + only concept-bearing lines highlighted + output on the
  NEXT slide (predict-first); Input → Code → Output for every example; error slides follow
  write → run → see error → explain → fix → rerun.
- **Visual before textual** (E11) where a visual model exists — with REAL values in
  diagrams, and container/artifact state re-shown on every operation slide.
- ≥40% of session time is active practice (E06); practice examples target catalogued
  misconceptions, graduated easy → medium → hard.

## Procedure (outline a session)

1. Identify the **archetype** from the session's takeaways + stack overlay, and pick the
   matching flow from the doc's 15 (concept explainer / bridge course / STL-API / complexity
   analysis / markup (goal_state_preview!) / tool walkthrough / prompt-engineering /
   no-code build / project track intro / …). Name it.
2. Map Key Takeaways → the session's teaching beats; check the node registry so every
   node-bearing takeaway gets a beat and a quiz/practice moment.
3. Slot patterns per beat, citing ids (e.g. "beat 3: token_level_syntax_annotation +
   matched_output_code_slide").
4. Emit a **slide-by-slide outline**: slide no. · purpose · pattern id(s) · ≤40-word content
   draft · visual spec (diagram/code/illustration note).
5. Self-review against E01–E20; list any gate you could not satisfy and why.

## Procedure (review an existing deck)

Judge against E01–E20 + the hard rules; verdicts cite gate ids with slide numbers; propose
the minimal edit per violation. Use the pedagogy doc's observed exemplars as calibration.

## Limits (v1 — say this when asked to fully generate)

- **Outline/review grade.** Full rendered-deck generation is gated on: (a) an editorial
  verdict pass converting the pedagogy doc from descriptive → prescriptive (keep/drop per
  pattern, owner: Pavan), and (b) a rendering/asset contract (target format, brand template,
  addressable illustration assets — the 251-page library is not yet extracted).
- For rendering an approved outline, hand off to the existing deck tooling (pptx /
  tr-doc-to-ppt skills) rather than inventing layout.
