# Storage And Memory

## Storage Categories

Open ACP has five distinct storage categories.

## 1. Tracked Source Inputs

These belong in Git because they are canonical inputs:

- raw knowledge sources
- learner and competitor seed files
- source manifests
- style corpus exports
- derived human-authored analyses
- schemas, prompts, and pipeline definitions

## 2. Runtime Knowledge State

These are generated and should not be treated as canonical tracked source files:

- runtime knowledge-store entities
- wiki indexes
- wiki logs
- crystallized runtime knowledge artifacts

These should live under `storage/wiki` or another runtime-owned location.

This runtime layer should eventually support both:

- canonical shared entities
- stack-specific graph or profile views

Current implementation note:

- canonical entities live under `storage/wiki/entities/`
- stack-scoped skill overlays live under `storage/wiki/stack_profiles/<stack>/`
- product summaries are derived runtime entities, not canonical catalogs

For controlled reruns or clean simulations, it should be acceptable to wipe `storage/wiki`
and rebuild the runtime knowledge store from canonical manifests and source inputs.

## 3. Runtime Design Artifacts

These are generated design-stage artifacts from Loop B and should not be treated as
canonical source inputs:

- `brief.yaml`
- `curriculum.yaml`
- `courses/index.yaml` and `course.<id>.yaml`
- `modules/index.yaml` and `module.<id>.yaml`
- `topics/index.yaml` and `topic.<id>.yaml`
- `units/index.yaml` and `unit.<id>.yaml`
- later `unit.<id>.yaml`, `practice.<id>.yaml`, and `assessment.<id>.yaml`

These belong under `storage/design/<domain>/<cycle_id>/`.

This layer should become the source of truth for downstream design-stage reads during a
run. In other words:

- manifests and catalogs define canonical input truth
- `storage/design` defines accepted runtime design truth for the current cycle

## 4. Execution Outputs

These are generated artifacts from pipeline runs:

- per-stage JSON outputs
- final assembled markdown
- future rendered assets

These belong under `outputs/`.

## 5. Memory Stores

The system conceptually wants multiple memory types:

- working memory
  - transient state carried during a run or graph execution
- episodic memory
  - run records, cycle summaries, and historical execution traces
- semantic memory
  - reusable knowledge structures and retrieval-oriented memory
- feedback memory
  - evaluator outputs, insights, and fix history

Today some of this is file-backed. Over time, this can mature into more durable stores such as:

- PostgreSQL for episodic and feedback records
- vector or hybrid retrieval stores for semantic memory
- richer graph-like structures for wiki relationships

## Skill Graph Storage Direction

The recommended direction is:

1. shared canonical entities
2. stack-specific skill profiles
3. stack-specific relationship edges

This means the system should not duplicate the whole wiki per stack.

Instead, it should support:

- one shared `skill_python` entity
- separate stack-aware interpretations of that skill for `genai`, `dsa`, and other stacks

Current runtime example:

```text
entities/skill_python.md
stack_profiles/genai/skill_python.md
stack_profiles/dsa/skill_python.md
```

Conceptually, that suggests future storage shapes such as:

- entity records
- stack profile records
- relationship or edge records
- runtime search and indexing views

## Storage Design Rule

The key rule is:

- version canonical inputs
- persist runtime state separately
- never confuse generated knowledge views with tracked source-of-truth inputs

That separation is what keeps the system reproducible without making Git carry every mutable artifact.
