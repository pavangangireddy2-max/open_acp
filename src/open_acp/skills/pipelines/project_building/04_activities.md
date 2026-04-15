# Stage: Activities Design — Project Building

## Your Role
You are designing milestone-based build activities where each builds on the previous.

## What's Different from Concept Explainer
- Activities ARE the milestones — each activity produces a project component
- Activities are **sequential and cumulative** (not independent)
- Pair programming suggestions are included for each activity
- Activities include "stretch goals" for advanced learners

## Process
Follow `concept_explainer/04_activities` with these modifications:

### Step 2: Design Milestone Activities
For each project milestone:
- **Build task**: The core deliverable (required)
- **Teaching mode**: Preserve the section mode from the outline
- **Pair programming mode**: Suggest driver/navigator roles and swap points
- **Verification checklist**: How to confirm the milestone is complete
- **Stretch goal**: Optional enhancement for fast learners
- **Checkpoint**: Instructor pause point to ensure everyone is caught up

### Step 3: Integration Activity
The final activity should be:
- Connecting all milestones into the working project
- Running the full test suite
- Demo preparation (what to show, in what order)

## Output Format
Same as `concept_explainer/04_activities`, with additional fields:
```json
{
  "activities": [
    {
      "type": "build",
      "title": "Milestone 1: API Skeleton",
      "instructions": "...",
      "verification_checklist": ["Server starts without errors", "GET /health returns 200"],
      "pair_programming": "Driver writes code, navigator reviews and checks docs. Swap after 10 min.",
      "stretch_goal": "Add a /version endpoint that returns the app version from a config file",
      "time_minutes": 20,
      "bloom_level": "create",
      "objective_ids": ["obj_1"],
      "depends_on": [],
      "teaching_mode": "guided_build"
    }
  ]
}
```

## Quality Criteria
- Activities are sequential — each depends on previous milestones
- Every activity has a verification checklist
- Pair programming suggestions are specific (not just "work together")
- At least one stretch goal per milestone
- Final activity integrates all components
- Activities should reflect whether the milestone is a concept, architecture, build, or integration checkpoint
