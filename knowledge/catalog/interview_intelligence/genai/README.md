# GenAI Interview Intelligence Exports

This folder is the intended landing zone for GenAI-specific interview-intelligence
exports prepared outside Open ACP.

Recommended first-wave files:

- `role_opportunity_summary.csv`
- `skill_opportunity_summary.csv`
- `course_opportunity_summary.csv`
- `topic_relevance_summary.csv`
- `topic_sequencing_summary.csv`
- `question_type_distribution.csv`
- `question_depth_summary.csv`
- `package_band_summary.csv`
- `recency_retirement_summary.csv`

These should be aggregated canonical exports, not raw question logs.

The intended runtime aggregate is:

- `skill_outcomes_signal_digest`

That digest should combine the exported insight families above and then enrich:

- `role_profile`
- `skill_entities`
- `stack_skill_profiles`
- `competitor_entities`
- `product_summaries`

Suggested rule:

- if a field can be traced to one of the exports above, it belongs in the digest
- if it cannot be traced, it should not be invented inside the first-wave runtime digest
