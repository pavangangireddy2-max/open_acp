# open_acp

Agentic Content Production System for educational content generation across 16+ pipeline types and a 4-loop closed-loop architecture.

## V1 Migration

The `v1` branch is the incremental migration layer on top of the M0-M4 baseline. It keeps the system runnable while introducing:

- a hybrid LangGraph + stage-director execution model
- a layered pedagogy/style system
- deterministic `pedagogy_profile` resolution
- strict first-wave execution for `concept_explainer` and `project_building`
- runtime wiki outputs under `storage/wiki` instead of tracked source-tree wiki state

See [docs/v1_architecture.md](/Users/pavangangireddy/Desktop/projects/open_acp/docs/v1_architecture.md) for the full architecture package and migration roadmap.
