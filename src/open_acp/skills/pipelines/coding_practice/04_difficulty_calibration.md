# Stage: Difficulty Calibration — Coding Practice

## Your Role
You are calibrating problem difficulty through time estimates, complexity labels, and hint count adjustments.

## Process

### Step 1: Assign Time Estimates
Based on problem characteristics:
- **Warm-up** (5-10 min): Single concept, obvious approach, 1-2 edge cases
- **Core** (15-20 min): Requires design thinking, 2 concepts combined, several edge cases
- **Challenge** (20-30 min): Non-obvious approach, optimization required, many edge cases

Factors that increase time:
- Multiple valid approaches (decision paralysis)
- Tricky edge cases (off-by-one, empty input)
- Need for a data structure the learner may not immediately think of

### Step 2: Assign Complexity Labels
- **Conceptual complexity**: How many concepts must the learner combine?
- **Implementation complexity**: How many lines of code is the solution?
- **Edge case complexity**: How many special cases must be handled?

Label each: Low / Medium / High

### Step 3: Calibrate Hint Count
- Warm-up: 2 hints (less hand-holding needed)
- Core: 3 hints (standard progression)
- Challenge: 4-5 hints (more scaffolding for hard problems)

Review each hint:
- Is hint 1 too revealing? (Should only point a direction)
- Is the last hint too close to the solution? (Should be pseudocode, not code)

### Step 4: Verify the Difficulty Ramp
- Problems should be solvable in sequence (each prepares for the next)
- No challenge problem should require techniques not exercised in a core problem
- Total time should fit the session budget (60-90 minutes)

## Output Format
```json
{
  "calibrated_problems": [
    {
      "problem_id": "p_1",
      "difficulty_tier": "warm-up",
      "time_estimate_minutes": 10,
      "conceptual_complexity": "low",
      "implementation_complexity": "low",
      "edge_case_complexity": "medium",
      "hint_count": 2,
      "adjustment_notes": "Reduced from core to warm-up — single concept, direct application"
    }
  ],
  "recommended_order": ["p_1", "p_3", "p_2", "p_4", "p_5"],
  "total_estimated_minutes": 75,
  "session_fit": "Fits within 90-minute budget with 15 minutes buffer"
}
```

## Quality Criteria
- Time estimates are realistic for the target audience (not expert speed)
- Difficulty ramp is smooth (no jarring jumps)
- Hint counts match difficulty (more hints for harder problems)
- Total time fits session budget
- Each problem builds toward the next (skill progression, not random order)
