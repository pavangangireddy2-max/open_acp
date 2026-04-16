# Source And Guidance Model

## Purpose

This document defines the cleaned-up, purpose-based model for:

- canonical source inputs
- structured reference catalogs
- exemplar corpora
- derived analyses
- runtime guidance playbooks
- generated runtime knowledge

It exists because the historical repo layout mixed:

- code under `src/`
- exemplar PDFs under `knowledge/raw/brand/`
- derived analyses now being moved under `knowledge/analyses/`
- runtime guidance YAMLs under `src/open_acp/styles/`

That historical layout works, but it is hard to reason about because the names do not match the purpose.

The target direction is: **organize by usage and authority, not by history**.

## Current Migration Status

The first seeded-source cleanup slice is now in place:

- canonical seeded text inputs live under `knowledge/sources/`
- manifests point to `knowledge/sources/...` for learner, hiring, market, competitor, and curriculum reference inputs
- the older `src/open_acp/knowledge/raw/` tree has been removed

So the repo is now in a clearer state:

- `knowledge/sources/` is the canonical home for seeded text inputs
- `src/` should not carry non-code knowledge inputs

The first guidance cleanup slice is also now in place:

- runtime guidance YAMLs live under `knowledge/guidance/`
- `src/open_acp/styles/` now holds loader and resolver code only
- the first semantic split is now in place:
  - `learning_unit_types/`
  - `presentation_surfaces/`
  - `instructional_patterns/`

## Core Rule

The simplest rule is:

- only code should live under `src/`
- canonical non-code inputs should live under root `knowledge/`
- generated runtime state should live under `storage/`

## Why The Current Layout Feels Confusing

Today, there are two different non-code knowledge concepts in practice:

1. `knowledge/sources/...`
   - seeded text inputs for Loop A and Loop B
2. `knowledge/raw/brand/...`
   - exemplar PPT/PDF assets used for style and content-development understanding

There is also a third, separate concern:

3. `knowledge/guidance/...` plus `src/open_acp/styles/...`
  - runtime playbooks under `knowledge/guidance/`
  - loader and resolver code under `src/open_acp/styles/`

These are not the same thing, but the folder names make them look similar.

## Purpose-Based Naming Model

The cleaned-up naming model should be:

- `manifests`
  - canonical selectors and configuration
- `catalogs`
  - structured reference tables and CSV-backed data
- `sources`
  - canonical seeded text inputs for runtime intelligence
- `corpus`
  - curated exemplar assets such as PPT/PDF references
- `analyses`
  - derived human-authored or one-time interpreted notes from the corpus
- `guidance`
  - distilled runtime playbooks that prompts and execution actually load
- `storage`
  - generated runtime state

At the moment, the canonical top-level stack/domain inventory should be seeded
from:

- `knowledge/catalog/courses/base_course_abstract.csv`

## Target Repository Shape

```text
knowledge/
  manifests/
    stacks/
    products/
    structure_profiles/
    packaging/
    shared/

  catalogs/
    niat/
    regulations/
    courses/
    certifications/

  sources/
    shared/
      learner/
      hiring/
      competitors/
      market/
    domains/
      genai/
      cpp/
      dsa/
      reactjs/
    products/
      niat/
      academy/
      intensive/

  corpus/
    style_exemplars/
    delivery_exemplars/
    content_type_exemplars/
    extracted_text/

  analyses/
    style/
    pedagogy/
    delivery_patterns/
    content_type_patterns/

  guidance/
    brand/
    pedagogy/
    domains/
    learning_unit_types/
    presentation_surfaces/
    instructional_patterns/
    product_overlays/
    packaging_overlays/

storage/
  wiki/
  episodic/
  ...
```

## Layer Meanings

### 1. `knowledge/manifests`

This is the canonical selector and configuration layer.

It answers questions like:

- which stack exists?
- which product exists?
- which structure profile applies?
- which source files should be used?
- which packaging profile should be applied?

This layer should stay declarative and version-controlled.

### 2. `knowledge/catalogs`

This is the structured reference layer.

Examples:

- NIAT university and batch CSVs
- AICTE regulation tables
- future canonical course catalog
- future course variant matrix
- future certification registry

This layer is canonical, but more tabular than manifest-like.

### 3. `knowledge/sources`

This is the seeded text-input layer for runtime intelligence.

It should hold markdown or text that Loop A and Loop B ingest directly.

Examples:

- target-audience profile
- hiring and interview requirement summaries
- competitor summaries
- stack curriculum seeds
- domain trend notes
- product-specific academic notes

This is the canonical home for what Loop A and Loop B ingest directly.

### 4. `knowledge/corpus`

This is the exemplar asset layer.

This is where the 33 PPT/PDF references belong.

These are not ordinary Loop A intelligence inputs.
They are development-time or design-time exemplars used to extract:

- brand patterns
- delivery patterns
- content-type conventions
- visual and structural heuristics

These assets should be treated as a curated corpus, not as generic “raw knowledge.”

### 5. `knowledge/analyses`

This is the interpreted-notes layer built from the corpus.

Examples:

- `cpp_s2_analysis.md`
- `cpp_s3_stl_analysis.md`
- `cpp_s4_sessions8910_analysis.md`
- future content-type or pedagogy extraction notes

These are not runtime source inputs in the same sense as learner or hiring signals.
They are reusable design understanding artifacts.

### 6. `knowledge/guidance`

This is the distilled runtime playbook layer.

It should contain only guidance that the system actively composes into prompts or execution context.

This is now the canonical home for runtime playbooks.

### 7. `storage/`

This is generated runtime state.

Examples:

- `storage/wiki/`
- stack profile overlays
- runtime indexes and logs
- episodic traces

This layer is not canonical input.

## Guidance Model

The current `styles` folder is doing more than “style.”

It currently mixes:

- brand rules
- pedagogy runtime rules
- pedagogy profiles
- domain-specific teaching preferences
- format or delivery guidance
- some design-analysis material that is not actually runtime guidance

So the right long-term concept is not “styles.”
It is **guidance**.

### Runtime Guidance Categories

The target runtime guidance layer should be split by purpose.

#### `knowledge/guidance/brand/`

Examples:

- default brand playbook
- visual and typography rules
- tone and presentation conventions

Current likely source:

- `knowledge/guidance/brand/default.yaml`

#### `knowledge/guidance/pedagogy/`

This should contain:

- `runtime_core.yaml`
  - distilled always-on runtime pedagogy constraints
- code-level fallback defaults
  - only used when neither product manifests nor stack manifests provide a pedagogy decision
- `profiles/`
  - `concept_progression`
  - `project_build_along`
  - `worked_example_scaffold`
  - and so on

Current likely sources:

- `knowledge/guidance/pedagogy/core.yaml`
- `knowledge/guidance/pedagogy/profiles/...`

Important rule:

- rich analytical files like `universal_principles.yaml` should not be treated as runtime guidance automatically
- they belong closer to `knowledge/analyses/pedagogy/` unless a distilled runtime subset is intentionally created

#### `knowledge/guidance/domains/`

This should hold domain or stack playbooks.

Examples:

- `genai.yaml`
- `cpp.yaml`
- `dsa.yaml`
- `reactjs.yaml`

Current likely source:

- `knowledge/guidance/domains/...`

These answer:

- what teaching patterns are preferred in this domain?
- what visual patterns help here?
- what content emphases matter?

#### `knowledge/guidance/learning_unit_types/`

This should hold playbooks for artifact or unit types.

Examples:

- `video_session_unit.yaml`
- `reading_material_unit.yaml`
- `coding_practice_unit.yaml`
- `mcq_practice_unit.yaml`

This split is now the canonical runtime direction.

#### `knowledge/guidance/presentation_surfaces/`

This should hold presentation-medium playbooks.

Examples:

- `slide_backed_session.yaml`
- `screen_demo_session.yaml`
- `portal_reading_surface.yaml`

This is where the old `ppt_session` concept has been reclassified.

Important rule:

- not every video session is PPT-backed
- platform walkthroughs may be demo-backed rather than slide-backed

#### `knowledge/guidance/instructional_patterns/`

This should hold instructional-pattern overlays.

Examples:

- `concept_explainer.yaml`
- `problem_solving_session.yaml`
- `project_building_session.yaml`
- `platform_walkthrough_session.yaml`
- `induction_session.yaml`

These are not “content types” in the old overloaded sense.
They are instructional-pattern playbooks.

### Teaching Mode Contract

The runtime guidance loader now resolves a teaching-mode contract explicitly.

The contract comes from combining:

- the pedagogy profile's `allowed_teaching_modes`
- the instructional pattern's `common_teaching_mode_sequence`

So the logic becomes:

- pedagogy profile says which teaching modes are allowed
- instructional pattern says how those modes should typically be sequenced
- the loader computes the resolved intersection used at runtime

This is the main place where pedagogy profiles, teaching modes, and instructional patterns now connect.

#### `knowledge/guidance/product_overlays/`

This is later work.

Examples:

- NIAT delivery constraints
- Academy-specific support or assessment overlays
- Intensive Offline presentation constraints

This should not be the first migration step.

#### `knowledge/guidance/packaging_overlays/`

This is also later work.

It should carry packaging-sensitive delivery behavior without polluting the base stack or domain playbooks.

### What Should Not Be Runtime Guidance

The following should not be mixed into runtime guidance by default:

- large PPT/PDF corpus assets
- extracted corpus text dumps
- one-time analytical notes
- exploratory pedagogy research
- prompt bodies

These belong in `corpus`, `analyses`, or prompt folders, not in runtime guidance directories.

## Prompts Are Separate

Guidance playbooks are not the same thing as prompts.

- prompts tell the model what to do in a specific stage or loop step
- guidance tells the system what constraints and heuristics should shape that execution

So the target split is:

- `skills/...` and later `loops/.../prompts/` for prompts
- `knowledge/guidance/...` for runtime playbooks

## Current-To-Target Mapping

### Knowledge Inputs

- `knowledge/sources/domains/...`
  - future: `knowledge/sources/domains/...`
- `knowledge/sources/shared/hiring/...`
  - future: `knowledge/sources/shared/hiring/...`
- `knowledge/sources/shared/competitors/...`
  - future: `knowledge/sources/shared/competitors/...`
- `knowledge/sources/products/...`
  - canonical home for product-specific target-audience inputs and other product-scoped evidence

### Corpus And Analyses

- `knowledge/raw/brand/*.pdf`
  - future: `knowledge/corpus/style_exemplars/...`
- `knowledge/raw/brand/extracted_text/*.txt`
  - future: `knowledge/corpus/extracted_text/...`
- `knowledge/analyses/style/...`
  - canonical home for interpreted style notes

### Runtime Guidance

- `knowledge/guidance/brand/default.yaml`
  - later may be renamed to a more explicit brand-playbook id
- `knowledge/guidance/pedagogy/core.yaml`
  - later may be renamed to `runtime_core.yaml`
- code-level fallback defaults in `pedagogy_resolver.py`
  - emergency-only defaults, not a canonical source layer
- `knowledge/guidance/pedagogy/profiles/...`
  - runtime pedagogy profiles
- `knowledge/guidance/domains/...`
  - domain playbooks
- `knowledge/guidance/presentation_surfaces/slide_backed_session.yaml`
  - the canonical runtime playbook for slide-backed session delivery
- `knowledge/guidance/instructional_patterns/project_building.yaml`
  - the canonical runtime playbook for project-building sequencing

## What Is Not Needed Yet

The following changes are **not** required in the first migration slice:

1. renaming the Python code package from `styles` to `guidance`
   - the loader code can stay under `src/open_acp/styles` for now
2. migrating every prompt file
   - prompt refactoring is separate
3. turning all analyses into YAML playbooks
   - many should remain analyses
4. creating product-specific runtime guidance for every product immediately
   - product overlays should come later, only where runtime behavior needs them
5. moving runtime wiki state
   - `storage/wiki` is already in the right conceptual place
6. introducing a database-backed guidance system
   - file-backed guidance is still fine for now

## Recommended Migration Plan

### Phase 1: Freeze The Terms In Docs

Do this first.

- adopt the purpose-based naming model
- document the canonical roles of manifests, catalogs, sources, corpus, analyses, guidance, and storage
- stop calling everything “raw”
- stop calling every runtime playbook “style”

### Phase 2: Move Canonical Source Inputs Out Of `src`

Status: complete for the first seeded-source slice.

What happened:

- create `knowledge/sources/...`
- move the seeded markdown inputs there
- update manifests to point to the new paths
- remove the old `src/open_acp/knowledge/raw/` data tree

Goal:

- `src/` stops carrying canonical non-code knowledge inputs

### Phase 3: Move Runtime Guidance YAMLs Out Of `src`

Status: complete for the first guidance move slice.

What happened:

- `knowledge/guidance/...` now holds the runtime YAML playbooks
- `src/open_acp/styles/` keeps the loader and resolver code
- prompt and runtime references are being updated to point at `knowledge/guidance/...`

Goal:

- `src/` holds code
- `knowledge/` holds runtime playbooks

### Phase 3.1: Split Guidance By Purpose

Status: complete for the first semantic split.

What happened:

- retired the broad `formats/` bucket
- created explicit runtime categories for:
  - `learning_unit_types/`
  - `presentation_surfaces/`
  - `instructional_patterns/`
- updated the loader so it resolves a guidance contract and teaching-mode contract

Goal:

- guidance is composed by purpose rather than by an overloaded “format” concept

### Phase 4: Reclassify Corpus And Analyses

Then:

- move exemplar PDFs and extracted text into `knowledge/corpus/...`
- move one-time interpretation notes into `knowledge/analyses/...`
- remove the idea that these are ordinary Loop A source inputs

Goal:

- corpus and analyses become explicit design assets

### Phase 5: Split Guidance By Purpose

Then:

- split current `formats` into:
  - learning unit types
  - presentation surfaces
  - instructional patterns
- keep pedagogy, brand, and domain guidance separate

Goal:

- the runtime composition model becomes semantically clean

### Phase 6: Add Product And Packaging Overlays Carefully

Only after the base model is stable:

- add product overlays where runtime behavior truly differs
- add packaging overlays where unit mix, support, or end outputs differ
- add practice profiles and assessment modes later

Goal:

- product complexity comes in as overlays, not as pollution of base stack guidance

## Final Rule Of Thumb

If a file answers:

- “what should be selected?” -> `manifests`
- “what structured facts exist?” -> `catalogs`
- “what text evidence should runtime ingest?” -> `sources`
- “what exemplars should we study?” -> `corpus`
- “what did we learn from those exemplars?” -> `analyses`
- “what distilled playbooks should runtime load?” -> `guidance`
- “what did the system generate while running?” -> `storage`

That rule should make future layout decisions much easier.
