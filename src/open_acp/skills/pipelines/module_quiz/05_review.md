# Stage: Review — Module Quiz

## Your Role
You are the quality gate for a medium-stakes module quiz. Review is more thorough than classroom quiz.

## What's Different from Classroom Quiz
- Higher stakes require stricter review
- Cross-session questions need extra scrutiny (are they fair? is the connection taught?)
- Code questions must be tested for correctness
- Rubric review is critical (will grading be consistent?)

## Process
Follow `classroom_quiz/05_review` with these additions:

### Additional Checks
- **Cross-session fairness**: Are integration questions testing connections that were actually taught?
- **Code correctness**: Run all code snippets mentally — verify stated outputs
- **Rubric alignment**: Does each question's rubric match its actual difficulty?
- **Coverage balance**: Does the quiz fairly represent all 4 sessions?
- **No duplicate testing**: No two questions test the same concept in the same way

## Output Format
Same as `classroom_quiz/05_review`.

## Quality Criteria
- All classroom_quiz review criteria, plus:
- Cross-session questions verified as fair
- All code snippets verified for correctness
- No two questions are redundant
- Coverage is balanced across sessions
- Rubric enables consistent grading
