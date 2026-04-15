# Self-Review Protocol

## Purpose
After completing a pipeline stage, review the output against quality criteria before checkpointing.

## Process

### Step 1: Load Review Context
- Read the stage's `review_focus` items from the pipeline manifest
- Load the artifact schema for this stage
- Load the brand playbook if the stage involves content

### Step 2: Validate Artifact
- Check the output against the JSON schema — structural correctness
- Verify all required fields are present and non-empty
- Check referential integrity (e.g., objectives reference valid skill IDs)

### Step 3: Evaluate Quality
For each review_focus item, assess on a 3-point scale:
- **PASS** — meets the criterion
- **WARNING** — minor issues that don't block progress
- **FAIL** — must be fixed before proceeding

### Step 4: Decision
- **All PASS or WARNING** → PASS (proceed to next stage)
- **Any FAIL, round < max_review_rounds** → REVISE (fix failures, re-run this stage)
- **Any FAIL, round >= max_review_rounds** → PASS_WITH_WARNINGS (proceed with documented issues)

### Constraints
- Maximum 2 review rounds per stage (prevents infinite loops)
- Never block on WARNING-only findings
- Always document findings in the stage artifact metadata
