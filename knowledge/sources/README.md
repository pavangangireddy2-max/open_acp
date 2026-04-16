# Knowledge Sources

This folder holds canonical seeded text inputs for Loop A and Loop B.

These files are different from:

- `knowledge/manifests/`
  - selectors and configuration
- `knowledge/catalogs/`
  - structured reference data such as CSVs
- `knowledge/corpus/`
  - exemplar assets such as PPT/PDF references
- `knowledge/analyses/`
  - interpreted notes derived from exemplars
- `storage/wiki/`
  - generated runtime knowledge

Current layout:

- `shared/`
  - learner, hiring, competitor, and market inputs used across stacks unless overridden
- `domains/`
  - stack- or domain-specific reference inputs such as curriculum seeds
- `products/`
  - reserved for future product-specific text inputs

Rule:

- canonical seeded text inputs belong under `knowledge/sources/`
- they should not be placed under `src/`
