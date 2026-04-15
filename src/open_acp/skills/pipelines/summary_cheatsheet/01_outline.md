# Stage: Outline Generation — Summary Cheatsheet

## Your Role
You are generating the skeleton for a Summary Cheatsheet — a concise quick-reference document.

## What's Different from Other Written Pipelines
- CONCISE is the mandate: each concept in 3 sentences or less
- Structure is **reference-oriented** (lookup, not linear reading)
- Organized by topic/category, not by teaching flow
- Target length: 500-1,500 words (vs 2,000-5,000 for reading material)

## Process

### Step 1: Identify Topics to Summarize
- List all concepts, techniques, and terms that need to be in the cheatsheet
- Group into 4-8 logical categories
- Prioritize by frequency of reference (most-used concepts first)

### Step 2: Design the Reference Layout
Choose a layout per category:
- **Table format**: For comparisons (e.g., method name | syntax | description | example)
- **Bullet list**: For concept summaries (term: 1-2 sentence definition)
- **Code snippet gallery**: For syntax references (code block + one-line explanation)
- **Formula/rule cards**: For mathematical or logical rules

### Step 3: Generate Section Outline
For each category:
- **heading**: Category name
- **layout_type**: table / bullets / code_gallery / formula_cards
- **items_count**: Number of items in this category
- **estimated_lines**: Line count for this section

## Output Format
```json
{
  "sections": [
    {
      "heading": "String Methods",
      "layout_type": "table",
      "items_count": 8,
      "estimated_lines": 20,
      "items_preview": ["split()", "join()", "strip()", "replace()"]
    }
  ],
  "total_estimated_lines": 150,
  "target_word_count": 800,
  "common_mistakes_section": true
}
```

## Quality Criteria
- Total word count target is 500-1,500 (it's a CHEATSHEET, not a textbook)
- Every item can be understood in a glance (3 sentences max per item)
- Layout types are chosen for scannability (tables for comparisons, bullets for lists)
- Common mistakes section is planned
- Items are ordered by usage frequency within each category
