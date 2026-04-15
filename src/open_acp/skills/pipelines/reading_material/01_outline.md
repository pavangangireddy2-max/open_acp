# Stage: Outline Generation — Reading Material

## Your Role
You are generating the document skeleton for a Reading Material artifact — a long-form written tutorial, not a session.

## What's Different from Session Pipelines
- **No slides, no activities** — this is standalone reading content
- Longer form: 2,000-5,000 words (vs 1,500-2,500 for sessions)
- Must be self-contained (no instructor to clarify)
- Optimized for reading flow: table of contents, clear headings, progressive depth

## Process
Follow `concept_explainer/01_outline` with these modifications:

### Step 2: Design the Reading Flow
Reading materials need excellent flow because there's no instructor. Design for:
1. **Hook** — why should the reader care? (first 2 paragraphs must earn continued reading)
2. **Foundations** — what they need to know first
3. **Core content** — progressive depth, with embedded code and diagrams
4. **Application** — worked examples showing the concept in action
5. **Summary** — key takeaways, further reading links

### Step 3: Generate Section Outline
Include standard fields plus:
- **word_count_target**: Expected words for this section
- **code_blocks_expected**: Number of code examples planned
- **diagram_descriptions**: Diagrams needed (described for later creation)

### Step 4: Validate Completeness
Follow `concept_explainer/01_outline` validation, plus:
- Total word count target is 2,000-5,000
- Reading time estimate is 10-25 minutes
- Self-contained: no references to "as the instructor will explain"
- Table of contents is implied by the section structure

## Output Format
Same as `concept_explainer/01_outline`, with additional fields:
```json
{
  "sections": [
    {
      "heading": "Introduction to Recursion",
      "purpose": "Motivate why recursion matters",
      "word_count_target": 400,
      "code_blocks_expected": 1,
      "diagram_descriptions": ["Call stack visualization for factorial(4)"]
    }
  ],
  "total_word_count_target": 3000,
  "estimated_reading_minutes": 15
}
```

## Quality Criteria
- Self-contained: understandable without an instructor
- Progressive depth (don't front-load all complexity)
- Code examples planned for every technical section
- Diagram descriptions are specific enough to create
- Reading time is 10-25 minutes (not too short, not overwhelming)
