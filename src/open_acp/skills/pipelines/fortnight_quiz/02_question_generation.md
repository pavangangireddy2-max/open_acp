# Stage: Question Generation — Fortnight Quiz

## Your Role
You are writing 15-20 questions that test cumulative understanding across 2 modules.

## What's Different from Module Quiz
- Larger question set (15-20 vs 10-15)
- Cross-MODULE integration (not just cross-session)
- Earlier material tested at higher Bloom levels (retention check)
- More Apply/Analyze, less Remember

## Process
Follow `module_quiz/02_question_generation` with these modifications:

### Format Mix
- 8-10 MCQ questions
- 3-4 Short answer / explain
- 2-3 Code tracing / output prediction / debugging
- 2-3 Cross-module integration questions (scenario-based)

### Retention Questions
For material from the earlier module:
- Test at Apply level, not Remember (they should have internalized the basics)
- "Given [concept from Module 1], solve this new problem"
- These questions verify that learning has stuck, not just been crammed

### Cross-Module Integration
- Scenario-based: "You're building X (Module 2 concept) and encounter Y (Module 1 concept). How do you handle it?"
- Comparison: "Compare approach A (Module 1) with approach B (Module 2) for this use case"
- These are the hardest questions — place them at the end

## Output Format
Same as `module_quiz/02_question_generation`.

## Quality Criteria
- 15-20 questions covering both modules
- Earlier module tested at higher Bloom level than original instruction
- At least 3 cross-module integration questions
- At least 4 format types used
- No question requires knowledge not yet taught
