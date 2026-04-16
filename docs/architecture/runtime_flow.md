# Runtime Flow

## Loop A: Intelligence

Loop A ingests signals and updates the system's operating knowledge.

Bootstrap mode is allowed in Loop A: if stack-specific raw inputs are thin or missing, the loop should continue with shared and generic seed sources, surface explicit coverage warnings, and let the runtime wiki compound from those inputs instead of blocking execution.

Within Loop A, the intended chain is: signals -> detected patterns -> wiki entity updates. Pattern detection should actively guide later skill, learner, and competitor extraction instead of being treated as a disconnected side report.

Typical outputs:

- wiki entries
- drift observations
- skill or market updates
- learner or competitor signals

## Loop B: Curriculum

Loop B translates intelligence into instructional structure.

It is responsible for:

- curriculum mapping
- curriculum change visibility
- packaging-aware course, module, topic, and learning-unit design
- pedagogy profile resolution
- practice and learning-assessment design
- external skill-assessment requirement resolution
- learning-to-skill assessment alignment

This layer should decide the educational shape of the output before content generation begins.

The current intended Loop B flow is:

1. load wiki context
2. resolve pedagogy profile
3. generate curriculum
4. compare curriculum changes
5. resolve packaging profile
6. design courses
7. design modules
8. design topics
9. design learning units
10. design practice
11. design learning assessments
12. resolve skill-assessment requirements
13. align learning with skill assessments

`generate_differentiation` is no longer part of the core learning-design path.

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

Loop C still works against the older module-oriented compatibility layer today.
But as Loop B becomes richer, Loop C should increasingly consume:

- selected course context
- selected module context
- selected topic context
- learning unit type
- practice intent
- learning-assessment context

So the effect on Loop C is architectural now, even where the repo has not fully migrated every content pipeline to those richer inputs yet.

## Loop D: Evaluation and Backpropagation

Loop D evaluates outputs and decides what kind of remediation is needed.

Typical results:

- content fixes
- pedagogy fixes
- brand fixes
- curriculum fixes

The long-term goal is not only to score outputs, but to create reliable improvement work that can be routed back into the right loop or stage.

This means Loop D should eventually become more specific about Loop B targets.

Instead of routing only to broad curriculum nodes, it should be able to point remediation toward:

- curriculum generation
- packaging resolution
- module design
- topic design
- learning-unit design
- practice design
- learning-assessment design
- skill-assessment alignment

## Inner vs Outer Agentic Behavior

Open ACP should remain:

- deterministic at the loop-routing level
- agentic at the stage-execution level

That split keeps the system understandable while still letting stage-level generation and review benefit from model reasoning.
