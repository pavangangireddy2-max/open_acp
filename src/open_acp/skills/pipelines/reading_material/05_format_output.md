# Stage: Format Output — Reading Material

## Your Role
You are formatting the polished reading material into its final deliverable form: a well-structured Markdown document.

## What's Different from Session Pipelines
This stage replaces the slide deck stage. The output is a **formatted Markdown document** ready for publishing on a learning platform.

## Process

### Step 1: Generate Table of Contents
- Auto-generate from section headings (H2 and H3 levels)
- Include anchor links for navigation
- Place immediately after the title and introduction paragraph

### Step 2: Apply Document Structure
```markdown
# [Title]

> **Reading time**: X minutes | **Prerequisites**: [list] | **Bloom levels**: [range]

## Table of Contents
- [Section 1](#section-1)
- [Section 2](#section-2)
...

## Section 1: [Heading]
[Content]

### Subsection 1.1
[Content]

> **Check your understanding**: [Question]
> <details><summary>Answer</summary>[Answer]</details>

...

## Key Takeaways
- Takeaway 1
- Takeaway 2
- Takeaway 3

## Further Reading
- [Resource 1](url) — description
- [Resource 2](url) — description
```

### Step 3: Format Code Blocks
- Every code block has a language tag: ```python, ```javascript, etc.
- Output blocks use: ```output or ```text
- Long code blocks (20+ lines) get a descriptive comment header
- Inline code uses backticks for function names, variable names, commands

### Step 4: Add Key Takeaways Section
- 3-5 bullet points summarizing the most important concepts
- Each takeaway is one sentence, actionable where possible
- Place at the end, before "Further Reading"

### Step 5: Add Further Reading
- 2-4 curated resources for deeper exploration
- Include brief description of each (not just a link)

## Output Format
```json
{
  "formatted_markdown": "# Title\n\n> Reading time: ...\n\n## Table of Contents\n...",
  "metadata": {
    "title": "...",
    "reading_time_minutes": 16,
    "word_count": 3200,
    "key_terms": ["term1", "term2"],
    "bloom_levels": ["understand", "apply"],
    "prerequisites": ["prerequisite1"]
  }
}
```

## Quality Criteria
- Table of contents with working anchor links
- All code blocks have language tags
- Key takeaways section is present (3-5 bullets)
- Further reading section is present (2-4 resources)
- Document renders correctly in standard Markdown viewers
- Metadata is complete and accurate
