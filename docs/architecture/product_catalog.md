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

`Launchpad` is intentionally excluded from this architecture slice for now.

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

### GRIT

Known product family:

- `GRIT`

Current note:

- detailed versioning and delivery metadata are not yet captured here

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

## Important Modeling Rule

Products should **not** replace stack/domain curriculum design.

The intended layering is:

```text
stack/domain curriculum
  + packaging profile
  + product family / version overlay
  = delivered learning experience
```

So:

- `genai` remains a stack/domain
- `Academy 1.5` or `Intensive 3.0` should be treated as delivery overlays
- the same stack curriculum may be packaged differently by different products

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

## TODO

- add student capacity by product and version
- add stack availability by product and version
- add delivery intensity and pacing expectations
- add precise launch dates where needed
- add product-level assessment cadence overrides
- add product-level summary output requirements such as `summary_cheatsheet`
- add product-level live vs recorded vs offline distribution rules
- decide whether batch lineage and version lineage should share one schema or separate schemas
