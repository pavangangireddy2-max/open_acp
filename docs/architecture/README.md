# Open ACP Architecture

This folder is the stable, high-level architecture reference for Open ACP. It is meant to help future agents and contributors understand the system without needing to reconstruct the design from code, prompts, or milestone history.

## What Open ACP Is

Open ACP is an agentic educational content production system. It combines:

- an outer orchestrator for loop sequencing and routing
- inner stage-based pipelines for content generation
- a layered knowledge and style system
- evaluators that score outputs and feed improvement work back into the system

## Primary Architecture Layers

1. Orchestration layer
   - Owns loop sequencing, deterministic routing, and system-level control flow.
2. Pipeline execution layer
   - Owns stage manifests, stage prompts, schemas, review, and artifact generation.
3. Knowledge and style layer
   - Owns raw inputs, source manifests, wiki/runtime knowledge, and style/pedagogy guidance.
4. Evaluation and learning layer
   - Owns scoring, fix classification, and longer-term optimization/calibration.

## Core References

- [System Layers](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/system_layers.md)
- [Runtime Flow](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/runtime_flow.md)
- [Curriculum Design](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/curriculum_design.md)
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
- storage and memory maturity
- curriculum design depth
- packaging-aware delivery design
- evaluator rigor
- wiki intelligence quality
- system interfaces such as APIs or batch execution
