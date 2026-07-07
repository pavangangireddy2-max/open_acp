# Design Priorities

## Purpose

This document records the base curriculum-design priority framework for Open ACP.

These priorities shape the **base curriculum** before product overlays, packaging overlays,
and implementation-specific constraints are applied.

Important rule:

- not every priority dimension applies equally to every curriculum container
- different structure profiles may activate or weight different subsets of these dimensions
- product overlays may later sharpen or override how these priorities are applied

So this is a base framework, not a rigid one-size-fits-all rulebook.

## Eleven Design Dimensions

### 1. Job / Placement Outcomes

Also referred to as skill outcomes.

This dimension reverse-engineers the minimum skill set the curriculum must produce from hiring
signals, interview patterns, and placement expectations.

Covers:

- target roles and role-skill expectations
- shared hiring summaries and role-demand signals
- interview intelligence
- skill assessment performance
- interview assessment performance

### 2. Student Learning Outcomes

This dimension captures how students actually learn, struggle, retain, and disengage.

It influences:

- pacing
- practice design
- instructional format
- reinforcement frequency
- support interventions

Covers:

- queries team
- course mentors
- success coaches
- instructors
- in-app platform feedback and surveys
- video, reading, MCQ, and coding-practice feedback
- classroom assessment performance
- module assessment performance
- engagement and retention analytics

### 3. Degree and Higher Ed Outcomes

This dimension captures academic grade performance and readiness for higher studies.

It influences:

- revision blocks
- exam-prep slots
- foundational academic subjects
- GATE and MS readiness

Covers:

- academic assessment performance
- GATE readiness benchmarks
- MS readiness benchmarks

### 4. Regulatory Compliance

This is the hard-constraint layer for academic structure.

It fixes:

- credits
- hours
- subject mix
- mandatory academic constraints

Covers:

- AICTE mandates
- UGC mandates
- NEP 2020 constraints
- other formal compliance requirements

### 5. University Policy and Infrastructure Constraints

This is the slot-budget layer.

It determines the real delivery envelope before curriculum design begins.

It can include:

- college timings
- bus schedules
- Wi-Fi bandwidth
- lab availability
- holiday calendars
- full / co / hybrid delivery constraints

Covers:

- university policy
- infrastructure data
- academic calendars

### 6. Operational Efficiency

This dimension ensures the final subject or course placement is operationally feasible.

It optimizes:

- instructor utilization
- staff utilization
- semester-wise load balance
- delivery feasibility within the slot budget created by Dimension 5

Covers:

- program ops inputs
- program managers
- faculty deployment data
- staff utilization data

### 7. Cross-Product Alignment

This dimension prevents major divergence across products when alignment is strategically useful.

Covers:

- employee workshops
- corporate trainings
- placed-user feedback
- student bootcamps

### 8. Industry Partnerships and Certifications

This dimension covers external workshops, certifications, and partner-led interventions that
add credibility and current-tool exposure.

Covers:

- partner company inputs
- certification tracks

### 9. Market and Community Signals

This dimension captures what is becoming more relevant, less relevant, or obsolete in the
outside world.

Covers:

- competitor analysis
- tech tool upgrades and industry shifts
- LinkedIn
- Instagram
- YouTube
- Twitter
- WhatsApp
- Telegram
- public comments and chatter

### 10. Customer and Sales Intelligence

This dimension captures buying-side perception, confusion, resistance, and escalation.

Covers:

- customer support escalations
- sales and pre-sales resistance
- ad-hoc offline discussions
- in-person user calls
- user group meetups

### 11. Internal Expertise

This dimension captures expert judgment that data alone cannot resolve.

Covers:

- curriculum development, design, and SME teams
- product and software developers
- pedagogy experts
- technical-round insights from developers
- placement ops teams

## Design Sequence

The current intended design sequence is:

1. **Dimension 5** sets the slot budget.
2. **Dimension 4** reserves mandatory slots and hard constraints.
3. **Dimensions 1, 2, and 3** decide what fills the remaining slots.
4. **Dimensions 7, 8, 9, 10, and 11** sharpen and pressure-test those choices.
5. **Dimension 6** distributes the final plan across semesters or delivery blocks for operational balance.

## Planned Source And Digest Model

Each dimension should eventually have:

1. canonical source inputs under `knowledge/sources/` or `knowledge/catalog/`
2. a runtime synthesized digest or entity layer in `storage/wiki/` or cycle artifacts
3. explicit influence points in Loop B design stages

The design goal is to keep raw evidence canonical and versioned, while the runtime wiki
stores synthesized operating knowledge rather than becoming the source of truth.

Important source-model note:

- many canonical source families are shared across stacks
- a "shared" family means the evidence category and storage pattern are common
- individual files or exports may still be stack-scoped or stack-filtered inside that shared family
- interview intelligence, hiring, competitor, and market evidence should be treated as shared
  source families even when a given export is produced for one stack such as `genai`

### Dimension 1: Job / Placement Outcomes

- Canonical sources:
  - stack-level target roles and role-skill expectations
  - shared hiring summaries and role-demand signals under `knowledge/sources/dimension_1_job_outcomes/hiring/`
  - interview-intelligence aggregated exports such as:
    - `role_opportunity_summary`
    - `skill_opportunity_summary`
    - `course_opportunity_summary`
    - `topic_relevance_summary`
    - `topic_sequencing_summary`
    - `question_type_distribution`
    - `question_depth_summary`
    - `package_band_summary`
    - `recency_retirement_summary`
  - skill-assessment patterns and performance summaries
  - interview-assessment performance summaries
- Channel-contract note:
  - interview intelligence is one first-class shared Dimension 1 channel, not the entire dimension
  - high-volume question collections should prefer canonical aggregated exports or normalized snapshots instead of direct raw-event ingestion in the first wave
  - other Dimension 1 channels such as placement-readiness and skill-assessment-performance feeds should later add their own canonical source families and runtime digests
- Planned runtime digests:
  - `skill_outcomes_signal_digest`
  - `role_profile` runtime entities
- Primary Loop B influence:
  - Brief
  - curriculum structure
  - assessment alignment
- Planned implementation wave:
  - Wave 1

### Dimension 2: Student Learning Outcomes

- Canonical sources:
  - target-audience profiles
  - mentor and instructor observations
  - queries and support themes
  - in-app content feedback
  - classroom and module assessment performance
  - engagement and retention summaries
- Planned runtime digests:
  - `learning_outcomes_signal_digest`
  - audience-need overlays
- Primary Loop B influence:
  - Brief
  - module design
  - topic design
  - practice design
- Planned implementation wave:
  - Wave 1

### Dimension 3: Degree And Higher Ed Outcomes

- Canonical sources:
  - academic benchmark docs
  - BOS outcome expectations
  - GATE and MS readiness targets
  - higher-ed preparation notes
- Planned runtime digests:
  - `degree_outcomes_digest`
- Primary Loop B influence:
  - Brief
  - curriculum structure
  - assessment design
- Planned implementation wave:
  - Wave 1

### Dimension 4: Regulatory Compliance

- Canonical sources:
  - AICTE tables
  - UGC and NEP constraints
  - degree-credit rules
- Planned runtime digests:
  - `regulatory_constraints_digest`
- Primary Loop B influence:
  - structure profile
  - curriculum container generation
  - slot reservation
- Planned implementation wave:
  - Wave 1

### Dimension 5: University Policy And Infrastructure Constraints

- Canonical sources:
  - university calendars
  - delivery-mode agreements
  - lab and infra capacity
  - timetable and slot constraints
- Planned runtime digests:
  - `delivery_constraints_digest`
  - `time_budget_context`
- Primary Loop B influence:
  - Brief
  - curriculum generation
  - packaging resolution
- Planned implementation wave:
  - Wave 1

### Dimension 6: Operational Efficiency

- Canonical sources:
  - faculty deployment plans
  - program-ops constraints
  - semester-wise load distributions
- Planned runtime digests:
  - `operational_planning_digest`
- Primary Loop B influence:
  - curriculum balancing
  - later semester or block allocation
- Planned implementation wave:
  - Wave 2

### Dimension 7: Cross-Product Alignment

- Canonical sources:
  - product comparison docs
  - placed-user feedback
  - related bootcamp or workshop learnings
- Planned runtime digests:
  - `cross_product_alignment_digest`
- Primary Loop B influence:
  - Brief
  - curriculum pressure-testing
- Planned implementation wave:
  - Wave 2

### Dimension 8: Industry Partnerships And Certifications

- Canonical sources:
  - partner workshop notes
  - certification-track expectations
  - external tool adoption requirements
- Planned runtime digests:
  - `partnership_and_certification_digest`
- Primary Loop B influence:
  - Brief
  - assessment alignment
  - optional curriculum enrichments
- Planned implementation wave:
  - Wave 2

### Dimension 9: Market And Community Signals

- Canonical sources:
  - shared competitor summaries under `knowledge/sources/dimension_9_market_and_community/competitors/`
  - shared market and trend summaries under `knowledge/sources/dimension_9_market_and_community/market/`
- Planned runtime digests:
  - `market_and_community_digest`
- Primary Loop B influence:
  - curriculum pressure-testing
  - differentiation
- Planned implementation wave:
  - Wave 3

### Dimension 10: Customer And Sales Intelligence

- Canonical sources:
  - escalated support themes
  - sales objections
  - calls and meetup notes
- Planned runtime digests:
  - `customer_and_sales_digest`
- Primary Loop B influence:
  - Brief
  - differentiation
  - explanation strategy
- Planned implementation wave:
  - Wave 3

### Dimension 11: Internal Expertise

- Canonical sources:
  - SME notes
  - pedagogy reviews
  - developer and placement-ops inputs
- Planned runtime digests:
  - `internal_expertise_digest`
- Primary Loop B influence:
  - all design stages as a pressure-test layer
- Planned implementation wave:
  - Wave 3

## Where This Sits In The Architecture

This framework should eventually influence:

- structure profiles
- curriculum-container generation
- product overlays
- packaging decisions
- assessment design

Examples:

- a NIAT academic structure profile may strongly activate Dimensions 3, 4, 5, and 6
- an Academy certification structure may strongly activate Dimensions 1, 2, 7, and 8
- a Launchpad-style structure may strongly activate Dimensions 1, 7, 9, and 11

## Implementation Waves

The current intended rollout is:

### Wave 1

- Dimension 1: Job / Placement Outcomes
- Dimension 2: Student Learning Outcomes
- Dimension 3: Degree and Higher Ed Outcomes
- Dimension 4: Regulatory Compliance
- Dimension 5: University Policy and Infrastructure Constraints

These are the dimensions that most directly shape curriculum structure and slot budgeting.

### Wave 2

- Dimension 6: Operational Efficiency
- Dimension 7: Cross-Product Alignment
- Dimension 8: Industry Partnerships and Certifications

These should pressure-test and operationalize the curriculum once the base structure is stable.

### Wave 3

- Dimension 9: Market and Community Signals
- Dimension 10: Customer and Sales Intelligence
- Dimension 11: Internal Expertise

These remain important, but should not destabilize the first structural rollout.

## Feedback Channel Maintenance Note

The intent is to preserve all feedback channels from this framework, even before every
dimension is fully automated.

So the current architecture should be read as:

- all 11 dimensions are part of the long-term design contract
- only a subset is operationalized in code today
- the remaining dimensions should still be represented in docs, manifests, and rollout planning
- runtime implementation should happen incrementally, not by ignoring the unimplemented dimensions

## TODO

- define explicit `design_priority_profile` artifacts
- decide which dimensions are default for each structure profile
- decide which dimensions are configurable by product overlay
- connect Loop A signal categories directly to these priority dimensions
- add `time_budget_context` and other hard-constraint digests as structured inputs before curriculum generation
