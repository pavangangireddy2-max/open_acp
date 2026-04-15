# Stage: Scope Definition — Graded Assessment

## Your Role
You are defining the scope for a formal graded assessment / exam (30-40 questions, 90-120 minutes) with university-level rigor.

## Assessment Profile
- **Purpose**: Formal examination — official evaluation for academic records
- **Duration**: 90-120 minutes
- **Question count**: 30-40 questions
- **Bloom focus**: Full Bloom range (Remember through Evaluate)
- **Scope**: Full course or designated portion
- **Stakes**: Highest — official academic grade, possible proctored
- **Standards**: University grading standards, strict time limits, academic integrity measures

## What's Different from Final Course Quiz
- More questions (30-40 vs 25-30) and longer duration (90-120 min vs 60-75 min)
- Full Bloom range including Evaluate (quiz stops at Analyze typically)
- Formal exam conditions: strict time limits, no collaboration, academic integrity
- University grading standards: moderation, external examiner considerations
- Multiple question formats including long-form answers

## Process
Follow `final_course_quiz/01_scope_definition` with these modifications:

### Step 1: Formal Scope Definition
- Define the official exam scope (what's included and what's excluded)
- Reference the course syllabus and learning outcomes
- Identify which course learning outcomes (CLOs) this exam assesses
- Ensure alignment with any accreditation requirements

### Step 2: Define the Bloom Distribution
Target for formal graded assessment (full range):
- **Remember**: 10-15% (4-5 questions)
- **Understand**: 20-25% (7-8 questions)
- **Apply**: 25-30% (9-10 questions)
- **Analyze**: 20-25% (7-8 questions)
- **Evaluate**: 10-15% (3-5 questions)

### Step 3: Section Structure
Organize the exam into sections:
- **Section A**: Short answer / MCQ (40% of marks, tests breadth)
- **Section B**: Applied problems / code (35% of marks, tests depth)
- **Section C**: Analysis / essay / design (25% of marks, tests synthesis)

### Step 4: Academic Integrity Measures
- Define allowed resources (open book, closed book, cheat sheet)
- Plan for multiple exam versions (if needed for integrity)
- Include instructions about academic honesty on the exam paper

## Output Format
```json
{
  "assessment_profile": {
    "type": "graded_assessment",
    "purpose": "formal_examination",
    "duration_minutes": 120,
    "question_count": 35,
    "scope": "Full course",
    "stakes": "highest",
    "conditions": "closed_book_proctored"
  },
  "sections": [
    {"label": "Section A", "format": "MCQ + Short Answer", "marks_percentage": 40, "question_count": 20},
    {"label": "Section B", "format": "Applied Problems", "marks_percentage": 35, "question_count": 10},
    {"label": "Section C", "format": "Analysis / Design", "marks_percentage": 25, "question_count": 5}
  ],
  "bloom_distribution": {"remember": 5, "understand": 8, "apply": 10, "analyze": 8, "evaluate": 4},
  "clo_mapping": {"CLO1": 8, "CLO2": 10, "CLO3": 9, "CLO4": 8}
}
```

## Quality Criteria
- 30-40 questions spanning full Bloom range
- Sectioned exam paper (short + applied + analysis)
- Every course learning outcome (CLO) is assessed
- Academic integrity measures defined
- Duration is 90-120 minutes with clear time guidance per section
- Exam conditions specified (open/closed book, allowed resources)
