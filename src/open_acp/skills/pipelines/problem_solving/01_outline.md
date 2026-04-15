# Stage: Outline Generation — Problem Solving

## Your Role
You are generating the document skeleton for a Problem Solving session. This session teaches learners to solve problems methodically, not just understand concepts.

## What's Different from Concept Explainer
- Sections are organized around **problem categories**, not concept explanations
- Teaching flow follows difficulty progression: warm-up → guided → scaffolded → independent
- Each section centers on a **worked example** with explicit solution strategy
- Time allocation skews toward practice (50-60% vs 40% in concept_explainer)

## Process

### Step 1: Analyze and Categorize Problems
- Identify 3-5 problem categories relevant to the module topic
- Order by difficulty: foundational patterns first, complex variations later
- Map each category to prerequisite knowledge

### Step 2: Design the Problem Progression
Use backward design with a problem-solving lens:
1. Terminal problem — what problem type should the learner solve independently?
2. Identify sub-skills needed (pattern recognition, edge case handling, optimization)
3. Design progression: **warm-up review → worked example → guided practice → independent practice**

Choose a problem-solving pattern:
- **Pattern-first**: Show the pattern → demonstrate → practice variations
- **Struggle-first**: Pose a hard problem → fail → teach the technique → retry
- **Comparison**: Show brute force → show optimized → analyze tradeoffs

### Step 3: Generate Section Outline
Follow `concept_explainer/01_outline` format. For each section also include:
- **problem_type**: The category of problem this section addresses
- **difficulty**: easy / medium / hard
- **worked_example_summary**: One-line description of the worked example

### Step 4: Validate Completeness
Follow `concept_explainer/01_outline` validation, plus:
- Difficulty must progress (no hard problems before medium)
- At least 2 worked examples across the session
- At least 50% of time is allocated to problem-solving activities

## Output Format
Same as `concept_explainer/01_outline` JSON, with additional fields per section:
```json
{
  "sections": [
    {
      "heading": "Section title",
      "purpose": "What this section achieves",
      "estimated_minutes": 15,
      "bloom_level": "apply",
      "problem_type": "array traversal",
      "difficulty": "medium",
      "worked_example_summary": "Find the maximum subarray sum using Kadane's algorithm"
    }
  ],
  "teaching_flow": "...",
  "difficulty_progression": "easy → medium → hard",
  "total_estimated_minutes": 60
}
```

## Quality Criteria
- Difficulty progression is monotonically non-decreasing
- Every problem type has at least one worked example
- Practice time is >= 50% of total session time
- Common mistakes are identified for each problem category
- Multiple solution approaches noted where applicable
