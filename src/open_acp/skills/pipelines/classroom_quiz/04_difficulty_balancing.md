# Stage: Difficulty Balancing — Classroom Quiz

## Your Role
You are verifying that the quiz difficulty matches its formative purpose and target Bloom distribution.

## Process

### Step 1: Verify Bloom Distribution
Check that the actual question Bloom levels match targets:
- Remember: 40-50%
- Understand: 30-40%
- Apply: 10-20%

### Step 2: Assess Overall Difficulty
For a classroom quiz:
- Average student who attended the session should score 70%+
- No question should require knowledge beyond the single session's material
- No trick questions or "gotcha" edge cases

### Step 3: Check Time Feasibility
- Total answering time should be 15-20 minutes
- MCQ: ~1-2 minutes each
- True/False + explain: ~2-3 minutes each
- Short answer: ~3 minutes each
- Sum should not exceed the time limit

### Step 4: Balance Adjustments
If difficulty is too high:
- Simplify stems (remove unnecessary context)
- Make distractors less similar to the correct answer
- Reduce code complexity

If difficulty is too low:
- Add an Apply-level question
- Make distractors more plausible

## Output Format
```json
{
  "balance_report": {
    "bloom_match": true,
    "estimated_completion_time": 17,
    "expected_average_score": 0.75,
    "adjustments_made": ["Simplified q_3 stem", "Added more plausible distractor to q_1"],
    "final_question_order": ["q_1", "q_3", "q_2", "q_5", "q_4", "q_6"]
  }
}
```

## Quality Criteria
- Bloom distribution matches targets within 10%
- Estimated completion time is 15-20 minutes
- Expected average score is 70-85% (formative, not punitive)
- Questions ordered easiest to hardest
- No question requires out-of-scope knowledge
