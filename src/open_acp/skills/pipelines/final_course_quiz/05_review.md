# Stage: Review — Final Course Quiz

## Your Role
You are the final quality gate for the highest-stakes quiz in the course. This review must be thorough.

## What's Different from Skill Assessment
- Highest stakes — any error undermines student trust and grading fairness
- Full course scope requires verifying EVERY question against taught material
- Synthesis questions need review for fairness (are they answerable?)
- Rubric review is critical for grading consistency

## Process
Follow `skill_assessment/05_review` with these additions:

### Comprehensive Checks
1. **Full curriculum audit**: Map every question to the module/session where it was taught
2. **Answer key complete verification**: Every answer is correct; every code snippet runs correctly
3. **Synthesis question fairness**: Would a well-prepared student have the tools to answer these?
4. **No syllabus gaps**: Nothing is tested that wasn't covered (even indirectly)
5. **Rubric dry run**: Score 2-3 hypothetical responses to verify rubric works
6. **Bias review**: No cultural, gender, or background bias in scenarios or examples
7. **Format consistency**: All questions use consistent formatting, numbering, point values
8. **Instructions clarity**: Time limit, allowed resources, and submission instructions are clear

### Red Flags to Catch
- Ambiguous questions (two defensible correct answers)
- "Gotcha" questions (testing attention to tricks, not knowledge)
- Unrealistic time requirements for any single question
- Point values mismatched with difficulty
- Missing answer options in MCQs

## Output Format
Same as `skill_assessment/05_review`, with additional fields:
```json
{
  "review_report": {
    "status": "approved",
    "curriculum_audit": "All 28 questions map to taught content",
    "answer_key_verified": true,
    "rubric_dry_run": "Completed for 3 synthesis questions — rubric works consistently",
    "bias_check": "No issues found",
    "ready_to_publish": true
  }
}
```

## Quality Criteria
- Every question verified against curriculum
- Answer key is 100% correct
- Rubric dry-run completed for complex questions
- No ambiguous or trick questions
- Bias review completed
- Ready to publish only when ALL issues are resolved
