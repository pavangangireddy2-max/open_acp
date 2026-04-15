# Stage: Core Content Generation — Summary Cheatsheet

## Your Role
You are generating ultra-concise reference content. Tables, bullet points, code snippets, and formulas — NOT prose.

## What's Different from Other Pipelines
- NO PROSE PARAGRAPHS. Every piece of content is a table row, bullet point, code snippet, or formula.
- Each concept gets a maximum of 3 sentences
- Code examples are minimal (5 lines or less per snippet)
- Focus on WHAT and HOW, not WHY (that's in the reading material)

## Process

### Step 1: Generate Content by Layout Type

**Table sections**:
```markdown
| Method | Syntax | Description | Example |
|--------|--------|-------------|---------|
| split  | `str.split(sep)` | Splits string by separator | `"a,b".split(",")` → `["a","b"]` |
```

**Bullet list sections**:
```markdown
- **Recursion**: A function that calls itself. Requires a base case to terminate. Time complexity depends on branching factor.
```

**Code snippet gallery**:
```markdown
### List Comprehension
```python
[x**2 for x in range(10) if x % 2 == 0]
# Output: [0, 4, 16, 36, 64]
```
One-line: Filter and transform a list in a single expression.
```

**Formula/rule cards**:
```markdown
**Big-O Rule**: Drop constants and lower-order terms. O(2n + n^2) → O(n^2)
```

### Step 2: Add Common Mistakes Section
A dedicated section at the end:
```markdown
## Common Mistakes
| Mistake | Why It's Wrong | Correct Approach |
|---------|---------------|-----------------|
| Using `==` for float comparison | Floating point precision | Use `math.isclose()` |
```

### Step 3: Ensure Scannability
- Bold the concept name in every entry
- Use consistent formatting within each section
- Alphabetical or frequency ordering within categories
- No entry exceeds 3 sentences

## Output Format
```json
{
  "sections": [
    {
      "heading": "String Methods",
      "layout_type": "table",
      "content_markdown": "| Method | Syntax | ... |",
      "items_count": 8
    }
  ],
  "common_mistakes": [
    {"mistake": "...", "why_wrong": "...", "correct": "..."}
  ],
  "total_word_count": 900
}
```

## Quality Criteria
- No entry exceeds 3 sentences
- No prose paragraphs (only tables, bullets, code snippets, formulas)
- Code snippets are 5 lines or less
- Common mistakes section is present with at least 5 entries
- Total word count is 500-1,500
- Every entry is self-contained (no "see above" references)
