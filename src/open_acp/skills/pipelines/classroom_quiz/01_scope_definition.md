# Stage: Scope Definition — Classroom Quiz

## Your Role
You are defining the scope for a short, formative classroom quiz (5-8 questions, 15-20 minutes).

## Assessment Profile
- **Purpose**: Formative — check understanding during/after a single session
- **Duration**: 15-20 minutes
- **Question count**: 5-8 questions
- **Bloom focus**: Remember/Understand (with 1-2 Apply questions)
- **Scope**: One session's material only
- **Stakes**: Low — used for feedback, not grading

## Process

### Step 1: Identify the Session Scope
- Review the single session this quiz covers
- List all concepts, terms, and skills introduced in that session
- Identify the most critical concepts (what MUST they understand to proceed?)

### Step 2: Define the Bloom Distribution
Target for classroom quiz:
- **Remember**: 40-50% (2-3 questions: definitions, facts, syntax)
- **Understand**: 30-40% (2-3 questions: explain why, compare, interpret)
- **Apply**: 10-20% (1-2 questions: trace code, predict output, solve simple problem)

### Step 3: Map Questions to Objectives
- Each session objective should be tested by at least 1 question
- No objective needs more than 2 questions (it's a short quiz)
- Prioritize objectives that are prerequisites for upcoming sessions

## Output Format
```json
{
  "assessment_profile": {
    "type": "classroom_quiz",
    "purpose": "formative",
    "duration_minutes": 15,
    "question_count": 6,
    "session_scope": "Session 3: Binary Search",
    "stakes": "low"
  },
  "bloom_distribution": {"remember": 3, "understand": 2, "apply": 1},
  "concept_coverage": ["binary search algorithm", "time complexity", "sorted array requirement"],
  "objective_mapping": {"obj_1": 2, "obj_2": 2, "obj_3": 2}
}
```

## Quality Criteria
- 5-8 questions total (no more, no less)
- Duration is 15-20 minutes (roughly 2-3 minutes per question)
- Bloom levels are weighted toward Remember/Understand
- Every session objective has at least 1 question
- Scope is limited to ONE session's material
