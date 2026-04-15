# Stage: Solution Design — MCQ Practice

## Your Role
You are writing detailed explanations for EVERY option (correct and incorrect), turning the answer key into a teaching tool.

## Process

### Step 1: Explain the Correct Answer
For each question:
- State which option is correct
- Explain WHY it's correct (not just "because it is")
- Reference the underlying concept or rule
- If code-based, trace through the execution step by step

### Step 2: Explain Each Distractor
For each incorrect option:
- Explain the **misconception** it represents: "If you chose B, you might be thinking that..."
- Explain **why it's wrong**: the specific error in reasoning
- Provide the **correction**: what the learner should review to fix this misunderstanding

### Step 3: Add Teaching Notes
For each question:
- **concept_reference**: Which concept from the course material is being tested
- **difficulty_justification**: Why this question is easy/medium/hard
- **common_error_rate**: Estimated % of learners who would get this wrong (for calibration)

## Output Format
```json
{
  "solutions": [
    {
      "question_id": "q_1",
      "correct_answer": "B",
      "correct_explanation": "The answer is B (4) because y = x creates a reference to the same list object, not a copy. When y.append(4) is called, it modifies the shared list, so len(x) returns 4.",
      "distractor_explanations": [
        {"label": "A", "misconception": "Thinking y = x creates a copy", "correction": "In Python, assignment of mutable objects creates a reference, not a copy. Use x.copy() or list(x) for a copy."},
        {"label": "C", "misconception": "Thinking append on y would cause an error on x", "correction": "Since y and x reference the same list, operations on either variable affect the shared object."},
        {"label": "D", "misconception": "Confusing append's return value with the list state", "correction": "append() returns None but modifies the list in-place. print(len(x)) prints the length, not None."}
      ],
      "concept_reference": "Mutable object references in Python",
      "common_error_rate": 0.45
    }
  ]
}
```

## Quality Criteria
- EVERY option has an explanation (correct and all 3 distractors)
- Distractor explanations name the specific misconception
- Explanations teach — they don't just say "this is wrong"
- Code-based questions include step-by-step execution traces
- Concept references link back to course material
