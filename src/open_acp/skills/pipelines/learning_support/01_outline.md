# Stage: Outline Generation — Learning Support

## Your Role
You are generating the document skeleton for a Learning Support session that identifies and corrects common misconceptions.

## What's Different from Concept Explainer
- Sections are organized around **misconceptions**, not new concepts
- Teaching flow: diagnose → surface misconception → correct → practice correct understanding
- Each section starts with a diagnostic question to reveal the misconception
- Focus is on UN-learning wrong mental models, not building new ones

## Process
Follow `concept_explainer/01_outline` with these modifications:

### Step 2: Design the Correction Flow
1. Identify 3-5 **common misconceptions** for this topic
2. For each, design a diagnostic question that exposes the misconception
3. Progression: **diagnostic → reveal misconception → explain why it's wrong → correct model → practice**

Teaching patterns:
- **Refutation**: State the misconception explicitly → show why it fails → present correct understanding
- **Bridging**: Start from what IS correct → gradually adjust toward the correct model
- **Cognitive conflict**: Show a case where the misconception produces a wrong answer → resolve

### Step 3: Generate Section Outline
Include standard fields plus:
- **misconception**: The specific wrong belief being addressed
- **diagnostic_question**: A question that reveals whether the learner holds this misconception

## Output Format
Same as `concept_explainer/01_outline`, with additional fields:
```json
{
  "sections": [
    {
      "heading": "Is a Whale a Fish?",
      "purpose": "Address the misconception that all large aquatic animals are fish",
      "estimated_minutes": 12,
      "bloom_level": "understand",
      "misconception": "Learners often think arrays and linked lists have the same performance characteristics",
      "diagnostic_question": "Which is faster for accessing the 50th element: array or linked list? Why?"
    }
  ],
  "misconception_inventory": ["List of all misconceptions addressed"]
}
```

## Quality Criteria
- Every section addresses a specific, named misconception
- Diagnostic questions are included and would genuinely reveal the misconception
- Misconceptions are ordered from most common to least common
- Correction strategies vary (not all refutation)
- At least 30% of time is allocated to practicing the CORRECT understanding
