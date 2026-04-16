# Prompt Organization

## Purpose

This document describes the intended prompt layout for Open ACP.

The goal is to keep:

- pipeline-stage prompts
- loop-operational prompts
- shared meta-review prompts

clearly separated as the system becomes more product-aware and structure-aware.

Important distinction:

- prompts are not the same thing as runtime guidance playbooks
- prompts belong in `skills/...` and later `loops/.../prompts/`
- guidance belongs in the non-code knowledge layer and should eventually live under `knowledge/guidance/...`

See also:

- [Source And Guidance Model](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/source_and_guidance_model.md)

## Current State

Today the repo mostly uses:

- `src/open_acp/skills/pipelines/...`
  - for stage-director prompts
- `src/open_acp/skills/meta/...`
  - for reviewer and meta prompts
- inline prompt strings inside loop node code
  - especially in Loop A and Loop B

That works for now, but the loop-level prompt surface is starting to grow.

## Recommended Separation

### 1. Pipeline Stage Prompts

Keep these in:

- `src/open_acp/skills/pipelines/...`

These are best for:

- content-generation stages
- stage-specific review instructions
- schema-oriented artifact generation

Examples:

- concept explainer stage prompts
- project building stage prompts
- slide deck stage prompts

### 2. Loop-Operational Prompts

Introduce loop-local prompt folders later:

- `src/open_acp/loops/loop_a/prompts/`
- `src/open_acp/loops/loop_b/prompts/`
- `src/open_acp/loops/loop_c/prompts/`
- `src/open_acp/loops/loop_d/prompts/`

These are best for:

- signal analysis prompts
- product-context synthesis prompts
- curriculum-structure prompts
- alignment prompts
- evaluator routing prompts

This keeps loop logic readable and prevents long prompt bodies from being buried inside node code.

### 3. Shared Meta Prompts

Keep shared prompts in:

- `src/open_acp/skills/meta/...`

These are best for:

- reviewer prompts
- checkpoint prompts
- generic critique or revision prompts

## Why This Split Helps

- Loop prompts evolve differently from content-stage prompts.
- Loop prompts are more architecture- and policy-heavy.
- Pipeline prompts are more artifact- and content-heavy.
- Product-aware and structure-aware curriculum logic will make Loop B prompts much larger over time.
- Product-specific content constraints will later affect Loop C too.

## Recommendation

Do **not** refactor all prompts immediately.

The next clean move should be:

1. keep existing pipeline prompts where they are
2. gradually extract loop-inline prompts into loop-local `prompts/` folders
3. start with Loop B first, because it is accumulating the most architecture-specific prompting

## Suggested Migration Order

1. Loop B curriculum-generation and alignment prompts
2. Loop A signal-analysis and product-context prompts
3. Loop D evaluation/routing prompts
4. Loop C execution/review helper prompts that are not already stage skills

## TODO

- extract Loop B curriculum-generation prompt into `src/open_acp/loops/loop_b/prompts/`
- extract Loop A pattern-analysis and product-context prompts into `src/open_acp/loops/loop_a/prompts/`
- define a small shared loader/helper for loop prompt files
- later record which prompts are product-sensitive and which are stack-sensitive
