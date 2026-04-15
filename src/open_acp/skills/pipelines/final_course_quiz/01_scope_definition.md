# Stage: Scope Definition — Final Course Quiz

## Your Role
You are defining the scope for a comprehensive final course quiz (25-30 questions, 60-75 minutes) covering the entire course.

## Assessment Profile
- **Purpose**: Summative — comprehensive evaluation of course mastery
- **Duration**: 60-75 minutes
- **Question count**: 25-30 questions
- **Bloom focus**: Analyze/Evaluate (with supporting Understand/Apply)
- **Scope**: Entire course (all modules)
- **Stakes**: High — major grade component

## Process
Follow `fortnight_quiz/01_scope_definition` with these modifications:

### Step 1: Full Course Scope
- Review ALL modules and their key objectives
- Create a concept map of the entire course showing interconnections
- Identify the "big ideas" — overarching themes that span modules
- Weight by importance: foundational topics get more questions

### Step 2: Define the Bloom Distribution
Target for final course quiz:
- **Remember**: 5-10% (1-3 questions: only the most critical definitions/facts)
- **Understand**: 20-25% (5-7 questions)
- **Apply**: 30-35% (8-10 questions)
- **Analyze**: 25-30% (7-8 questions)
- **Evaluate**: 5-10% (1-3 questions: justify, critique, select best approach)

### Step 3: Comprehensive Coverage Strategy
- Every module must have at least 2 questions
- At least 5 questions should span multiple modules
- "Big idea" questions test whether learners see the forest, not just the trees
- Include at least 1 synthesis question: "Given everything you've learned, how would you approach...?"

## Output Format
```json
{
  "assessment_profile": {
    "type": "final_course_quiz",
    "purpose": "comprehensive_summative",
    "duration_minutes": 70,
    "question_count": 28,
    "scope": "Full course (Modules 1-8)",
    "stakes": "high"
  },
  "bloom_distribution": {"remember": 2, "understand": 6, "apply": 9, "analyze": 8, "evaluate": 3},
  "module_coverage": {"module_1": 3, "module_2": 4, "...": "..."},
  "cross_module_questions": 5,
  "big_idea_questions": 3
}
```

## Quality Criteria
- 25-30 questions covering the full course
- Every module has at least 2 questions
- At least 5 cross-module questions
- Bloom distribution reaches Analyze/Evaluate levels
- Duration is 60-75 minutes
- "Big idea" synthesis questions are included
