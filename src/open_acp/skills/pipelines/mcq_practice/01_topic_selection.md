# Stage: Topic Selection — MCQ Practice

## Your Role
You are selecting and organizing topics for a set of multiple-choice practice questions, mapping learning objectives to question topics.

## Process

### Step 1: Map Objectives to Question Topics
- Review the module's learning objectives and their Bloom levels
- For each objective, identify 1-3 specific sub-topics that can be tested via MCQ
- Create a topic-to-objective mapping

### Step 2: Plan Bloom Distribution
Target distribution for practice MCQs:
- **Remember**: 20-30% (recall facts, definitions, syntax)
- **Understand**: 30-40% (explain concepts, compare, interpret)
- **Apply**: 20-30% (predict output, trace code, solve simple problems)
- **Analyze**: 10-20% (identify patterns, debug, evaluate trade-offs)

### Step 3: Determine Question Count
- Standard practice set: 10-15 questions
- At least 2 questions per major objective
- Distribute across Bloom levels per the target above

### Step 4: Create the Topic Map
For each planned question, specify:
- Topic area
- Target Bloom level
- Mapped objective(s)
- Expected difficulty (easy/medium/hard)

## Output Format
```json
{
  "topic_map": [
    {
      "question_slot": 1,
      "topic": "List comprehension syntax",
      "bloom_level": "remember",
      "objective_ids": ["obj_1"],
      "difficulty": "easy"
    }
  ],
  "bloom_distribution": {"remember": 3, "understand": 5, "apply": 4, "analyze": 2},
  "total_questions": 14,
  "objectives_coverage": {"obj_1": 3, "obj_2": 4, "obj_3": 3}
}
```

## Quality Criteria
- Every objective is covered by at least 2 questions
- Bloom distribution matches the target (within 10%)
- Topics are specific enough to write a focused question (not "Python basics")
- Difficulty spread: ~30% easy, ~50% medium, ~20% hard
- No topic is over-represented (max 3 questions per narrow topic)
