# Stage: Activities Design — Problem Solving

## Your Role
You are designing problem-solving activities with progressive difficulty and hint systems.

## What's Different from Concept Explainer
- Activities follow a **guided → scaffolded → independent** progression
- Each activity includes a **hint system** (3 levels of hints before solution)
- Activities are primarily coding/problem-solving exercises, not discussions
- Time allocation is higher (50-60% of session)

## Process
Follow `concept_explainer/04_activities` with these modifications:

### Step 2: Design Activities with Progressive Scaffolding

**Guided practice** (first activity per problem type):
- Full problem statement + pseudocode outline provided
- Learner fills in key logic steps
- Hints available immediately

**Scaffolded practice** (middle):
- Full problem statement + starter code with key function signatures
- Learner implements the solution
- 3-tier hint system: (1) conceptual hint, (2) approach hint, (3) partial code

**Independent practice** (final):
- Problem statement only, no starter code
- Learner designs and implements from scratch
- Hints available but discouraged

### Step 3: Design the Hint System
For each activity, provide 3 hint levels:
- **Hint 1** (conceptual): "Think about what data structure would help here..."
- **Hint 2** (approach): "Try using a hash map to store seen elements..."
- **Hint 3** (partial code): "Initialize a dictionary, then for each element..."

## Output Format
Same as `concept_explainer/04_activities`, with additional fields:
```json
{
  "activities": [
    {
      "type": "exercise",
      "title": "Find Two Sum",
      "scaffolding_level": "scaffolded",
      "instructions": "...",
      "starter_code": "def two_sum(nums, target):\n    # Your code here",
      "hints": ["Think about lookup time...", "Use a hash map...", "for i, num in enumerate(nums): complement = ..."],
      "expected_output": "...",
      "time_minutes": 15,
      "bloom_level": "apply",
      "objective_ids": ["obj_2"]
    }
  ]
}
```

## Quality Criteria
- At least 3 activities spanning guided → scaffolded → independent
- Every activity has a 3-tier hint system
- Activities cover the same problem types as the core content
- Independent activities are solvable with the techniques taught (no surprise difficulty)
- Total activity time is 50-60% of session
