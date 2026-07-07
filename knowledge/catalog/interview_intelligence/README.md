# Interview Intelligence Catalog

This folder is the intended landing zone for canonical interview-intelligence
exports or normalized snapshots prepared outside Open ACP.

Important scope note:

- these exports represent the **interview-intelligence portion** of
  **Dimension 1: Job / Placement Outcomes**
- interview intelligence is a shared channel across stacks
- this folder should stay shared at the channel level
- stack-specificity should be carried by fields such as `stack`, `role_cluster`,
  `course_id`, or `topic_id` inside the exports rather than by per-stack
  subfolders
- they do not replace other planned Dimension 1 canonical inputs such as
  placement-readiness summaries, skill-assessment performance summaries, or
  corporate skill-assessment summaries

Recommended direction:

- keep heavy raw analysis, tagging workflows, and dashboards outside Open ACP
- export canonical aggregated snapshots or normalized entries into this folder
- let Open ACP ingest those snapshots into runtime digests and knowledge updates

Expected first-wave snapshot families:

- `role_opportunity_summary`
- `skill_opportunity_summary`
- `course_opportunity_summary`
- `topic_relevance_summary`
- `topic_sequencing_summary`
- `question_type_distribution`
- `question_depth_summary`
- `package_band_summary`
- `recency_retirement_summary`

At monthly scales of thousands of questions, aggregated exports are preferred
over direct raw-event ingestion for the first implementation wave.

Open ACP should treat this folder as the canonical landing zone for interview-intelligence
exports, not as the place where the upstream SOP, tagging workflow, or raw analytics
pipeline is executed.

## Digest Mapping

The intended runtime aggregate is:

- `skill_outcomes_signal_digest`

That digest should summarize and combine the insight families above rather than
introducing unrelated fields.

Expected mapping:

- `target_roles` <- `role_opportunity_summary`
- `skill_priority_clusters` <- `skill_opportunity_summary`
- `packaging_implications` <- `package_band_summary` and `course_opportunity_summary`
- `sequencing_implications` <- `topic_sequencing_summary` and `topic_relevance_summary`
- `question_type_patterns` <- `question_type_distribution`
- `difficulty_patterns` <- `question_depth_summary`
- `retire_or_refresh_signals` <- `recency_retirement_summary`

The canonical skill taxonomy and vocabularies stay alongside this channel as
reference inputs, but the runtime digest should still be driven by the exported
insight families above.

So the relationship is:

- `Dimension 1` = broader job / placement outcomes layer
- `interview_intelligence` = one channel feeding that dimension
- `skill_outcomes_signal_digest` = runtime aggregate that combines this channel
  with other Dimension 1 source families as they are added
