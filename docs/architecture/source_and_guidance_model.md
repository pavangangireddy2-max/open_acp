# Source And Guidance Model

## Purpose

This document defines the cleaned-up, purpose-based model for:

- canonical source inputs
- structured reference catalogs
- exemplar corpora
- derived analyses
- runtime guidance playbooks
- generated runtime knowledge

It exists because the current repo layout mixes:

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

3. `src/open_acp/styles/...`
   - runtime brand, pedagogy, and domain guidance YAMLs plus loader code

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

- target learner persona
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

This is the future home for what is currently under `src/open_acp/styles/`.

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

- `src/open_acp/styles/default.yaml`

#### `knowledge/guidance/pedagogy/`

This should contain:

- `runtime_core.yaml`
  - distilled always-on runtime pedagogy constraints
- `resolution_rules.yaml`
  - the deterministic profile-resolution matrix
- `profiles/`
  - `concept_progression`
  - `project_build_along`
  - `worked_example_scaffold`
  - and so on

Current likely sources:

- `src/open_acp/styles/pedagogy/core.yaml`
- `src/open_acp/styles/pedagogy/profile_matrix.yaml`
- `src/open_acp/styles/pedagogy/profiles/...`

Important rule:

- rich analytical files like `principles.yaml` should not be treated as runtime guidance automatically
- they belong closer to `knowledge/analyses/pedagogy/` unless a distilled runtime subset is intentionally created

#### `knowledge/guidance/domains/`

This should hold domain or stack playbooks.

Examples:

- `genai.yaml`
- `cpp.yaml`
- `dsa.yaml`
- `reactjs.yaml`

Current likely source:

- `src/open_acp/styles/stacks/...`

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

This is more accurate than calling everything “format.”

#### `knowledge/guidance/presentation_surfaces/`

This should hold presentation-medium playbooks.

Examples:

- `slide_backed_session.yaml`
- `screen_demo_session.yaml`
- `portal_reading_surface.yaml`

This is where a current `ppt_session` concept belongs.

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
- `knowledge/sources/shared/learner/...`
  - future: `knowledge/sources/shared/learner/...`

### Corpus And Analyses

- `knowledge/raw/brand/*.pdf`
  - future: `knowledge/corpus/style_exemplars/...`
- `knowledge/raw/brand/extracted_text/*.txt`
  - future: `knowledge/corpus/extracted_text/...`
- `knowledge/analyses/style/...`
  - canonical home for interpreted style notes

### Runtime Guidance

- `src/open_acp/styles/default.yaml`
  - future: `knowledge/guidance/brand/forgeai_default.yaml`
- `src/open_acp/styles/pedagogy/core.yaml`
  - future: `knowledge/guidance/pedagogy/runtime_core.yaml`
- `src/open_acp/styles/pedagogy/profile_matrix.yaml`
  - future: `knowledge/guidance/pedagogy/resolution_rules.yaml`
- `src/open_acp/styles/pedagogy/profiles/...`
  - future: `knowledge/guidance/pedagogy/profiles/...`
- `src/open_acp/styles/stacks/...`
  - future: `knowledge/guidance/domains/...`
- `src/open_acp/styles/formats/ppt_session.yaml`
  - future: `knowledge/guidance/presentation_surfaces/slide_backed_session.yaml`
- `src/open_acp/styles/formats/project_session.yaml`
  - likely future: `knowledge/guidance/instructional_patterns/project_building_session.yaml`

## What Is Not Needed Yet

The following changes are **not** required in the first migration slice:

1. renaming the Python code package from `styles` to `guidance`
   - the loader code can keep working while the data moves first
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

Then:

- create `knowledge/guidance/...`
- copy current runtime YAMLs there
- update the loader to read `knowledge/guidance` first
- keep temporary compatibility with `src/open_acp/styles` during migration

Goal:

- `src/` holds code
- `knowledge/` holds runtime playbooks

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
