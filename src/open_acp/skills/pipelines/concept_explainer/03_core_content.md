# Stage: Core Content Generation — Concept Explainer

## Your Role
You are generating the instructional content — the highest quality layer. This is where the actual teaching happens.

## Prerequisites
- Outline artifact (sections, teaching_flow)
- Objectives artifact (objectives)
- Brand playbook (voice, formatting, terminology) — if available
- Wiki entities for relevant skills/concepts — if available

## Input Artifacts
- `outline` — section structure and teaching flow
- `objectives` — measurable objectives with Bloom levels

## Process

### Step 1: Internalize the Teaching Flow
- Re-read the outline's teaching_flow
- For each section, understand its PURPOSE (not just its topic)
- Know which objectives each section serves (from section.objective_ids)
- Honor the section's `teaching_mode`

### Step 2: Generate Content Section by Section
For each section in the outline:

1. **Opening hook** (1-2 sentences): Connect to what the learner already knows or pose an intriguing question
2. **Core explanation**: Clear, progressive explanation of the concept
   - Use analogies before formal definitions
   - Introduce key terms with definitions on first use (bold the term)
   - Build from simple to complex
3. **Concrete examples**: At least 1 per section
   - Use real-world, domain-relevant examples (not toy examples)
   - Show the concept in action, not just described
   - If code is involved, make it runnable (not pseudocode)
4. **Common misconceptions**: Address 1-2 likely mistakes or confusions
5. **Bridge to next section**: 1-2 sentences connecting to what comes next

Teaching-mode adaptations:
- `motivation`: lead with relevance, stakes, and curiosity
- `prior_knowledge_bridge`: explicitly connect to what learners already know
- `concept_explain`: prioritize clarity, definitions, and mental models
- `worked_example`: walk through one example slowly and explain every move
- `guided_practice`: shift from explanation to learner action with scaffolding
- `reflection_summary`: synthesize the big ideas and transfer guidance

### Step 3: Apply Quality Standards
- **Accuracy**: Every factual claim must be correct. Cite sources for non-obvious facts.
- **Clarity**: Use short sentences. One idea per paragraph. Active voice.
- **Engagement**: Vary structure — don't make every section feel the same.
- **Depth**: Match the Bloom level — "understand" sections explain why, "apply" sections show how.
- **Cognitive load**: No more than 3-4 new concepts per section. Space them with examples.

### Step 4: Add Metadata
- Count words per section and total
- Estimate reading time (assume 200 words/minute for technical content)
- List key terms introduced
- Note any citations used

## Output Format
Return a JSON object matching `core_content.schema.json`:
```json
{
  "sections": [
    {
      "heading": "What is Binary Search?",
      "teaching_mode": "concept_explain",
      "objective_ids": ["obj_1"],
      "content_markdown": "## What is Binary Search?\n\nImagine you're looking for...",
      "key_terms": ["binary search", "sorted array", "time complexity"],
      "examples": [
        {"title": "Finding a word in a dictionary", "content": "When you open a dictionary..."}
      ],
      "misconceptions": ["Binary search does not work on unsorted collections"],
      "bridge_to_next": "Now that the learner understands the idea, the next section shows a concrete walkthrough.",
      "citations": ["Cormen et al., Introduction to Algorithms, Ch. 2"]
    }
  ],
  "word_count": 2500,
  "reading_time_minutes": 12.5
}
```

## Quality Criteria
- Minimum 500 words per section
- At least 1 concrete example per section
- Key terms bolded on first use
- No jargon without definition
- Active voice preferred (passive < 20% of sentences)
- Every section serves at least one objective from the outline's `objective_ids`
- The content behavior should clearly match the declared `teaching_mode`
