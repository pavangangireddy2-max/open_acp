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

## Important Terminology Rule

Stacks or domains such as `genai`, `python`, `cpp`, `dsa`, or `reactjs` are not
the same thing as products or programs.

For now:

- the stack or domain defines the curriculum spine
- packaging defines how that spine is delivered
- products can later override packaging, hours, unit mix, and assessment cadence

This keeps the curriculum model clean without introducing full product complexity too early.

## Current Loop B Design

The current Loop B flow is:

1. `load_wiki_context`
2. `resolve_pedagogy_profile`
3. `generate_curriculum`
4. `compare_curriculum_changes`
5. `resolve_packaging_profile`
6. `design_courses`
7. `design_modules`
8. `design_topics`
9. `design_learning_units`
10. `design_practice`
11. `design_learning_assessments`
12. `resolve_skill_assessment_requirements`
13. `align_learning_with_skill_assessments`

`generate_differentiation` is intentionally removed from the core learning-design path.

## Compatibility Note

The current `generate_curriculum` stage still writes a `curriculum_map.modules` array.
That is a compatibility shape inherited from the earlier repo model.

Architecturally, those current "modules" are now treated as **course seeds** by the downstream stages.

So today:

- `curriculum_map.modules` = course-level structural seeds
- `design_courses` = converts those seeds into explicit course design
- `design_modules`, `design_topics`, and `design_learning_units` = expand the structure further

Later, the compatibility layer can be removed and the upstream artifact can become course-native.

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

See also:

- [Product Catalog](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/product_catalog.md)

TODO:

- introduce an explicit product layer above packaging
- let product configuration decide whether `summary_cheatsheet` appears as a course-end deliverable
- let product configuration override module counts, unit mix, assessment cadence, and skill-assessment cadence
- let product configuration decide when course-end units such as cheat sheets, revision packs, or recap assets are required

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
- assignments
- guided practice checks

### 2. Skill Assessments

These belong to an external team or repo and support product or placement eligibility.

Examples:

- placement-readiness checks
- external coding rounds
- product-specific assessment contracts

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

Until that migration happens, Loop C still works through the compatibility layer.

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
