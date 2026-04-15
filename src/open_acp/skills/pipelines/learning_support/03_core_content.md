# Stage: Core Content Generation — Learning Support

## Your Role
You are generating content that surfaces, addresses, and corrects common misconceptions.

## What's Different from Concept Explainer
- Content structure: misconception → why it's wrong → correct understanding → practice
- Side-by-side comparisons are the primary teaching tool
- "Wrong" examples are shown deliberately and explicitly labeled
- Tone must be non-judgmental (these are common mistakes, not stupid mistakes)

## Process
Follow `concept_explainer/03_core_content` with these modifications:

### Step 2: Generate Content Section by Section
For each misconception section:

1. **Diagnostic question** (the question from the outline, posed to the reader)
2. **The misconception stated clearly**: "Many learners believe that..."
3. **Why it seems reasonable**: Validate WHY someone would think this (build empathy)
4. **The counter-example**: A concrete case where the misconception produces a wrong answer
5. **The correct understanding**: Clear explanation of what's actually true
6. **Side-by-side comparison**:
   - Two-column format: Misconception vs Reality
   - Include code examples if applicable (wrong code vs correct code)
7. **Practice the correct model**: A quick exercise applying the correct understanding

### Tone Standards
- Never say "wrong" about the learner — say "a common misconception" or "an easy mistake"
- Validate the reasoning: "It's natural to think X because..."
- Be direct about the correction: "However, the actual behavior is..."

## Output Format
Same as `concept_explainer/03_core_content`, with additional fields:
```json
{
  "sections": [
    {
      "heading": "Misconception: Strings are Modified In-Place",
      "content_markdown": "...",
      "misconception": "Strings are mutable in Python",
      "correct_understanding": "Strings are immutable; operations create new string objects",
      "comparison_table": {"misconception_column": "...", "reality_column": "..."}
    }
  ]
}
```

## Quality Criteria
- Every section has an explicit side-by-side comparison (wrong vs right)
- Counter-examples are concrete and runnable where possible
- Tone is consistently non-judgmental
- "Why it seems reasonable" is included for every misconception (builds trust)
- Practice exercises specifically test the corrected understanding
