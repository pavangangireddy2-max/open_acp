# Runtime Flow

## Loop A: Intelligence

Loop A ingests signals and updates the system's operating knowledge.

Typical outputs:

- wiki entries
- drift observations
- skill or market updates
- learner or competitor signals

## Loop B: Curriculum

Loop B translates intelligence into instructional structure.

It is responsible for:

- curriculum mapping
- module sequencing
- differentiation logic
- pedagogy profile resolution
- assessment alignment

This layer should decide the educational shape of the output before content generation begins.

## Loop C: Content Production

Loop C executes a stage-based pipeline for a chosen content type.

The stage lifecycle is:

1. load stage instructions
2. inject module, style, and prior artifact context
3. generate artifact
4. parse and validate artifact
5. review against declared criteria
6. revise if needed
7. persist accepted artifact

For stricter pipelines, schema and review failures should block progress rather than merely producing warnings.

## Loop D: Evaluation and Backpropagation

Loop D evaluates outputs and decides what kind of remediation is needed.

Typical results:

- content fixes
- pedagogy fixes
- brand fixes
- curriculum fixes

The long-term goal is not only to score outputs, but to create reliable improvement work that can be routed back into the right loop or stage.

## Inner vs Outer Agentic Behavior

Open ACP should remain:

- deterministic at the loop-routing level
- agentic at the stage-execution level

That split keeps the system understandable while still letting stage-level generation and review benefit from model reasoning.
