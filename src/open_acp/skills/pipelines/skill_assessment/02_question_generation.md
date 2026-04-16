# Stage: Question Generation — Skill Assessment

## Your Role
You are writing 15-20 questions that test applied skill readiness across the configured assessment window.

## What's Different from Module Quiz
- Larger question set (15-20 vs 10-15)
- Cross-topic or cross-module integration when relevant
- Earlier material tested at higher Bloom levels (retention check)
- More Apply/Analyze, less Remember

## Process
Follow `module_quiz/02_question_generation` with these modifications:

### Format Mix
- 8-10 MCQ questions
- 3-4 Short answer / explain
- 2-3 Code tracing / output prediction / debugging
- 2-3 Integration questions (scenario-based when relevant)

### Retention Questions
For material from earlier in the assessment window:
- Test at Apply level, not Remember (the learner should have internalized the basics)
- "Given [previously taught concept], solve this new problem"
- These questions verify that learning has stuck, not just been crammed

### Integration Questions
- Scenario-based: "You're building X and encounter Y. How do you handle it?"
- Comparison: "Compare approach A with approach B for this use case"
- These are often the hardest questions, so place them toward the end

## Output Format
Same as `module_quiz/02_question_generation`.

## Quality Criteria
- 15-20 questions covering the configured assessment window
- Earlier material tested at higher Bloom level than original instruction
- Integration questions included when the assessment scope requires them
- At least 4 format types used
- No question requires knowledge not yet taught
