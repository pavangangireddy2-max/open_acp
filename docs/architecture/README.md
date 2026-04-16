# Open ACP Architecture

This folder is the stable, high-level architecture reference for Open ACP. It is meant to help future agents and contributors understand the system without needing to reconstruct the design from code, prompts, or milestone history.

## What Open ACP Is

Open ACP is an agentic educational content production system. It combines:

- an outer orchestrator for loop sequencing and routing
- inner stage-based pipelines for content generation
- a layered knowledge and guidance system
- evaluators that score outputs and feed improvement work back into the system

## Primary Architecture Layers

1. Orchestration layer
   - Owns loop sequencing, deterministic routing, and system-level control flow.
2. Pipeline execution layer
   - Owns stage manifests, stage prompts, schemas, review, and artifact generation.
3. Knowledge and guidance layer
   - Owns canonical source inputs, catalogs, exemplar corpora, the runtime knowledge store, and guidance playbooks.
4. Evaluation and learning layer
   - Owns scoring, fix classification, and longer-term optimization/calibration.

## Core References

- [System Layers](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/system_layers.md)
- [Runtime Flow](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/runtime_flow.md)
- [Source And Guidance Model](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/source_and_guidance_model.md)
- [Curriculum Design](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/curriculum_design.md)
- [Design Priorities](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/design_priorities.md)
- [Prompt Organization](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/prompt_organization.md)
- [Product Catalog](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/product_catalog.md)
- [Knowledge Model](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/knowledge_model.md)
- [Storage And Memory](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/storage_and_memory.md)
- [Evaluation And Learning](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/evaluation_and_learning.md)

## Design Intent

The system should feel like:

- code-governed at the outer loop level
- agentic and flexible inside stages
- schema-backed for artifacts
- review-aware, not just generation-heavy
- compounding in knowledge rather than stateless between runs

## Near-Term Direction

The main near-term direction is to keep the architecture legible while expanding:

- first-wave migrated pipelines
- product-aware Loop A and Loop B resolution
- purpose-based cleanup of sources, corpus, analyses, and guidance playbooks
- storage and memory maturity
- curriculum design depth
- packaging-aware delivery design
- evaluator rigor
- wiki intelligence quality
- system interfaces such as APIs or batch execution

## Recommended Operator Flow

For real execution, the repo should be operated in staged review mode rather than jumping straight to
full unattended runs.

Recommended flow:

1. run Loop A one node at a time with `review-loop`
2. run Loop B one node at a time with `review-loop`
3. run Loop C one stage at a time with `review`
4. use `run --full` only after earlier checkpoints are approved

The CLI now includes `oacp guide` to show the recommended commands and operator prompt examples.

TODO:

- introduce a product layer above packaging without collapsing stack/domain curriculum design into product design
- keep course-end outputs such as `summary_cheatsheet` product-configurable rather than universally required
- continue documenting other products in the same style as NIAT as product context is collected
