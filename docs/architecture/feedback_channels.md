# Feedback Channels

## Purpose

This document defines how feedback channels should connect to Open ACP without
forcing the system to own every upstream analytics or tagging workflow.

The key rule is:

- Open ACP should consume **canonical channel exports or normalized snapshots**
- Open ACP should not try to replace the full operational analytics system for every channel

That boundary matters because some channels can produce thousands of records per month.

This should be read as a reusable architecture pattern.

Interview intelligence is only the first formalized example.
Other channels can follow the same structure even when they have different SOPs,
different data volume, or different downstream curriculum implications.

## Channel Contract Model

Every channel should eventually have a canonical contract under:

- `knowledge/manifests/channels/`

Each contract should define:

- channel meaning
- owning design dimensions
- canonical source families
- canonical vocabularies
- runtime digests to derive
- runtime knowledge targets to update
- Loop B influence points
- Loop D backprop targets

For high-scale channels, the contract should also make clear whether Open ACP expects:

- aggregated exports
- normalized snapshots
- or direct raw-event ingestion

## External vs Internal Responsibility

### Keep Outside Open ACP

- raw event collection
- human tagging workflows
- dashboards and BI
- historical re-tagging or backfills
- source-system operational SOP execution

### Keep Inside Open ACP

- channel contracts
- canonical export expectations
- normalized ingestion schemas
- runtime digests
- knowledge-model updates
- curriculum-design and backprop routing decisions

## Interview Intelligence as the First Worked Example

Interview intelligence is the first recommended channel to formalize because it
feeds Dimension 1: Job / Placement Outcomes directly.

For this channel:

- the operational SOP can remain outside Open ACP
- canonical aggregated exports or normalized snapshots should be ingested
- Open ACP should derive:
  - `skill_outcomes_signal_digest`
  - `assessment_pattern_digest`
  - `role_profile` runtime entities
- those outputs should enrich:
  - skill entities
  - stack skill profiles
  - market and community digests
  - product summaries

The canonical contract for this channel lives at:

- `knowledge/manifests/channels/interview_intelligence.yaml`

The canonical catalog landing zone for first-wave exports lives at:

- `knowledge/catalog/interview_intelligence/`

The first-wave source families should be inspired directly by the analytics
cuts produced in the external SOP, for example:

- `role_opportunity_summary`
- `skill_opportunity_summary`
- `course_opportunity_summary`
- `topic_relevance_summary`
- `topic_sequencing_summary`
- `question_type_distribution`
- `question_depth_summary`
- `package_band_summary`
- `recency_retirement_summary`

The runtime aggregate should then be:

- `skill_outcomes_signal_digest`

That digest should summarize the exported insight families above rather than
introducing unrelated invented fields.

## How To Think About Other Channels

Every additional channel should answer the same questions:

1. What is the canonical source family prepared outside runtime?
2. What normalized runtime digest should Open ACP derive?
3. Which runtime entities or overlays should be updated?
4. Which Loop B stages should this influence?
5. Which Loop D backprop targets should consume it?

So the reusable pattern is:

```text
channel SOP and analytics system
  -> canonical export contract
  -> Open ACP channel contract
  -> runtime digest
  -> knowledge updates
  -> Loop B / Loop D decisions
```

## Why Aggregated Exports First

When monthly volume is in the thousands of questions:

- raw-event ingestion adds too much noise to the first architecture wave
- aggregated canonical exports are easier to review and route
- Open ACP can still remain channel-aware without becoming the analytics platform

So the preferred first-wave pattern is:

```text
external channel ops
  -> canonical export / normalized snapshot
  -> Open ACP ingest
  -> runtime digests
  -> knowledge-model updates
  -> Loop B decisions / Loop D backprop
```

## Relationship to Design Priorities

Each feedback channel should map to one or more dimensions in:

- [Design Priorities](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/design_priorities.md)

Examples:

- Interview Intelligence -> Dimension 1
- Classroom Feedback / Queries -> Dimension 2
- AICTE / BOS Inputs -> Dimensions 3, 4, 5
- Competitor / Market Feeds -> Dimension 9

## Relationship to Runtime Flow

Loop A should gradually move toward:

1. ingest canonical channel inputs
2. detect patterns
3. derive dimension digests
4. update runtime knowledge

See also:

- [Runtime Flow](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/runtime_flow.md)
- [Knowledge Model](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/knowledge_model.md)
- [Design Priorities](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/design_priorities.md)
