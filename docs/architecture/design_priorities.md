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

- placement readiness
- interview intelligence
- written tests
- take-home projects
- skill assessment performance
- interview assessment performance
- recruiter first-hand insights
- corporate skill assessments

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
- engagement and retention analytics

### 3. Degree and Higher Ed Outcomes

This dimension captures academic grade performance and readiness for higher studies.

It influences:

- revision blocks
- exam-prep slots
- foundational academic subjects
- GATE and MS readiness

Covers:

- classroom assessment performance
- module assessment performance
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

## TODO

- define explicit `design_priority_profile` artifacts
- decide which dimensions are default for each structure profile
- decide which dimensions are configurable by product overlay
- later connect Loop A signal categories directly to these priority dimensions
