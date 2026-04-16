# Knowledge Model

## Purpose

This document explains how Open ACP should treat its wiki, skill graph, and stack-specific knowledge.

The central design decision is:

- the wiki should stay shared
- the skill graph inside it should become stack-aware

So the correct model is **not** one duplicated wiki per stack.

## Canonical Rule

The short version is:

- yes, the skill graph should be stack-specific
- no, the underlying wiki should not be fully duplicated per stack

## Canonical Inputs vs Runtime Knowledge

The wiki is not the canonical home for every kind of knowledge.

The intended rule is:

- manifests and catalogs stay canonical for designed inputs and structured references
- seeded source files stay canonical for runtime-ingested text evidence
- the runtime knowledge store (`storage/wiki`) stores synthesized operating knowledge

So for example:

- product definitions belong in manifests
- NIAT CSVs belong in catalogs
- learner, hiring, competitor, and curriculum reference markdown belongs in sources
- runtime skill entities and stack overlays belong in the wiki

And importantly:

- those canonical source files should not live under `src/`

See also:

- [Source And Guidance Model](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/source_and_guidance_model.md)

## Why This Matters

Some skills are reusable across many stacks:

- Python
- Git
- SQL
- Docker

But those same skills behave differently by stack.

Examples:

- `python` in `genai`
  - used for LLM apps, RAG systems, agent tooling, evaluation, deployment
- `python` in `dsa`
  - used as an algorithmic expression language
- `python` in `reactjs`
  - may be peripheral or irrelevant

So the wiki should not create three fully separate copies of Python as if they are unrelated.
But the system also should not treat Python as identical in all stacks.

## Recommended Data Shape

The cleanest long-term structure is:

### 1. Global Canonical Entity Layer

This is the shared reusable knowledge layer.

Examples:

- `skill_python`
- `skill_git`
- `skill_sql`
- `skill_rag`
- `audience_segment_career_switcher`
- `competitor_datacamppro`

These are not duplicated per stack by default.

### 2. Stack-Specific Skill Profile Layer

This captures how a canonical skill behaves inside a specific stack.

Examples:

- `stack_skill_profile(genai, python)`
- `stack_skill_profile(dsa, python)`
- `stack_skill_profile(genai, rag)`

Important implementation rule:

- this should be stored as a **stack-scoped overlay**, not as a normal canonical wiki entity
- in other words, `skill_python` remains the shared entity
- `python in genai` is an overlay profile of that same skill, not a second independent skill entity

Useful fields include:

- relevance score for that stack
- role in the stack
- prerequisite depth
- prerequisite skills
- downstream skills
- pedagogy notes
- assessment implications

### 3. Stack-Specific Relationship Layer

This captures graph edges that are specific to a stack.

Examples:

- in `genai`
  - `python -> rag`
  - `python -> llm_api_integration`
  - `rag -> agent_evaluation`
- in `dsa`
  - `python -> arrays`
  - `arrays -> recursion`
  - `recursion -> trees`

This is where the skill graph becomes truly stack-specific.

## What Should Be Shared vs Scoped

### Shared

- canonical skill identity
- display title
- stable entity id
- broad description
- general evidence history

### Stack-Scoped

- demand or relevance score
- prerequisite edges
- sequencing
- role in the curriculum
- assessment implications
- pedagogy notes

## Runtime Implementation Shape

The current intended runtime storage shape is:

```text
storage/wiki/
  entities/
    skill_python.md
    skill_rag.md
  stack_profiles/
    genai/
      skill_python.md
      skill_rag.md
    dsa/
      skill_python.md
```

So:

- `entities/` stores canonical reusable entities
- `stack_profiles/` stores stack-scoped overlays for those entities

This keeps the canonical/shared layer and the contextual/stack-specific layer separate.

## How Loop A Should Use This

Loop A should continue to ingest shared and stack-specific source inputs.

It should then:

1. update canonical entities when the skill itself is new or generally revised
2. update stack-specific profiles and edges when the change is really stack-local
3. write product-aware runtime summaries only as derived wiki knowledge, not as canonical product definitions

That means signals can influence both:

- the shared wiki entity
- the stack-scoped graph view
- the runtime product summary layer

without requiring a brand-new wiki per stack.

## How Loop B Should Use This

Loop B should not consume only a flat skill list.

Over time it should consume:

- canonical skills
- stack-specific relevance and sequencing
- learner implications
- relationship structure for the chosen stack

That would let curriculum generation reason more accurately about:

- which skills are foundational in this stack
- which skills are optional
- which sequencing paths make sense
- what must appear in learning and assessment alignment

## Storage Implications

The architecture should eventually support three storage views:

1. canonical entity store
2. stack-specific graph/profile store
3. runtime indexes and logs

At the file-backed stage, this can still be represented in a shared runtime wiki plus derived stack views.
Later, it could become:

- relational records for entities and evidence
- graph-oriented or structured relationship storage for stack edges
- retrieval views for fast stack-aware curriculum design

## TODO: Wiki Knowledge Model Implementation

The target architecture is clear, but the repo is not fully there yet.

TODO:

- introduce explicit stack-scoped skill profiles alongside shared canonical entities
- introduce stack-scoped relationship overlays without duplicating the whole wiki
- add canonical guidance inputs for stack-profile creation so Loop A can shape stack-specific skill roles, pedagogy notes, and assessment implications from designed sources instead of relying only on signal extraction
- add retrieval views that can answer stack-aware curriculum questions from the shared wiki
- later add product-aware retrieval overlays without turning products into separate wikis
- keep product manifests and structure profiles canonical while allowing Loop A to write derived `product` summaries into the runtime wiki
- keep runtime wiki state in `storage/wiki` while treating manifests and curated sources as canonical inputs

## Example Conceptual Shape

One way to think about it is:

```text
skill_python
  shared identity and broad description

stack: genai
  demand_score: high
  role: foundational
  prerequisites_for: [rag, llm_api_apps, agent_tooling]

stack: dsa
  demand_score: medium
  role: implementation_language
  prerequisites_for: [arrays, strings, recursion]
```

This keeps the knowledge model compact while still respecting stack-specific instructional reality.

## Current Repo State

Today, the repo is still closer to:

- shared runtime entities
- light stack-aware behavior through manifests and prompts

The first runtime slice of stack overlays is now present:

- canonical entities still live in `storage/wiki/entities/`
- stack-scoped skill overlays now live in `storage/wiki/stack_profiles/<stack>/`
- Loop A writes these overlays during skill-graph updates
- Loop B can now read stack-profile summaries from the runtime wiki context

The full graph-overlay and retrieval story is still future work, but the canonical-vs-overlay boundary is now explicit in the runtime layer.

## Why This Is Better Than Separate Wikis

Separate per-stack wikis would create:

- duplicate entities
- drift in definitions
- harder cross-stack reasoning
- duplicated maintenance

A shared wiki with stack-scoped graph overlays gives:

- reuse
- consistency
- stack specificity
- cleaner evolution into richer graph storage later
