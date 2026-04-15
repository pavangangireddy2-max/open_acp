# System Layers

## 1. Orchestration Layer

The orchestration layer is responsible for the outer system behavior:

- running Loops A -> B -> C -> D
- routing fixes and follow-up work
- carrying run-level state
- coordinating gate behavior

This layer should stay deterministic and code-driven. It is the part of the system that benefits most from explicit graphs, typed state, and stable routing rules.

## 2. Pipeline Execution Layer

The pipeline execution layer is where content is actually produced. It is driven by:

- YAML pipeline manifests
- stage director markdown files
- JSON schemas
- tool registry integrations
- review and checkpoint protocols

This layer is intentionally more agentic than the orchestration layer. The model has room to make content and pedagogy decisions inside the bounded contract of a stage.

## 3. Knowledge and Style Layer

This layer provides the reusable inputs that shape the system:

- raw source documents
- source manifests
- learner and competitor seeds
- style corpus exports and analyses
- brand, format, stack, and pedagogy configs

The key design rule is that not all knowledge is equally canonical:

- raw inputs and manifests are tracked source material
- generated wiki pages and indexes are runtime state

## 4. Evaluation and Learning Layer

This layer converts produced content into system feedback:

- evaluator scores
- failing elements
- fix routes
- crystallized lessons

Over time, this layer should become more rigorous and more calibratable, especially where DSPy-backed optimization and evaluator tuning become part of the system.
