# Stage: Question Generation — Classroom Quiz

## Your Role
You are writing 5-8 quiz questions for a short formative assessment. Questions should be quick to answer and focused on checking basic understanding.

## What's Different from MCQ Practice
- Questions are simpler (formative, not practice)
- Mix of formats: MCQ, true/false with justification, short answer (1-2 sentences)
- Questions should take 2-3 minutes each, max
- Focus on "do you understand the basics?" not "can you solve hard problems?"

## Process
Follow `mcq_practice/02_question_generation` with these modifications:

### Format Mix
- 3-4 MCQ questions (4 options each, follow mcq_practice rules)
- 1-2 True/False with "explain why" (tests understanding, not guessing)
- 1-2 Short answer (define a term, explain a concept in 1-2 sentences)

### Difficulty Calibration
- All questions should be answerable by someone who paid attention in the session
- No trick questions or edge cases
- Code questions (if any) should be 3-5 lines max

## Output Format
```json
{
  "questions": [
    {
      "id": "q_1",
      "format": "mcq",
      "stem": "What is the time complexity of binary search?",
      "options": [{"label": "A", "text": "O(n)"}, {"label": "B", "text": "O(log n)"}, {"label": "C", "text": "O(n^2)"}, {"label": "D", "text": "O(1)"}],
      "correct_answer": "B",
      "bloom_level": "remember",
      "points": 1
    },
    {
      "id": "q_2",
      "format": "true_false",
      "stem": "Binary search works on unsorted arrays. True or False? Explain.",
      "correct_answer": "False",
      "explanation_required": true,
      "bloom_level": "understand",
      "points": 2
    }
  ]
}
```

## Quality Criteria
- 5-8 questions total
- Mix of at least 2 formats
- No question takes more than 3 minutes
- Questions test basic understanding (not advanced application)
- Every question is clearly worded and unambiguous
