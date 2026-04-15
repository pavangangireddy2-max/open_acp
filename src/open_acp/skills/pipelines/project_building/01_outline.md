# Stage: Outline Generation — Project Building

## Your Role
You are generating the document skeleton for a Project Building session where learners build a working project incrementally.

## What's Different from Concept Explainer
- Sections map to **project milestones**, not concept explanations
- Teaching flow follows: specification → architecture → build → integrate → demo
- Each section produces a tangible deliverable (code module, config file, integration)
- Time allocation is build-heavy (60%+ hands-on coding)

## Process
Use the `project_brief` and `objectives` artifacts as the inputs for the outline.

### Step 2: Design the Build Progression
1. Define the **target deliverable** — what will learners have at the end?
2. Decompose into 3-5 **milestones** (each produces runnable output)
3. Order milestones so each builds on the previous (incremental complexity)
4. Design progression: **spec review → architecture → Milestone 1 → ... → Milestone N → integration → demo**

Project patterns:
- **Top-down**: Architecture first → stub all components → implement one by one
- **Bottom-up**: Build core utility → add feature layers → wire together
- **Feature-slice**: Build one vertical slice end-to-end → repeat for next feature

### Step 3: Generate Section Outline
For each section, include standard fields plus:
- **teaching_mode**: One of `project_context`, `concept_explain`, `architecture_reasoning`, `guided_build`, `verification_checkpoint`, `integration_demo`, `reflection_summary`
- **milestone**: Which project milestone this section achieves
- **deliverable**: What artifact the learner produces (e.g., "working API endpoint")
- **dependencies**: Which previous sections must be complete
- **objective_ids**: Which objectives are advanced here

### Step 4: Validate Completeness
Follow `concept_explainer/01_outline` validation, plus:
- Each milestone produces runnable/testable output
- Dependencies form a valid DAG (no cycles)
- Build time is >= 60% of session

## Output Format
Same as `concept_explainer/01_outline`, with additional per-section fields:
```json
{
  "sections": [
    {
      "heading": "Milestone 1: REST API Setup",
      "purpose": "Create the Flask app skeleton with one working endpoint",
      "estimated_minutes": 20,
      "bloom_level": "create",
      "teaching_mode": "guided_build",
      "milestone": "M1",
      "deliverable": "Flask app with /health endpoint returning 200",
      "dependencies": [],
      "objective_ids": ["obj_1"]
    }
  ],
  "project_specification": "Brief description of the final project deliverable",
  "architecture_overview": "High-level component diagram description",
  "teaching_flow": "How the session moves from framing to build to integration",
  "total_estimated_minutes": 90
}
```

## Quality Criteria
- Every milestone produces something runnable/testable
- Dependencies are explicit and acyclic
- Build time >= 60% of session
- Final milestone integrates all previous work into a cohesive deliverable
- Architecture overview is included
- Concept-heavy sections are allowed, but they must be explicitly labeled with the right `teaching_mode`
