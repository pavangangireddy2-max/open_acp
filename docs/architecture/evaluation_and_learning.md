# Evaluation And Learning

## Current Evaluator Shape

Open ACP already thinks in multiple evaluator dimensions:

- accuracy
- pedagogy
- engagement
- brand
- citation or provenance

This is the right direction because educational quality is multi-dimensional. A single scalar score is not enough.

## Role of Evaluators

Evaluators should do three things:

1. score outputs
2. explain failures clearly
3. produce actionable remediation signals

If an evaluator only gives a number, it is not yet useful enough for a closed-loop system.

This becomes especially important once the system distinguishes:

- content quality
- curriculum quality
- learning-assessment quality
- external skill-assessment alignment quality

## DSPy Direction

DSPy-backed evaluators are a natural future step for this system because they can support:

- better rubric shaping
- trace-based optimization
- calibration across content types
- systematic improvement of evaluator prompts or programs

The design expectation should be:

- content generation remains stage-driven
- evaluator logic becomes more programmatic and optimizable

## Continuous Learning Direction

The longer-term learning loop should include:

- crystallizing repeated insights from Loop D
- feeding stable lessons back into prompts, schemas, and configs
- upgrading retrieval and knowledge quality
- decaying stale confidence in old intelligence
- improving evaluation reliability over time

## Learning Assessments vs Skill Assessments

The architecture should treat these as different things.

### Learning Assessments

These belong inside Open ACP and support learning progression:

- classroom quizzes
- module quizzes
- assignments
- guided practice checks

### Skill Assessments

These belong to an external team or repo and support product or placement eligibility.

Loop B should align internal learning design to those external requirements rather than own the external assessment bank itself.

## Alignment Dimensions

When comparing learning design to external skill assessments, the system should evaluate:

- question type alignment
- difficulty alignment
- concept coverage alignment
- pattern alignment against industry signals
- cadence alignment

This is already becoming a first-class architectural concern in Loop B.

## Future Extension: Practice And Testing Strategy

Practice design and learning-assessment design may need their own design contracts over time.

Useful future concepts include:

- `practice_profile`
  - examples: retrieval, guided build, debugging, reflection
- `assessment_mode`
  - examples: classroom quiz, module quiz, project evidence, placement readiness

Those contracts may vary by:

- stack
- packaging
- future product constraints
- external assessment expectations

This is a natural next step once the current Loop B structural refactor stabilizes.

## Interface Growth

As the system matures, evaluation and learning should also support:

- batch execution
- service interfaces such as REST APIs
- richer retrieval and search
- knowledge graph style relationships
- cross-run performance monitoring

The main principle is that learning should not only change content. It should also improve the system's own standards, memory, and control logic.

## TODO: Backpropagation Maturity

The current Loop D routing is still too coarse for the richer artifact model now emerging in Loop A and Loop B.

TODO:

- route fixes to the earliest owning artifact stage rather than only broad loop-level targets
- distinguish fixes that belong to canonical inputs, runtime knowledge synthesis, design artifacts, and generated outputs
- add rerun-start semantics so downstream stages are recomputed from the first corrected artifact boundary
- make channel and dimension digests first-class inputs to backprop routing instead of treating all feedback as generic content noise
