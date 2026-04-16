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

Useful fields include:

- demand score for that stack
- importance weight
- readiness expectation
- prerequisite depth
- common misconceptions in that stack
- recommended pedagogy notes

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

The architecture direction above is the next clean step, not a fully finished implementation.

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
