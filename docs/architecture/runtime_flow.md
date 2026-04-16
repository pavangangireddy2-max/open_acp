# Runtime Flow

## Loop A: Intelligence

Loop A ingests signals and updates the system's operating knowledge.

Bootstrap mode is allowed in Loop A: if stack-specific raw inputs are thin or missing, the loop should continue with shared and generic seed sources, surface explicit coverage warnings, and let the runtime wiki compound from those inputs instead of blocking execution.

Within Loop A, the intended chain is: signals -> detected patterns -> wiki entity updates. Pattern detection should actively guide later skill, learner, and competitor extraction instead of being treated as a disconnected side report.

The current intended Loop A flow is:

1. ingest signals
2. detect patterns
3. update skill graph
4. update learner model
5. update competitor map
6. update product context
7. update wiki index

Product note:

- product and structure manifests are canonical
- Loop A writes only a derived runtime summary for explicit products
- stack-only runs skip product wiki writes and keep moving
- for clean simulations, it is valid to reset `storage/wiki` and rebuild runtime knowledge from scratch

Knowledge-model note:

- Loop A now updates both canonical skill entities and stack-scoped skill overlay profiles
- the canonical entity answers “what is this skill in general?”
- the stack overlay answers “what role does this skill play in this stack?”

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
2. resolve product context
3. resolve structure profile
4. resolve packaging profile
5. resolve pedagogy profile
6. generate curriculum
7. compare curriculum changes
8. design courses
9. design modules
10. design topics
11. design learning units
12. design practice
13. design learning assessments
14. resolve skill-assessment requirements
15. align learning with skill assessments

`generate_differentiation` is no longer part of the core learning-design path.

Runtime policy note:

- for real product-driven runs, Loop B should eventually stop if product context is missing
- for real domain runs, Loop A and Loop B should eventually stop if domain-specific canonical inputs are missing instead of borrowing unrelated defaults

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

Loop B knowledge note:

- Loop B can now consume both canonical skill context and stack-profile summaries from the runtime wiki
- this is still a lightweight context feed, not yet a full stack-graph retrieval system

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
