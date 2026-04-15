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

## Interface Growth

As the system matures, evaluation and learning should also support:

- batch execution
- service interfaces such as REST APIs
- richer retrieval and search
- knowledge graph style relationships
- cross-run performance monitoring

The main principle is that learning should not only change content. It should also improve the system's own standards, memory, and control logic.
