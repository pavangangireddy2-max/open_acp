# Stage: Format Output — Summary Cheatsheet

## Your Role
You are formatting the cheatsheet into its final deliverable: a quick-reference Markdown document optimized for scanning.

## Process

### Step 1: Apply Quick-Reference Layout
```markdown
# [Topic] Cheatsheet

> **Covers**: [list of topics] | **Last updated**: [date]

---

## [Category 1]

| Column1 | Column2 | Column3 |
|---------|---------|---------|
| ...     | ...     | ...     |

## [Category 2]

- **Term**: Definition in one sentence. Example: `code`.

...

## Common Mistakes

| Mistake | Why | Fix |
|---------|-----|-----|
| ...     | ... | ... |

---
*Quick reference for [course/module name]*
```

### Step 2: Optimize for Two-Column Printing
- Keep sections independent (no section spans a column break awkwardly)
- Use horizontal rules (---) between major sections
- Tables should fit within half a page width (3-4 columns max)
- Consider landscape orientation for wide tables

### Step 3: Add Visual Hierarchy
- H1 for the cheatsheet title only
- H2 for each category
- Bold for every concept name/term
- Code backticks for all syntax, function names, commands
- Horizontal rules between categories

### Step 4: Metadata Footer
- Include "Covers: [topics]" at the top
- Include course/module reference at the bottom
- Optionally include version/date

## Output Format
```json
{
  "formatted_markdown": "# Python Strings Cheatsheet\n\n> Covers: ...\n\n---\n...",
  "metadata": {
    "title": "...",
    "word_count": 900,
    "categories_count": 5,
    "items_count": 35,
    "common_mistakes_count": 6
  },
  "print_layout_notes": "Optimized for A4 landscape, two-column layout"
}
```

## Quality Criteria
- Renders correctly in standard Markdown viewers
- Fits on 1-3 printed pages (landscape, two-column)
- Visual hierarchy is clear (H1 > H2 > bold > code)
- All tables have consistent formatting
- Horizontal rules separate categories
- Metadata header and footer are present
