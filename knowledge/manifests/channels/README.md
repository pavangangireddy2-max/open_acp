# Feedback Channel Contracts

This folder stores canonical contracts for feedback channels that influence
Loop A intelligence synthesis and Loop B curriculum design.

A channel contract is **not** the raw data pipeline.

It defines:

- what the channel means
- which design dimensions it influences
- what canonical source families should be prepared outside runtime
- what runtime digests Open ACP should derive
- which runtime entities or overlays should be updated
- which Loop B stages and Loop D backprop targets should consume the result

Important boundary:

- raw collection, human tagging workflows, heavy analytics, and reporting can remain outside Open ACP
- Open ACP should prefer canonical exports or normalized snapshots from those systems
- runtime wiki knowledge should store synthesized operating knowledge, not replace the source analytics system

## Why Contracts Exist

Different feedback channels can each have:

- their own SOP
- their own data volume and analytics depth
- their own canonical taxonomies
- their own downstream curriculum implications

The contract layer keeps Open ACP reusable across those channels without forcing
the repo to absorb every upstream analytics workflow.

## Adding A New Channel

For each new channel, add a manifest named:

- `knowledge/manifests/channels/<channel_id>.yaml`

The contract should define:

- `channel_id`
- `label`
- `channel_category`
- `unit_of_data`
- `owning_dimensions`
- `preferred_ingest_mode`
- `canonical_source_families`
- `canonical_vocabularies`
- `runtime_digests`
- `knowledge_targets`
- `loop_b_influence`
- `backprop_targets`

## Scale Guidance

When channel volume is large, prefer:

- canonical aggregated exports
- normalized snapshots

Avoid first-wave direct ingestion of raw event streams unless the channel is
small enough and already normalized.
