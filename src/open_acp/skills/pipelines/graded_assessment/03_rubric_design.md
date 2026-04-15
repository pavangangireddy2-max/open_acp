# Stage: Rubric Design — Graded Assessment

## Your Role
You are creating a formal marking scheme for an academic exam, suitable for use by multiple markers with moderation.

## What's Different from Other Assessment Rubrics
- Must be a formal **marking scheme** (not just a rubric — detailed point-by-point scoring)
- Must support **moderation** (external examiner review)
- Partial credit rules must be precise enough for consistent grading across markers
- Long-answer questions need band descriptors, not just checklists

## Process

### Step 1: Section A Marking Scheme
- MCQ: Answer key (no partial credit)
- Short answer: Model answer + key terms required + acceptable alternatives
- Total marks per question clearly stated

### Step 2: Section B Marking Scheme
For each applied/code question:
- **Model answer**: Complete solution
- **Mark breakdown**: Points allocated to specific components
  - Correct approach/algorithm: X marks
  - Correct implementation: X marks
  - Edge case handling: X marks
  - Code quality/comments: X marks (if applicable)
- **Partial credit rules**: Specific scenarios and their scores
  - "Correct approach but syntax errors: -1 mark"
  - "Correct for happy path but misses edge cases: -2 marks"
- **Common errors**: Expected wrong answers and how to score them

### Step 3: Section C Marking Scheme — Band Descriptors
For long-answer/essay questions:

| Band | Marks | Descriptor |
|------|-------|-----------|
| Excellent | 8-10 | Comprehensive analysis, multiple perspectives, specific examples, clear justification |
| Good | 6-7 | Solid analysis, relevant examples, mostly justified |
| Adequate | 4-5 | Basic analysis, some examples, partial justification |
| Weak | 2-3 | Superficial analysis, few examples, weak justification |
| Poor | 0-1 | Irrelevant or missing |

Each question gets its own band descriptor with question-specific criteria.

### Step 4: Moderation Guide
- Instructions for double-marking (which questions require it)
- Calibration: sample scripts at different grade levels
- Dispute resolution process for borderline cases

## Output Format
```json
{
  "marking_scheme": {
    "section_a": {
      "answer_key": [{"id": "A1", "correct": "B", "marks": 2}],
      "short_answer_models": [{"id": "A15", "model_answer": "...", "key_terms": ["term1"], "marks": 3}]
    },
    "section_b": {
      "mark_breakdowns": [
        {"id": "B1", "total_marks": 5, "components": [{"aspect": "Correct algorithm", "marks": 2}, {"aspect": "Implementation", "marks": 2}, {"aspect": "Edge cases", "marks": 1}]}
      ]
    },
    "section_c": {
      "band_descriptors": [{"id": "C1", "total_marks": 10, "bands": {"excellent": "...", "good": "...", "adequate": "...", "weak": "...", "poor": "..."}}]
    }
  },
  "moderation_guide": {
    "double_marking_required": ["C1", "C2", "C3"],
    "sample_scripts": "Provided at 3 grade levels"
  },
  "total_marks": 100,
  "grade_boundaries": {"A": 70, "B": 60, "C": 50, "D": 40, "F": 0}
}
```

## Quality Criteria
- Every question has explicit mark allocation and model answer
- Section C has band descriptors (not just binary scoring)
- Partial credit rules cover the most common error scenarios
- Moderation guide is included
- Grade boundaries are defined
- Two markers would assign the same grade (+/- 3 marks on 100)
