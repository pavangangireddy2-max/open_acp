# Proposal — Handoff Folder Structure v2 (scope-first)

> How `docs/handoff/` scales from ~14 flat files to the full program: 10 stacks, ~50
> courses, per-product streams, plus proposals/reviews/requests — without breaking the
> bootstrap, Echo retrieval, or the EOD context-ops loop. Proposal v1 — 2026-07-08.

## 1. The two rules everything follows

**Rule 1 — inputs are not handoff docs.** Course contents (outlines, reading material,
transcripts, question exports, decks) are RAW INPUTS → they live under `knowledge/raw/corpora/`,
organized by the same scope path. `docs/handoff/` holds only **derived, agent-consumable
intelligence** and program artifacts. (This is the repo's existing purpose-based layering —
sources/corpus vs analyses/guidance — applied consistently.)

**Rule 2 — one scope path, used everywhere.** `<stack_slug>/<course_slug>` is the universal
address, identical across corpora, registries, and handoff intelligence:

```
knowledge/raw/corpora/  <stack>/<course>/...   # inputs (outlines, exports, decks, transcripts)
knowledge/registries/   <stack>/<course>/...   # the WHAT rail (node registries)
docs/handoff/intelligence/stacks/<stack>/courses/<course>/...  # derived intelligence
```

Slugs come from one canonical table (`docs/handoff/SLUGS.md`): Central Stack Catalogue name
↔ folder slug ↔ `knowledge/manifests/stacks/*.yaml` slug. Stack slugs: `programming_algorithms`,
`fullstack`, `cs_core`, `ds_ml`, `genai`, `system_design`, `aptitude`, `english`,
`devops_testing`, `physical_ai`. Course slugs snake_cased from the catalogue's internal titles
(e.g. `python`, `dsa_cpp`, `react`, `node_mongodb`, `dbms`, `math_for_cse`).

## 2. Target tree

```
docs/handoff/
├── README.md                  # the bootstrap — map, reading order, current state (unchanged role)
├── CHANGELOG.md               # one line per doc change (EOD loop appends)
├── SLUGS.md                   # canonical name ↔ slug table
├── digests/                   # EOD digests (context-ops loop)
│
├── program/                   # program-level, cross-cutting (the "why/how of the whole thing")
│   ├── agent_family_architecture.md
│   ├── context_operations.md          # adopted ops procedure (from the proposal)
│   ├── echo_design.md
│   └── plans/
│       └── ai_credits_niat_100cr.md
│
├── intelligence/              # THE CONTEXT LAYER (always-current truth; Echo's corpus)
│   ├── global/                # scope: cross-stack, cross-product
│   │   ├── products.md                 # all product families
│   │   ├── pedagogy_universal.md       # universal principles + E-eval (stack overlays split out as stacks arrive)
│   │   ├── question_craft_universal.md # the universal item-craft layer + C-gates (split from python doc when stack #2 lands)
│   │   └── platform_student_experience.md
│   ├── stacks/
│   │   └── programming_algorithms/
│   │       ├── stack.md                # stack-level overlay (pedagogy + item-craft specifics shared by its courses)
│   │       └── courses/
│   │           └── python/
│   │               ├── question_intelligence.md   # the python overlay (misconception bank, format contracts)
│   │               ├── learner_behaviour.md
│   │               └── registry_notes.md          # editorial notes; registry data itself in knowledge/registries/
│   └── products/              # product-scoped streams
│       └── niat/
│           ├── delivery_quality.md     # instructor feedback synthesis (incoming stream)
│           └── delivery_rhythm.md      # weekly schedules synthesis (incoming stream)
│
└── workbench/                 # POINT-IN-TIME artifacts (not truth; superseded when adopted)
    ├── proposals/             # forge review UX, context ops, this doc, ...
    ├── reviews/               # adaptive PRD review, future PRD/design reviews
    ├── requests/              # data requests + intake specs (learner behaviour, co-failure, per-stack intake)
    └── addenda/               # scope addenda, one-off notes
```

## 3. Why scope-first (not type-first)

- **Work arrives per course** (a course's outline + questions + behaviour land together) and
  **agents consume per scope** ("everything about Python" beats "the pedagogy slice of
  everything"). One folder = one working set.
- Matches the knowledge-layer model (stack curriculum + product overlay) and the resolution
  semantics agents already know.
- Echo retrieval stays whole-doc: a course question pulls that course's folder + its stack.md
  + global/ — a clean, cheap retrieval ladder (course → stack → global).
- Folders are created **lazily** — first artifact creates the path; no 50 empty dirs.

## 4. The context/workbench split (why it matters)

`intelligence/` = always-current truth: the EOD loop updates it, Echo indexes it, freshness
is enforced. `workbench/` = timestamped thinking: proposals, reviews, requests. They are
consumed differently — a proposal is *adopted into* a context doc (then the proposal is
history), a review is sent and done. Mixing them (today's flat folder) makes "what is
current truth?" a filename-guessing game. `program/` sits between: slow-changing canon about
the program itself.

## 5. Split-when-second-instance rule (no speculative fragmentation)

- `pedagogy_universal.md` keeps its stack overlays inline **until** a second stack's overlay
  is authored → then overlays move to each `stacks/<slug>/stack.md`.
- `question_intelligence_python.md` splits into `global/question_craft_universal.md` +
  `courses/python/question_intelligence.md` **when the second course's mining starts**
  (the doc already has the §2/§3 seam for exactly this).
- Same for learner behaviour: python doc now; global patterns doc only when course #2 shows
  shared structure.

## 6. Migration map (git mv, one commit)

| current (flat) | new home |
|---|---|
| context_agent_family_architecture.md | program/agent_family_architecture.md |
| design_echo_rag_app.md | program/echo_design.md |
| plan_100cr_ai_credits_niat.md | program/plans/ai_credits_niat_100cr.md |
| proposal_context_operations.md | program/context_operations.md (on adoption; else workbench/proposals/) |
| context_products_all.md | intelligence/global/products.md |
| context_pedagogy_intelligence.md | intelligence/global/pedagogy_universal.md |
| context_platform_student_experience.md | intelligence/global/platform_student_experience.md |
| context_question_intelligence_python.md | intelligence/stacks/programming_algorithms/courses/python/question_intelligence.md |
| context_learner_behaviour_python.md | intelligence/stacks/programming_algorithms/courses/python/learner_behaviour.md |
| proposal_forge_review_and_adaptive_experience.md | workbench/proposals/forge_review_and_adaptive_experience.md |
| proposal_handoff_structure.md (this) | workbench/proposals/handoff_structure_v2.md |
| review_adaptive_coding_prd.md | workbench/reviews/adaptive_coding_prd.md |
| data_request_learner_behaviour_intelligence.md | workbench/requests/learner_behaviour_data.md |
| data_request_item_cofailure_python.md | workbench/requests/item_cofailure_python.md |
| addendum_cofailure_pilot_scope.md | workbench/addenda/cofailure_pilot_scope.md |
| intake_spec_question_intelligence_per_stack.md | workbench/requests/intake_per_stack_question_intelligence.md |

Also (knowledge side, same commit or the next): `knowledge/raw/corpora/*` files regrouped to
`corpora/programming_algorithms/python/…`; `knowledge/registries/python/` →
`knowledge/registries/programming_algorithms/python/`.

**Migration hygiene:** update README's index (it is the only file whose path never changes);
fix inter-doc relative links; update memory pointers + Echo corpus glob (`docs/handoff/
intelligence/**/*.md` + `program/**/*.md`); leave `git log --follow` to preserve history.
Do it in ONE commit before the per-stack expansion starts — the cheapest moment is now.

## 7. Naming conventions going forward

- Folder carries the type; filenames drop `context_`/`proposal_` prefixes.
- Dates/versions live in doc headers (+ CHANGELOG), never in filenames — except digests.
- New stream = new doc under its scope, registered in README's index the same day
  (doc-contracts skill enforces this once context-ops is scaffolded).
```
