# Stage: Question Generation — Graded Assessment

## Your Role
You are writing 30-40 exam questions across the full Bloom range for a formal academic assessment.

## What's Different from Final Course Quiz
- More formats: MCQ, short answer, long answer, code writing, design questions, essay
- Higher rigor: questions must withstand external examiner scrutiny
- Section-based: different question types in different sections
- Full Bloom coverage including Evaluate-level questions
- Must be answerable under exam conditions (no internet, time pressure)

## Process
Follow `final_course_quiz/02_question_generation` with these modifications:

### Section A: MCQ + Short Answer (20 questions)
- 12-15 MCQ (follow `mcq_practice/02_question_generation` rules strictly)
- 5-8 Short answer (1-3 sentences, test precise knowledge)
- Bloom: Remember through Apply

### Section B: Applied Problems (10 questions)
- 4-5 Code writing problems (write a function, fix a bug, trace execution)
- 3-4 Problem-solving questions (design an approach, analyze complexity)
- 1-2 Scenario-based multi-part questions
- Bloom: Apply through Analyze

### Section C: Analysis / Design (5 questions)
- 2-3 Long-form analysis (compare approaches, justify decisions, critique designs)
- 1-2 Design questions (architect a solution, propose improvements)
- Expected answer length: 150-300 words each
- Bloom: Analyze and Evaluate

### Exam Paper Standards
- Clear mark allocation visible on every question: [X marks]
- Section instructions: how many to answer, time guidance
- Consistent formatting across all questions
- No ambiguity — every question has exactly one intended interpretation

## Output Format
```json
{
  "sections": {
    "A": {
      "instructions": "Answer ALL questions. Suggested time: 40 minutes.",
      "questions": [{"id": "A1", "format": "mcq", "marks": 2, "bloom_level": "remember", "...": "..."}]
    },
    "B": {
      "instructions": "Answer ALL questions. Suggested time: 45 minutes.",
      "questions": [{"id": "B1", "format": "code_writing", "marks": 5, "bloom_level": "apply", "...": "..."}]
    },
    "C": {
      "instructions": "Answer 3 out of 5 questions. Suggested time: 35 minutes.",
      "questions": [{"id": "C1", "format": "long_answer", "marks": 10, "bloom_level": "evaluate", "...": "..."}]
    }
  },
  "total_marks": 100
}
```

## Quality Criteria
- 30-40 questions across 3 sections
- Full Bloom range (Remember through Evaluate)
- Mark allocation is explicit for every question
- Section instructions are clear (all required vs choice)
- Questions are answerable under exam conditions (no internet needed)
- Total marks sum to 100 (or specified total)
- External examiner would approve all questions
