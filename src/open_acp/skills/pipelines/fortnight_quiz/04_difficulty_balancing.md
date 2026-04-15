# Stage: Difficulty Balancing — Fortnight Quiz

## Your Role
You are calibrating difficulty for a cumulative quiz spanning 2 modules.

## What's Different from Module Quiz
- Higher overall difficulty (cumulative, Apply/Analyze focus)
- Expected average score: 55-70%
- Must balance recent vs earlier material difficulty
- Cross-module questions are inherently harder — account for this

## Process
Follow `module_quiz/04_difficulty_balancing` with these modifications:

### Difficulty Targets
- Easy: 20-25% (baseline retention of key concepts)
- Medium: 45-50% (solid application required)
- Hard: 25-30% (analysis, cross-module integration)

### Cumulative Balance
- Earlier module questions: should be medium difficulty (testing retained application)
- Recent module questions: mix of easy and medium (more recently taught)
- Cross-module questions: medium to hard (inherently requires more synthesis)
- Ensure that a student who forgot Module 1 entirely can still pass (barely)

### Time Feasibility
- Total should fit within 35-45 minutes
- Hard/integration questions get 4-5 minutes each
- Average 2.5 minutes per question

## Output Format
Same as `module_quiz/04_difficulty_balancing`.

## Quality Criteria
- Expected average score is 55-70%
- Difficulty ramp: start easier, end harder
- Time fits within 35-45 minutes
- Quiz is passable even with weakness in one module
- No unfair spikes in difficulty
