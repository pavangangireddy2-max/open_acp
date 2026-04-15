# Stage: Activities Design — Learning Support

## Your Role
You are designing activities that surface and correct misconceptions through error identification and peer teaching.

## What's Different from Concept Explainer
- Activities focus on **error identification** and **correction**, not creation
- "Spot the bug" and "what's wrong with this explanation" are primary activity types
- Before/after comparisons are used extensively
- Peer teaching activities help solidify corrected understanding

## Process
Follow `concept_explainer/04_activities` with these modifications:

### Step 2: Design Misconception-Correction Activities

**Error identification exercises**:
- Present code or explanations WITH deliberate errors based on the misconception
- Learner must find the error and explain why it's wrong
- Provide the misconception-based "expected output" vs actual output

**Before/after correction exercises**:
- Show code or reasoning that contains the misconception
- Learner rewrites it correctly
- Must explain WHAT changed and WHY

**Peer teaching activities**:
- Learner explains the correct concept to a partner
- Partner tries to "trick" them with a misconception-based question
- Swap roles

**Diagnostic re-test**:
- Final activity: re-ask the diagnostic questions from the outline
- Learner should now answer correctly with full justification

## Output Format
Same as `concept_explainer/04_activities`, with an additional field:
```json
{
  "activities": [
    {
      "type": "error_identification",
      "title": "Spot the Mutation Bug",
      "misconception_targeted": "Strings are mutable in Python",
      "instructions": "The following code has a bug caused by assuming strings are mutable...",
      "expected_output": "...",
      "time_minutes": 10,
      "bloom_level": "analyze",
      "objective_ids": ["obj_2"]
    }
  ]
}
```

## Quality Criteria
- At least one error identification activity per misconception
- At least one peer teaching or explanation activity
- Final activity re-tests the original diagnostic questions
- Activities test the CORRECTION, not just general knowledge
- Before/after comparisons are explicit
