# Checkpoint Protocol

## Purpose
Persist stage state and optionally request human approval before proceeding.

## Process

### Step 1: Check Gate Requirements
- Read `checkpoint_required` and `human_approval_default` from the pipeline manifest
- If checkpoint not required, skip to Step 4

### Step 2: Prepare Checkpoint Data
- Stage name and status
- Canonical artifact (validated against schema)
- Review findings from the reviewer
- Cost snapshot (estimated vs actual for this stage)

### Step 3: Human Approval (if required)
Present to the human reviewer:
- Stage summary (what was produced)
- Key decisions made (and why)
- Quality metrics
- Cost so far vs budget

Wait for: APPROVE, REVISE (with notes), or ABORT

### Step 4: Determine Next Stage
- Read the pipeline manifest's stage list
- Find the current stage index
- Return the next stage ID (or "complete" if this was the last stage)

## Gate Mapping
- **G1 (Advisory):** Loop A — only triggers on significant drift
- **G2 (Always Blocking):** Loop B — curriculum must be approved
- **G3 (Blocking/Relaxable):** Loop C — per-batch content review
- **G4 (Blocking for Critical):** Loop D — high-severity fixes
