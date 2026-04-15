# Stage: Core Content Generation — Problem Solving

## Your Role
You are generating instructional content centered on step-by-step problem solving, not concept explanation.

## What's Different from Concept Explainer
- Content is structured around **worked examples** and **solution walkthroughs**
- Each section teaches a problem-solving STRATEGY, not just a concept
- Multiple approaches are shown and compared (brute force vs optimal)
- Common mistakes and debugging guidance are first-class content, not afterthoughts

## Process
Follow `concept_explainer/03_core_content` with these modifications:

### Step 2: Generate Content Section by Section
For each section:

1. **Problem statement** (clear, complete, with constraints and examples)
2. **Intuition building** (2-3 sentences: why is this hard? what pattern applies?)
3. **Solution walkthrough**:
   - Approach 1 (often brute force): explain, show code, analyze complexity
   - Approach 2 (optimized): explain the insight, show code, analyze complexity
   - Compare approaches in a table (time/space complexity, readability, when to use each)
4. **Common mistakes** (2-3 specific errors learners make, with explanations):
   - Off-by-one errors, wrong boundary conditions, forgetting edge cases
   - Show the WRONG code and explain WHY it fails
5. **Variation hints**: Brief mention of how this pattern applies to related problems

### Code Standards
- All code must be **runnable** (not pseudocode)
- Include comments marking key steps in the solution
- Show input/output examples inline
- Use consistent variable naming across all examples in the session

## Output Format
Same as `concept_explainer/03_core_content`, with additional per-section fields:
```json
{
  "sections": [
    {
      "heading": "Two-Pointer Technique",
      "content_markdown": "...",
      "key_terms": ["two-pointer", "sorted array"],
      "approaches": [
        {"name": "Brute Force", "time_complexity": "O(n^2)", "space_complexity": "O(1)"},
        {"name": "Two Pointer", "time_complexity": "O(n)", "space_complexity": "O(1)"}
      ],
      "common_mistakes": ["Forgetting to handle duplicate elements", "Off-by-one on pointer boundaries"]
    }
  ]
}
```

## Quality Criteria
- Every section has at least one complete, runnable code solution
- At least one section compares multiple approaches with complexity analysis
- Common mistakes include the wrong code AND explanation of the bug
- Edge cases are explicitly listed and handled in solutions
- Solution walkthroughs show the THINKING process, not just the final code
