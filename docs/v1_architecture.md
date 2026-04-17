# Open ACP V1 Architecture

## Purpose

V1 is an incremental migration of Open ACP, not a rewrite. The M0-M4 system stays the historical baseline, and V1 reshapes the architecture so the codebase can support stronger pedagogy control, stricter runtime behavior, and better knowledge/style source management without breaking the working foundation.

## Baseline Preserved From M0-M4

- Loop A gathers intelligence and compounds knowledge through the wiki.
- Loop B creates a curriculum and module plan.
- Loop C executes stage-based content pipelines.
- Loop D evaluates outputs and routes fixes.
- YAML pipeline manifests, stage director markdown skills, schemas, and tool discovery are already proven patterns.

## Hybrid Architecture

### 1. Orchestration Layer

Code remains responsible for:

- outer-loop sequencing across A -> B -> C -> D
- deterministic fix routing
- evaluator execution
- memory and storage reads/writes
- pipeline-level blocking or abort behavior

### 2. Agent Execution Layer

Within a loop, stage execution follows the OpenMontage-style pattern:

- pipeline manifests define stages and runtime policy
- markdown skills define stage behavior
- tools provide capability implementations
- schemas define artifact contracts
- reviewer and checkpoint meta-skills define quality protocol

### 3. Knowledge and Style Source Layer

Canonical tracked knowledge is:

- source manifests
- shared seed inputs
- raw source files
- style corpus exports
- derived human-authored analyses

Generated wiki pages, `index.md`, and `log.md` are runtime state and belong under `storage/wiki`.

## Pedagogy Model

### Session-Level Contract: `pedagogy_profile`

This answers: "What learning experience is this whole session trying to be?"

Initial repo-wide vocabulary:

- `concept_progression`
- `worked_example_scaffold`
- `project_build_along`
- `guided_tool_walkthrough`
- `practice_with_feedback`
- `assessment_evidence_check`

Profiles are resolved deterministically from `(domain, content_type)` using fallback order:

1. exact domain/content-type match
2. content-type default
3. global default

### Section-Level Contract: `teaching_mode`

This answers: "What are we doing in this section right now?"

First-wave concept modes:

- `motivation`
- `prior_knowledge_bridge`
- `concept_explain`
- `worked_example`
- `guided_practice`
- `reflection_summary`

First-wave project modes:

- `project_context`
- `concept_explain`
- `architecture_reasoning`
- `guided_build`
- `verification_checkpoint`
- `integration_demo`
- `reflection_summary`

`pedagogy_profile` sets the overall experience. `teaching_mode` controls local section behavior.

## Style Layer Model

V1 style composition is explicitly layered:

1. pedagogy core
2. pedagogy profile
3. format config
4. stack/domain config
5. brand config

This style context is injected during generation and review, not only during `brand_polish`.

## Wiki Model

The wiki follows a Karpathy/Wiki-V2-inspired split:

- tracked source inputs live under `knowledge/`
- runtime wiki state lives under `storage/wiki`
- generated entities, logs, and indexes are rebuildable artifacts

This keeps Git clean while preserving compounding intelligence.

## First-Wave Runtime Changes

- Loop B no longer asks an LLM to pick the pedagogy framework.
- Loop B resolves `pedagogy_profile` deterministically.
- Loop B now starts with explicit pre-design resolution:
  - product context
  - structure profile
  - packaging profile
  - design-priority profile
  - time-budget context
  - pedagogy profile
  - brief generation
- Loop B uses a course-native curriculum contract:
  - `generate_curriculum` emits packaged `courses`
  - explicit `levels` are not a required output shape
  - topic placement is deferred to later design stages
- Loop B is moving from a coarse curriculum step into a richer curriculum-design chain:
  - brief generation
  - curriculum generation
  - curriculum change visibility
  - packaging resolution
  - course/module/topic/unit design
  - practice and learning-assessment design
  - external skill-assessment alignment
- Loop C consumes the course-native curriculum output plus downstream module/topic/unit design context.
- Loop C stages follow: generate -> parse -> schema validate -> review -> revise -> persist.
- First-wave pipelines use `strict_execution`, which blocks on schema or review failures after bounded retries.

## First-Wave Pipeline Migrations

### `concept_explainer`

Stage order:

1. objectives
2. outline
3. core_content
4. activities
5. brand_polish
6. slide_deck

### `project_building`

Stage order:

1. project_brief
2. objectives
3. outline
4. core_content
5. activities
6. brand_polish
7. slide_deck

## Migration Roadmap

### V1-M0

- standalone Git repo bootstrap
- clean ignore rules
- `main` baseline snapshot
- `v1` working branch

### V1-M1

- architecture package
- repo-visible source manifest model
- style layering contract

### V1-M2

- runtime wiki relocation to `storage/wiki`
- style corpus normalization
- stack/domain manifests and configs

### V1-M3

- deterministic pedagogy resolution
- strict execution and review loop
- shared runtime compatibility shims

### V1-M4

- `concept_explainer` migration

### V1-M5

- `project_building` migration

### Post First-Wave

- broader pipeline rollout
- Wiki V2 retrieval and decay
- batch execution and REST API
- continuous learning automation
