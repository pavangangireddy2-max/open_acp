# Curriculum Design

## Purpose

This document defines how Open ACP should think about curriculum design in Loop B.

The key idea is that curriculum design is not the same thing as content generation.
Loop B should shape the learning architecture first, and Loop C should only generate
content after that architecture is explicit and reviewable.

## Canonical Learning Hierarchy

The current target hierarchy is:

1. Curriculum
2. Courses
3. Modules
4. Topics
5. Learning Units

Definitions:

- **Curriculum**
  - the full stack or domain learning blueprint
- **Course**
  - a deliverable slice of the curriculum
- **Module**
  - a grouped instructional block inside a course
- **Topic**
  - a coherent teaching chunk inside a module
- **Learning Unit**
  - the actual deliverable artifact, such as:
    - PPT or video unit
    - reading material unit
    - MCQ practice unit
    - coding practice unit

## Guidance Connection

At runtime, Loop C should not treat all "content types" as one flat axis.

The current guidance model now separates:

- **pedagogy profile**
  - defines the allowed teaching modes
- **instructional pattern**
  - defines the preferred teaching-mode sequence
- **learning unit type**
  - defines what kind of unit is being produced
- **presentation surface**
  - defines the medium through which the learner experiences the unit
- **domain guidance**
  - shapes examples, diagrams, and emphasis

So the connection is:

```text
pedagogy profile -> allowed teaching modes
instructional pattern -> preferred teaching-mode sequence
learning unit type + presentation surface -> delivery constraints
domain guidance -> contextual emphasis
```

This is intentionally clearer than the older single `format` bucket.

### Learning Support Note

`learning_support` should not be treated as a normal slide-backed teaching
session by default.

Current intended meaning:

- on-demand support delivery
- revision-oriented or doubt-resolution oriented
- often triggered by learner need rather than fixed curriculum sequence
- may not require PPTs or a slide-backed presentation surface

This remains a pending taxonomy cleanup item. The current runtime name stays
`learning_support` for compatibility, but future guidance and pipeline design
should treat it more like a support or intervention pattern than a standard
session pattern.

### Pedagogy Resolution Rule

Pedagogy should not be treated as stack-only in real product runs.

The intended rule is:

- packaging is **product-first**
- pedagogy is **product-aware and stack-grounded**

So the effective pedagogy profile should resolve from canonical manifests in this order:

- product default pedagogy
- product + domain pedagogy
- product + version pedagogy
- product + version + domain pedagogy
- stack/domain pedagogy baseline

This keeps product-specific academic or delivery realities visible without losing the stack's
baseline instructional logic.

## Important Terminology Rule

Stacks or domains such as `genai`, `python`, `cpp`, `dsa`, or `reactjs` are not
the same thing as products or programs.

For now:

- the stack or domain defines the curriculum spine
- packaging defines how that spine is delivered
- products can later override packaging, hours, unit mix, and assessment cadence

This keeps the curriculum model clean without introducing full product complexity too early.

## Core Terminology

### Packaging Profile

`packaging_profile` means the delivery-constraint layer that shapes how a curriculum container
is delivered.

It can decide things such as:

- hours
- module counts
- topic counts
- learning-unit mix
- assessment cadence
- feature flags
- course-end outputs such as `summary_cheatsheet`

Important rule:

- `packaging_profile` does **not** define the academic spine by itself
- it sits below the base curriculum and structure profile
- it sits below product overlays
- it helps shape the final implementation curriculum

So the intended layering is:

```text
base curriculum
  + structure profile
  + product overlay
  + packaging profile
  = implementation curriculum
```

Implementation note:

- the first product-aware runtime slice now resolves `product_context` and `structure_profile`
  before packaging and pedagogy
- if no product is selected, the system falls back to a stack-only default context rather than blocking
- stricter run modes are now available so real product runs can require explicit product context and manifest-backed domain inputs

Recommended next policy:

- product-governed curriculum runs should eventually fail fast when no explicit product context is supplied
- the stack-only default should remain only for tests, legacy compatibility, and generic exploration
- academic products such as NIAT should not rely on the stack-only default for real curriculum design

## Current Loop B Design

The current Loop B flow is:

1. `load_wiki_context`
2. `resolve_product_context`
3. `resolve_structure_profile`
4. `resolve_packaging_profile`
5. `resolve_design_priority_profile`
6. `resolve_time_budget_context`
7. `resolve_pedagogy_profile`
8. `generate_brief`
9. `generate_curriculum`
10. `compare_curriculum_changes`
11. `design_courses`
12. `design_modules`
13. `design_topics`
14. `design_learning_units`
15. `design_practice`
16. `design_learning_assessments`
17. `resolve_skill_assessment_requirements`
18. `align_learning_with_skill_assessments`

`generate_differentiation` is intentionally removed from the core learning-design path.

## Course-Native Output

`generate_curriculum` writes a native `curriculum_map.courses` array.

That current meaning is:

- `curriculum_map.courses` = packaged course seeds
- `design_courses` = normalizes those seeds into explicit course design
- `design_modules`, `design_topics`, and `design_learning_units` = expand the structure further

Clarification:

- `generate_curriculum` should not emit a separate `levels` structure just because a source document uses levels or phases
- source-defined levels, phases, or tracks should mainly shape:
  - course ordering
  - course titles
  - packaged course scope
- explicit course selection should be driven by:
  - time-budget constraints
  - priority skill requirements
  - product-linked skill-assessment expectations
- topic allocation belongs to later design stages, not to `generate_curriculum`

## Brief-First Transition

Loop B is moving toward a stricter artifact chain:

1. resolve context
2. generate a compact `brief`
3. generate curriculum structure from that brief
4. expand into course, module, topic, and learning-unit design

This keeps the responsibilities cleaner:

- `generate_brief`
  - picks stack identity, audience focus, default pedagogy, stack learning outcomes, and the downstream product context minimum
- `generate_curriculum`
  - turns the brief plus source curriculum into a structural course-seed map using packaging-owned time constraints
- downstream design stages
  - expand that structure without re-deciding the Brief

This is intentionally closer to the longer-term stage discipline rule:

- each stage owns a fixed decision set
- later stages read upstream artifacts, not the full raw-source pile

## Runtime Design Artifacts

Loop B is now moving toward persisted design artifacts under:

```text
storage/design/<domain>/<cycle_id>/
  brief.yaml
  curriculum.yaml
  courses/
    index.yaml
    course.<id>.yaml
  modules/
    index.yaml
    module.<id>.yaml
  topics/
    index.yaml
    topic.<id>.yaml
  units/
    index.yaml
    unit.<id>.yaml
```

Near-term rule:

- `generate_brief` persists `brief.yaml`
- `generate_curriculum` persists `curriculum.yaml`
- `design_courses`, `design_modules`, `design_topics`, and `design_learning_units` now persist stage collections and per-item docs

Stage 1 validation rule:

- `total_hours` is the full Stage 1 budget for packaged courses plus any
  `capstone_project` and `grand_quiz`
- a parsed curriculum gets one structured repair pass if the first draft fails
  strict hours accounting
- if the repaired artifact still fails the validator, the stage must fail rather
  than silently persisting an invalid curriculum
- downstream stages should increasingly read those artifacts rather than relying only on in-memory state

Current Brief contract:

- `stack_name`
- `packaging_profile_ref`
- minimal `product_context`
- `audience`
- `pedagogy`
- `stack_learning_outcomes`
- `source_refs`
- `source_hours_declared`
- `source_vs_packaging_conflict`

Current Curriculum contract:

- `stack_name`
- `packaging_profile_ref`
- `courses`
- `capstone_project`
- `grand_quiz`
- `total_hours`
- `hours_check`

This is different from canonical source truth:

- manifests, catalogs, sources, and guidance remain the canonical input layer
- `storage/design` is the accepted runtime design layer for a specific cycle

The intended direction is:

```text
canonical inputs -> Loop B stage artifacts -> Loop C generation
```

not:

```text
canonical inputs -> ad hoc state dicts -> Loop C generation
```

## First Strict Validator

The first strict validator in this design chain is the curriculum-hours check.

At `generate_curriculum` time, the system should verify:

- sum of packaged course hours
- curriculum total hours
- brief total hours

If those totals disagree beyond the configured tolerance, the curriculum stage should fail
rather than silently carrying an inconsistent structure downstream.

TODO:

- make topic-to-course assignment explicitly consume channel-analysis inputs rather than relying only on source-curriculum prose
- when canonical packaging carries breadth/depth scope such as `C1/C2/C3` and `L1/L2/L3`, let packaged course scope or course title reflect that directly

## Packaging Layer

Packaging is now a first-class design input, but not yet a full product model.

The packaging layer controls things such as:

- number of modules per course
- number of topics per module
- allowed learning unit types
- preferred learning unit mix
- classroom quiz cadence
- module quiz requirement
- skill assessment cadence
- expected question types and difficulty bands

This is represented through a `packaging_profile`.

Source-of-truth note:

- product definitions live under `knowledge/manifests/products/`
- structure definitions live under `knowledge/manifests/structure_profiles/`
- packaging manifests remain under `knowledge/manifests/packaging/`
- Loop A may write a derived product summary into the runtime wiki, but the manifests remain canonical

Packaging resolution note:

- packaging should resolve from canonical manifests only
- product-aware packaging should be resolved before stack fallback values are accepted
- the intended precedence is:
  - global default packaging
  - stack fallback packaging
  - product default packaging
  - product + domain packaging
  - product + version packaging
  - product + version + domain packaging
  - later course-level packaging overrides
- stack manifests should fill gaps, not silently override explicit product packaging choices
- the resolved packaging profile should carry per-field provenance so review packets can explain where module counts, topic counts, and learning-unit constraints came from

Pedagogy resolution note:

- pedagogy should also resolve from canonical manifests only
- explicit product pedagogy should be allowed to override the stack baseline
- stack/domain pedagogy should remain the baseline when product manifests do not define a pedagogy choice
- the resolved pedagogy profile should carry source metadata so review packets can explain whether the decision came from product, stack, or global fallback

Strict-source note:

- if a requested domain has no explicit manifest-backed or domain-backed source inputs, the system should eventually stop rather than silently borrowing unrelated defaults
- cross-domain fallback such as using unrelated `ml_engineering` material should be avoided for real runs

See also:

- [Product Catalog](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/product_catalog.md)
- [Design Priorities](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/design_priorities.md)

TODO:

- introduce an explicit product layer above packaging
- let product configuration decide whether `summary_cheatsheet` appears as a course-end deliverable
- let product configuration override module counts, unit mix, assessment cadence, and skill-assessment cadence
- let product configuration decide when course-end units such as cheat sheets, revision packs, or recap assets are required
- let product configuration carry enablement flags such as `ai_tutor_enabled` and whether that support applies to all courses or selected courses only
- later add product-specific content-development constraints that Loop C must honor during execution

Examples of packaging-sensitive behavior:

- one course may have 2 modules in a light packaging and 4 modules in a deeper packaging
- one topic may use only video + MCQ in one packaging and video + reading + coding in another
- one stack may expect classroom checks every 15 minutes while another uses 20-minute cadence

## Assessments: Internal vs External

Open ACP should treat assessments as two different systems.

### 1. Learning Assessments

These belong inside this repo and support learning progression.

Examples:

- classroom quizzes
- module quizzes
- final course quizzes
- assignments
- guided practice checks

### 2. Skill Assessments

These belong to an external team or repo and support product or placement eligibility.

Examples:

- periodic skill assessments
- summative skill assessments
- placement-readiness checks
- external coding rounds
- product-specific assessment contracts

Canonical runtime assessment names should use:

- `skill_assessment`
- `graded_assessment`

`skill_assessment` is the fresh runtime replacement for older names such as
`fortnight_quiz`.

`graded_assessment` remains a separate academic-assessment content type for
product contexts like NIAT, where mid-semester and end-semester exams are
distinct from placement-linked skill assessments.

Legacy user inputs such as `fortnight_quiz` may still be normalized for
compatibility, but they should not be treated as the canonical taxonomy
moving forward.

The important rule is:

- this repo designs learning
- this repo aligns to skill assessments
- this repo does not own the external assessment bank itself

## Assessment Alignment Dimensions

The `align_learning_with_skill_assessments` stage should check at least:

- question type alignment
  - MCQ
  - coding
  - FIB
  - project
  - short answer
- difficulty alignment
- concept coverage alignment
- pattern alignment
  - whether both sides reflect the same Loop A market or industry signals
- cadence alignment
  - for example, external skill assessments every 8 topics

## Curriculum Change Visibility

Loop B should expose structural changes clearly after curriculum generation.

The `compare_curriculum_changes` stage exists for this reason.

It should surface:

- added courses
- removed courses
- renamed courses
- total-hours changes
- later: module-count and topic-count changes as the course/module/topic model matures

This is important because curriculum design needs to be reviewable, not silently regenerated.

## Loop A Product Context

Loop A now has a product-context synthesis stage before wiki index rebuild.

The intended behavior is:

- manifests remain the source of truth for product and structure definitions
- Loop A resolves those manifests for the current run
- Loop A writes a derived runtime summary for explicit products into the wiki
- Loop B then reuses that product context while remaining deterministic

This keeps product knowledge visible in runtime memory without turning the wiki into the canonical product catalog.

## Practice Design

Practice design is intentionally separated from basic content structure.

Examples of practice shapes:

- guided reflection
- MCQ retrieval checks
- coding practice
- architecture reasoning exercises
- debugging practice

This matters because not every topic should practice in the same way, even inside the same stack.

## Future Extension: Practice Profiles And Assessment Modes

This is not fully implemented yet, but it should become a first-class extension.

TODO:

- introduce `practice_profile` as an explicit contract
- introduce `assessment_mode` as an explicit contract

Two useful next concepts are:

- `practice_profile`
  - how a topic should be practiced
  - examples:
    - `retrieval_practice`
    - `guided_build_practice`
    - `debugging_practice`
    - `reflection_practice`
- `assessment_mode`
  - how learning or readiness is being tested
  - examples:
    - `classroom_quiz`
    - `module_quiz`
    - `assignment_review`
    - `placement_readiness_check`
    - `project_evidence`

This is especially useful because practice and assessment behavior can vary by:

- stack
- packaging
- future product constraints
- external skill-assessment contracts

TODO:

- target-audience profiles should be product-aware as canonical source inputs
- for academic products such as NIAT, target-audience profiles may also become batch-aware, university-aware, or branch-aware

## Loop C Impact

Loop C is not broken by this design, but it is now underfed if it only consumes the old module-level contract.

The long-term direction is:

- Loop C should receive richer inputs from Loop B
- Loop C should enter at **module scope**
- each module handoff should carry a nested `module_work_plan`
- the work plan should make the following explicit:
  - selected course
  - selected module
  - whether the module is being created or updated
  - planned topics
  - planned learning units
  - practice intent
  - learning assessment context
- skill assessment alignment context

Current implementation note:

- Loop C now prefers a module-first execution target when Loop B exposes:
  - course design
  - module design
  - topic design
  - learning-unit planning
- the selected module is passed forward together with a nested `module_work_plan`
- the work plan contains nested learning-unit and assessment production targets
- it still falls back to the older module-level contract when those richer artifacts are absent

TODO:

- distinguish clearly between `module_creation` and `module_update` in Loop C review and execution flows
- support video sessions that do not require a PPT-backed format
- add product-specific content-development constraints to the Loop C work plan as product overlays mature

So the migration is underway, but not yet complete.

## Loop D Impact

Loop D fix routing also needs to evolve as Loop B becomes more explicit.

Older routing assumed coarse Loop B targets such as curriculum generation or pedagogy selection.
Now, Loop D can eventually route more precisely to:

- `design_modules`
- `design_topics`
- `design_learning_units`
- `design_practice`
- `design_learning_assessments`
- `align_learning_with_skill_assessments`

That routing precision is not complete yet, but the architecture should treat it as the target shape.
