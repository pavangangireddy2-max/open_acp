# Stage: Rubric Design — Module Quiz

## Your Role
You are creating a scoring rubric for the module quiz with clear partial credit rules.

## What's Different from Classroom Quiz
- More total points (reflecting more questions and higher stakes)
- More nuanced partial credit (especially for code and analysis questions)
- Must support consistent grading across multiple graders

## Process
Follow `classroom_quiz/03_rubric_design` with these modifications:

### Point Allocation
- MCQ: 1-2 points each
- Short answer: 2-3 points each
- Code tracing: 3 points (partial credit for correct approach, wrong final answer)
- Cross-session integration: 3-4 points (partial credit for addressing each component)

### Partial Credit for Code/Analysis Questions
- Show correct reasoning but wrong answer: 60-70% credit
- Correct approach but implementation error: 50% credit
- One component correct, other wrong: proportional credit
- Must specify EXACTLY what earns each partial credit level

### Grading Consistency
- Provide 2-3 example responses at different quality levels for each short answer
- Specify "must include" terms for full credit
- Specify "acceptable alternatives" for terminology

## Output Format
Same structure as `classroom_quiz/03_rubric_design`, with higher point totals and more detailed partial credit rules.

## Quality Criteria
- Total points scale to 25-40 range
- Partial credit rules are unambiguous
- Example responses provided for all non-MCQ questions
- Two graders would assign the same score (+/- 1 point)
- Passing threshold is defined (typically 60%)
