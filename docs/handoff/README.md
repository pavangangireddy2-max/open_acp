# Handoff Docs — Start Here (Agent Bootstrap)

> **Purpose:** let any agent (Claude Code, OpenRouter-Claude in Cline/Roo/Continue, or a
> fresh claude.ai thread) pick up the Open ACP intelligence program with zero prior chat
> context. Every doc in this folder is standalone — no other files or conversations needed.
> Read this file first, then the docs relevant to your task. Last updated: 2026-07-09 (structure v2).

## The program in one paragraph

We are building the intelligence layer for NxtWave's curriculum/content system (Open ACP)
and the **Forge** agent family (Canon = knowledge base, Crux = mastery diagnosis, Forge =
question-bank builder; adaptivity is a separate delivery layer). Four intelligence docs are
done (products, pedagogy, question-creation, platform experience); a fifth (learner
behaviour) is commissioned to the data team. Items are generated **born-tagged** into
(node × rung easy/medium/hard × axis Read/Fix/Fill/Tweaked/Write) cells; tags are never
retrofitted. The Python course ("Programming Foundations" in the UI, course of the
Programming & Algorithms stack) is the pilot.

## Layout (structure v2 — scope-first)

```
program/        the why/how of the whole program (agent family, Echo, ops, plans)
intelligence/   ALWAYS-CURRENT TRUTH — Echo's corpus, EOD-maintained
  global/         cross-stack: products, pedagogy, question craft, platform
  stacks/<stack>/courses/<course>/   per-course intelligence (question, behaviour, registry notes)
  products/<product>/                per-product streams (delivery quality, rhythm)
workbench/      point-in-time artifacts: proposals/ reviews/ requests/ addenda/
digests/        EOD digests · CHANGELOG.md · SLUGS.md (canonical slug table)
```

Scope rule: `<stack>/<course>` is the same address in `knowledge/raw/corpora/`,
`knowledge/registries/`, and `intelligence/stacks/`. Slugs: [SLUGS.md](SLUGS.md).

## Doc index (read in this order for full context)

| doc | what it holds |
|---|---|
| [program/agent_family_architecture.md](program/agent_family_architecture.md) | **The system map** — the full 10-agent family (Canon/Crux/Loop/Relay/Forge/Lens/Radar/Panel/Prism/Docket + Compass), how they connect, locked cross-thread concepts, and where every other doc plugs in |
| [intelligence/global/products.md](intelligence/global/products.md) | All product families (NIAT/Academy/Intensive/GRIT/Launchpad/default), structure profiles, packaging, resolution semantics — fully inlined |
| [intelligence/global/pedagogy_universal.md](intelligence/global/pedagogy_universal.md) | The deck-mined pedagogy: universal principles (inlined YAML v4), stack overlays, E01–E20 eval set, session flows |
| [intelligence/stacks/programming_algorithms/courses/python/question_intelligence.md](intelligence/stacks/programming_algorithms/courses/python/question_intelligence.md) | The HOW rail for Forge (Python): corpus mine, ~310-entry misconception bank, item anatomy per axis, mechanical rungs, C01–C25 gates, format contracts, do-not-port defects |
| [intelligence/stacks/programming_algorithms/courses/python/learner_behaviour.md](intelligence/stacks/programming_algorithms/courses/python/learner_behaviour.md) | Learner-behaviour intelligence (Python): ELP analytics → registry-knob map, exposure caveats, co-failure ask |
| [intelligence/global/platform_student_experience.md](intelligence/global/platform_student_experience.md) | How the platform actually behaves (UI, grading, completion, players) + all 16 owner-confirmed answers |
| [program/echo_design.md](program/echo_design.md) | Design spec for **Echo** — the Agentic-RAG surface over this corpus |
| [workbench/requests/intake_per_stack_question_intelligence.md](workbench/requests/intake_per_stack_question_intelligence.md) | Intake spec to extend question intelligence to all stacks |
| [workbench/proposals/forge_review_and_adaptive_experience.md](workbench/proposals/forge_review_and_adaptive_experience.md) | Proposals: Forge reviewer UX + student adaptive walk |
| [workbench/proposals/context_operations.md](workbench/proposals/context_operations.md) | Context-ops: skills/agents/EOD-automation design (structure v2 assumed) |
| [workbench/reviews/adaptive_coding_prd.md](workbench/reviews/adaptive_coding_prd.md) | Simulation-backed review of the product team's IRT/Elo adaptive PRD |
| [workbench/requests/learner_behaviour_data.md](workbench/requests/learner_behaviour_data.md) | The 41-question data request delegated to DA/DE (NIAT B3, AY 2025-26) |
| [workbench/requests/item_cofailure_python.md](workbench/requests/item_cofailure_python.md) | Net-new DE ask: item co-failure clustering (+ [addendum](workbench/addenda/cofailure_pilot_scope.md)) |
| [program/plans/ai_credits_niat_100cr.md](program/plans/ai_credits_niat_100cr.md) | ₹100 Cr AI-credit consumption plan (NIAT) |

Related repo canon: `knowledge/analyses/pedagogy/universal_principles.yaml` (v4),
`knowledge/manifests/products/*.yaml` (NIAT `ai_tutor_enabled: true` corrected 2026-07-07),
`knowledge/raw/brand/` (recovered slide corpus + extracted text).

## Current state & open threads

1. **WHAT rail (node registry) — NEXT UP, critical path.** Author the Python course node
   registry from the Course Outline (32 sessions, key takeaways + outcome statements in
   `~/Downloads/Computer Programming using Python Course Contents - Course Outline (1).csv`,
   which also carries reading-material content + transcript links). Schema = the React
   exemplar (Node_ID · Node · Module · Session · Prereq · L1–L5 · Depends_On ·
   Dependency_Reason · Node_Reason; ragged depth; evidence flags), linked from
   `~/Downloads/Central Stack Catalogue - Stack.csv`. Module-1 exemplar first, then user
   editorial review (promote/fold/flatten verbs).
2. **Incoming from the user:** re-export of all questions WITH difficulty tags + tutorials +
   explanations (→ calibrate the mechanical rungs; not all explanations exist); module-quiz
   JSON (repurposed content — context only, do not mine).
3. **Delegated out → co-failure pilot DELIVERED (2026-07-10):** reviewed + content-
   adjudicated (workbench/reviews/review_cofailure_pilot.md): Loops split candidate
   confirmed (maps to LP-04/LP-06 bank families; session ≠ node proven empirically);
   full-scale run gated on **content-hash** + phi/cell-floor ranking + defect exclusion.
   Remaining ELP extracts (difficulty, discrimination, option distributions) still to come.
4. **PRD review** handed to the product owner — expect a revised adaptive PRD; hold them to
   the simulation acceptance tests and the node-coverage outer loop.
5. **Pedagogy gaps (optional):** React state/lists/events decks, a DSA algorithm-technique
   deck, and two frontend-track decks ("Getting Started with Frontend", "Leveraging Gen AI
   for accelerated learning") are still unanalyzed — user supplies decks if wanted.

## Non-negotiables already locked (don't relitigate)

- Compare learner/content data by **session_id / unit_id / question_id + content hash**,
  never course_id (ids changed); unit_ids are reused across sessions.
- FIB grading is **exact string match** → uniqueness gate C04 is mandatory.
- Runtime = **Python 3.10** for all emitted items.
- Items are single-use once answered (answer reveal) → ≥3 fresh variants per cell.
- Public Submissions are visible → novelty/rebuild constraint is real.
- Lint markers can't be disabled → don't ship statically-lintable bugs as error-item answers.
- Completion today = 80% rule; adaptive replaces it with node clearance.
- Corpus defects in the do-not-port list must never re-enter banks or analytics.

## Source data locations (user's machine)

`~/Downloads/`: question export JSON (4,963 q) · Course Outline CSVs (v1 + v2 with reading
content/transcripts) · Session-Unit linking CSV · Central Stack Catalogue CSV · CSS Part 1
deck PDF. Split/normalized question chunks (this analysis's working set) are in the session
scratchpad (ephemeral — regenerate from the JSON via the join script pattern in the question
doc §1 if needed).
