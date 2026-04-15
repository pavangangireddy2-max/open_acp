# Stage: Difficulty Calibration — MCQ Practice

## Your Role
You are reviewing and calibrating the difficulty of the question set to match target Bloom distributions and difficulty spread.

## Process

### Step 1: Label Difficulty Based on Cognitive Demand
Assess each question using these criteria:
- **Easy**: Single concept recall, direct application of a rule, no tricks
- **Medium**: Requires understanding of WHY (not just what), combines 2 concepts, code tracing with 3-5 steps
- **Hard**: Requires analysis of edge cases, multiple concepts interacting, non-obvious behavior, 5+ step code tracing

### Step 2: Verify Bloom Distribution
Compare actual distribution to targets:
- Remember: 20-30%
- Understand: 30-40%
- Apply: 20-30%
- Analyze: 10-20%

If distribution is off:
- Re-label questions where Bloom level doesn't match the actual cognitive demand
- Suggest questions to add or replace to hit targets

### Step 3: Verify Difficulty Spread
Target: ~30% easy, ~50% medium, ~20% hard

If spread is off:
- Suggest modifications to adjust difficulty (add/remove context, simplify/complicate code)
- Do NOT just re-label — actually propose changes

### Step 4: Final Quality Check
- Remove any questions that test the same concept in the same way (redundant)
- Ensure no question's difficulty depends on a "gotcha" (difficulty should come from cognitive demand, not tricks)
- Verify that question order progresses from easier to harder (for practice sets)

## Output Format
```json
{
  "calibrated_questions": [
    {
      "question_id": "q_1",
      "original_difficulty": "medium",
      "calibrated_difficulty": "easy",
      "bloom_level": "understand",
      "adjustment_notes": "Reduced from medium to easy — single concept, direct recall of reference behavior",
      "suggested_modifications": null
    }
  ],
  "bloom_distribution_actual": {"remember": 3, "understand": 5, "apply": 4, "analyze": 2},
  "bloom_distribution_target": {"remember": 3, "understand": 5, "apply": 4, "analyze": 2},
  "difficulty_distribution": {"easy": 4, "medium": 7, "hard": 3},
  "recommended_order": ["q_3", "q_1", "q_5", "..."],
  "questions_to_replace": [],
  "questions_to_add": []
}
```

## Quality Criteria
- Final Bloom distribution is within 10% of targets
- Difficulty spread is approximately 30/50/20 (easy/medium/hard)
- No redundant questions testing the same concept the same way
- No "gotcha" questions (difficulty from tricks, not cognitive demand)
- Recommended order progresses from easy to hard
