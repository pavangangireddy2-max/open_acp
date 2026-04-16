# System Layers

## 1. Orchestration Layer

The orchestration layer is responsible for the outer system behavior:

- running Loops A -> B -> C -> D
- routing fixes and follow-up work
- carrying run-level state
- coordinating gate behavior

This layer should stay deterministic and code-driven. It is the part of the system that benefits most from explicit graphs, typed state, and stable routing rules.

It should also own:

- stage ordering inside loops where routing semantics matter
- review checkpoints between major decisions
- compatibility shims during migrations
- cross-loop state handoff rules

## 2. Pipeline Execution Layer

The pipeline execution layer is where content is actually produced. It is driven by:

- YAML pipeline manifests
- stage director markdown files
- JSON schemas
- tool registry integrations
- review and checkpoint protocols

This layer is intentionally more agentic than the orchestration layer. The model has room to make content and pedagogy decisions inside the bounded contract of a stage.

Today, Loop C is the clearest example of this layer:

- stage prompts define what to generate
- schemas define what is acceptable
- review logic determines whether the stage can proceed

As Loop B becomes richer, this layer should eventually consume more explicit curriculum structure:

- course
- module
- topic
- learning unit type
- practice intent
- assessment context

## 3. Knowledge and Guidance Layer

This layer provides the reusable inputs that shape the system:

- source manifests
- structured catalogs
- seeded source documents
- exemplar corpus assets and derived analyses
- runtime guidance playbooks for brand, pedagogy, domains, and delivery behavior

The key design rule is that not all knowledge is equally canonical:

- manifests, catalogs, sources, corpus assets, and guidance playbooks are tracked source material
- generated wiki pages and indexes are runtime state

Another important rule is:

- the wiki stays shared
- stack-specific graph behavior sits inside that shared wiki model rather than forcing separate wikis per stack

See also:

- [Source And Guidance Model](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/source_and_guidance_model.md)

## 4. Evaluation and Learning Layer

This layer converts produced content into system feedback:

- evaluator scores
- failing elements
- fix routes
- crystallized lessons

Over time, this layer should become more rigorous and more calibratable, especially where DSPy-backed optimization and evaluator tuning become part of the system.

It should also distinguish clearly between:

- learning-quality feedback
- curriculum-structure feedback
- external skill-assessment alignment feedback

That distinction matters because Loop D should eventually route issues not only to "Loop B" in general, but to specific curriculum-design stages inside Loop B.
