# Product Catalog

## Purpose

This document records the current product-layer context that sits above stack/domain curriculum
design and above packaging defaults.

The key rule is:

- stack or domain curriculum should stay independent
- packaging shapes how that curriculum is delivered
- product and product-version overlays can further adjust packaging rules, delivery modes,
  assessment cadence, and end-of-course outputs

This document is a working reference for those product overlays.

## Current Implementation Status

The first product-aware implementation slice is now present in code.

Current canonical manifests live under:

- `knowledge/manifests/products/`
- `knowledge/manifests/structure_profiles/`

Current runtime behavior:

- Loop A resolves product context and structure profile from manifests
- explicit product runs write a derived product summary into the runtime wiki
- Loop B resolves product context and structure profile before packaging and pedagogy
- stack-only runs continue to work without an explicit product

Recommendation for real curriculum-design runs:

- explicit product context should become required for product-governed outputs
- the stack-only default should remain only for backward compatibility, tests, and generic architecture exploration

Other products should be documented in this file later using the same pattern as the NIAT section once detailed context is available.

## Status

This is a user-provided baseline snapshot captured on **April 16, 2026**.

Some dates and product notes are approximate and should be treated as internal working context,
not finalized source-of-truth launch metadata.

## Current Product Families

The current product families to model are:

- `Intensive`
- `Academy`
- `NIAT`
- `GRIT`

Other known standalone or future product families to note now:

- `Launchpad`
- `MINT`
- `Makers Conclave`
- `Partnership Workshops`
- `Govt Workshops`
- `Master Classes`
- `Youtube Series`
- `Content Branding Pipeline`
- `BITS Product`
- `Employee Workshops`

These are not all in the first implementation slice, but they should be accounted for in the architecture.

## Current Implementation Focus

The structure should support many versions and products, but the first implementation focus is not uniform.

Current focus priorities:

- `Academy 1.5`
- `Academy 2.0`
- `Intensive Offline`
- `NIAT B2`
- `NIAT B3`
- `NIAT B4`

Lower-priority or legacy support for now:

- `Academy 1.0`
- `Intensive 1.0`
- `Intensive 2.0`
- `Intensive 3.0`
- `NIAT B1`
- `Launchpad` as a later dedicated structure/product pass

Important note:

- `Launchpad` should likely not be treated as only a packaging variation
- because the target audience can require meaningfully different courses or course variants

## Product Variants

### NIAT

Current known variants:

- `B1`
- `B2`
- `B3`
- `B4`
- `B5`

Known timeline notes:

- `B1` = 2023 starting batch
- `B2` = 2024 starting batch
- later batches continue that yearly progression pattern

Delivery and packaging notes:

- NIAT is **offline-only**
- recorded videos are still included as part of the packaging

Operational focus note:

- early architecture focus should emphasize `B2`, `B3`, and `B4`
- `B1` should be supported, but not drive the design

### Academy

Current known variants:

- `1.0`
- `1.5`
- `2.0`

Known timeline notes:

- `Academy 1.0` started around **2020**
- `Academy 1.5` covers learners joining from **November 2025** onward up to the current period
- `Academy 2.0` is planned but **not launched yet** in this working snapshot

Delivery and packaging notes:

- Academy includes **live session delivery** as part of its value proposition

Operational focus note:

- architecture focus is on `1.5` and `2.0`
- `1.0` is legacy-supported, but not the primary design center

### Intensive

Current known variants:

- `1.0`
- `2.0`
- `3.0`
- `Offline`

Known timeline notes:

- `Intensive 1.0` launched in **2019**
- `Intensive 2.0` launched in **2021**
- `Intensive 3.0` launched in **2023**
- `Intensive Offline` is associated with **November 2025**

Delivery and packaging notes:

- Intensive exists in both **online** and **offline** forms
- recorded videos are still included as part of the packaging

Operational focus note:

- `Intensive Offline` is the primary current design focus
- the structure should still support other versions

### GRIT

Known product family:

- `GRIT`

Current note:

- detailed versioning and delivery metadata are not yet captured here

### Launchpad

Current note:

- Launchpad should remain in the architecture as a future product family
- it likely needs separate course variants for some subjects because the target audience is different

Examples already identified conceptually:

- `Operating Systems`
- `Computer Networks`

The same broad course name may not imply the same course variant across Launchpad and NIAT.

## Product Categories

The product families above should not all be treated as one kind of structure.

Working categories:

- `degree_program_product`
  - examples: `NIAT`, `BITS Product`
- `certification_or_upskilling_product`
  - examples: `Academy`, `Intensive`, `GRIT`, `MINT`
- `event_or_workshop_product`
  - examples: `Makers Conclave`, `Partnership Workshops`, `Govt Workshops`, `Master Classes`, `Employee Workshops`
- `media_or_brand_product`
  - examples: `Youtube Series`, `Content Branding Pipeline`

## Architecture Implications

These products should eventually become a product-layer overlay above packaging.

That means product configuration may later influence:

- which courses or modules are included
- number of modules per course
- number of topics per module
- allowed learning unit types
- whether recorded videos are bundled
- whether live delivery is expected
- course-end outputs such as `summary_cheatsheet`
- learning assessment cadence
- skill assessment cadence
- placement-eligibility linkage
- learner-persona overrides

## Important Modeling Rule

Products should **not** replace stack/domain curriculum design.

The intended layering is:

```text
stack/domain curriculum
  + structure profile
  + product family / version overlay
  + packaging profile
  = delivered learning experience
```

So:

- `genai` remains a stack/domain
- `Academy 1.5` or `Intensive 3.0` should be treated as delivery overlays
- the same stack curriculum may be packaged differently by different products

Later:

- some products may also require course variants, not just packaging variants

## Current Known Delivery Signals

Useful product-level distinctions already visible from the notes:

- `offline only`
- `online + offline`
- `recorded videos included`
- `live sessions included`
- batch-based lineage
- version-based lineage

These will matter later for:

- learning unit planning
- video session expectations
- assessment scheduling
- skill assessment alignment
- end-of-course summary outputs
- product-specific enablement flags such as AI tutor availability

## Future Product Flags

The product layer will likely need operational and experience-level flags in addition to
curriculum and packaging structure.

Examples already identified:

- `ai_tutor_enabled`
- whether AI tutor support is enabled for **all courses** or only selected courses
- whether AI tutor support is enabled only for specific modules or topics
- whether recorded videos are bundled for the product
- whether live sessions are bundled for the product
- whether offline delivery is required

These should eventually be treated as product or product-version overlay parameters rather
than stack or curriculum parameters.

## Learner Persona TODO

TODO:

- learner personas should later become product-aware
- some products may require audience-specific course variants
- NIAT may later need batch-aware, university-aware, and branch-aware persona overlays

## NIAT Product Notes

### Product Meaning

`NIAT` here refers to the university-collaboration product context.

### Target Audience

- post-12th students enrolled in partner universities

### Delivery Model

- full-time offline instruction shaped like traditional college delivery
- a learning portal is also provided with learning material for each course

### Learning Approach

NIAT should be treated as:

- industry-aligned
- project-based
- hands-on
- degree-linked
- placement-oriented

The current working roadmap described is:

- Year 1 and Year 2:
  - foundations
  - MERN stack projects
- Year 2:
  - DSA
  - competitive coding
- Year 3:
  - specialization selection
  - software engineering or AI/ML direction
- Year 4:
  - capstone projects
  - interview preparation

### Branch Complexity

NIAT branches currently noted include variants such as:

- B.Tech – Computer Science and Engineering (CSE)
- B.Tech – CSE (Full Stack Development)
- B.Tech – CSE (Artificial Intelligence & Machine Learning)
- B.Tech – CSE (Data Science)
- B.Tech – CSE (Generative AI)
- B.Tech – Artificial Intelligence & Agentic AI
- B.Tech – Artificial Intelligence & Data Engineering
- B.Tech – Computer Science & Quantum Engineering

Important architectural rule:

- branch names can differ by university
- not all universities have all branches
- different branches can require different curriculum-container structures

### Outcomes

Current target outcomes include:

- partner-university B.Tech or B.Sc. degree
- Industry-Ready Certificate (IRC)
- placement-readiness support

Skill assessments are aligned to the IRC and placement-readiness layer.

### University Partnership Growth Notes

Current working notes captured:

- 2024:
  - partnered with 2 universities
  - Batch 2
  - around 1000 students
  - BITS BSc Program
  - Chaitanya Deemed University BTech Program
  - delivery noted as hybrid for both
- 2025:
  - partnered with 17 universities
  - Batch 3
  - around 6500 students
- 2026:
  - partnering with 34+ more universities
  - Batch 4
  - ongoing

### NIAT Delivery Modes

These modes define who teaches BOS-approved curriculum courses at each university partner.

#### Co-Delivery

- NIAT teaches most courses
- university teaches a smaller portion
- example pattern:
  - NIAT covers around 141 of 161 credits
  - university covers around 20 credits

Current examples noted:

- `SGU`
- `CDU`
- `Annamacharya University` for Batch 3

#### Full Delivery

- NIAT teaches all courses in the approved curriculum

Current examples noted:

- `MRV University`
- `Aurora University`

#### Hybrid Delivery

- university runs its own curriculum
- NIAT runs a separate parallel curriculum
- common split:
  - university teaches about 1 to 1.5 days per week
  - NIAT teaches about 4 to 4.5 days per week

Current examples noted:

- `NSRIT`
- `Chalapathy University`

### Canonical Intake Location For NIAT Batch Sources

When BOS-approved curriculum structures and grid-template references are provided as CSVs,
they should be stored as canonical inputs under a batch-specific catalog location.

Recommended path pattern:

```text
knowledge/catalog/niat/batches/<batch_id>/
  bos_curriculum_references.csv
  grid_template_references.csv
  README.md
```

Example for Batch 3:

```text
knowledge/catalog/niat/batches/b3/
  bos_curriculum_references.csv
  grid_template_references.csv
```

These CSVs should be treated as canonical source inputs, not runtime wiki state.

The runtime wiki may later hold synthesized NIAT batch, university, or branch summaries derived from them.

## Structure Implication For NIAT

NIAT should be treated as requiring a richer curriculum-container hierarchy such as:

```text
product family
  -> batch
    -> university
      -> branch
        -> curriculum grid template
          -> BOS curriculum reference
            -> implementation curriculum
```

This is one of the strongest reasons the architecture should support different structure profiles.

## TODO

- add student capacity by product and version
- add stack availability by product and version
- add delivery intensity and pacing expectations
- add precise launch dates where needed
- add product-level assessment cadence overrides
- add product-level summary output requirements such as `summary_cheatsheet`
- add product-level live vs recorded vs offline distribution rules
- add product-level enablement flags such as AI tutor availability and course coverage scope
- decide whether batch lineage and version lineage should share one schema or separate schemas
- add structured university, branch, city, student-count, and BOS-reference records for NIAT batches
- add standalone-product structure profiles for event, workshop, and media products
- add the rest of the product families in the same documentation style as NIAT once their context is available
