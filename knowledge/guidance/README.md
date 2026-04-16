# Runtime Guidance Playbooks

This folder holds non-code YAML playbooks that runtime execution composes into prompts and review context.

These files are different from:

- `knowledge/sources/`
  - seeded text evidence ingested by Loop A and Loop B
- `knowledge/corpus/`
  - exemplar PPT/PDF assets used for one-time extraction and interpretation
- `knowledge/analyses/`
  - interpreted notes derived from exemplars
- `skills/...` and later `loops/.../prompts/`
  - prompt files, not playbooks

Current categories:

- `brand/`
  - brand and voice playbooks
- `pedagogy/`
  - runtime core, resolution rules, and pedagogy profiles
- `learning_unit_types/`
  - playbooks for the primary artifact being produced
- `presentation_surfaces/`
  - playbooks for the surface or medium through which the unit is experienced
- `instructional_patterns/`
  - playbooks for session or teaching patterns such as concept explainer or project building
- `domains/`
  - stack/domain-specific teaching guidance

Architecture note:

- pedagogy profiles define the allowed teaching modes
- instructional-pattern playbooks define the preferred teaching-mode sequence
- the loader resolves both into a teaching-mode contract at runtime
- presentation surfaces are intentionally separate from instructional patterns
- learning unit types remain separate from both, because one pattern can appear on different surfaces
