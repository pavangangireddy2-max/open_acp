# Stage: Rubric Design — Classroom Quiz

## Your Role
You are creating a scoring rubric for the classroom quiz, including partial credit rules.

## Process

### Step 1: Assign Points Per Question
- MCQ: 1 point each (correct or incorrect, no partial credit)
- True/False with explanation: 2 points (1 for correct T/F, 1 for valid explanation)
- Short answer: 2 points (rubric below)

### Step 2: Define Scoring Criteria
**For MCQ**: Binary — correct = full points, incorrect = 0

**For True/False + Explain**:
- 2 points: Correct answer + correct explanation
- 1 point: Correct answer + weak/incomplete explanation, OR incorrect answer + reasoning that shows partial understanding
- 0 points: Incorrect answer + no meaningful explanation

**For Short Answer**:
- 2 points: Complete, accurate answer using correct terminology
- 1 point: Partially correct or uses imprecise language but shows understanding
- 0 points: Incorrect or irrelevant answer

### Step 3: Create Answer Key
For each question, provide:
- The correct answer
- A model response (for short answer / T-F explain)
- Key terms that MUST appear for full credit
- Common partial-credit responses and their scores

## Output Format
```json
{
  "rubric": {
    "total_points": 10,
    "passing_threshold": 6,
    "questions": [
      {
        "question_id": "q_1",
        "max_points": 1,
        "scoring": "binary",
        "correct_answer": "B",
        "key_terms": []
      },
      {
        "question_id": "q_2",
        "max_points": 2,
        "scoring": "partial_credit",
        "correct_answer": "False",
        "model_response": "False. Binary search requires the array to be sorted because...",
        "key_terms": ["sorted", "divide in half"],
        "partial_credit_examples": [
          {"response_pattern": "False but no explanation", "points": 1}
        ]
      }
    ]
  }
}
```

## Quality Criteria
- Every question has explicit scoring criteria
- Partial credit rules are clear and consistent
- Key terms for full credit are identified
- Model responses are provided for non-MCQ questions
- Total points and passing threshold are defined
