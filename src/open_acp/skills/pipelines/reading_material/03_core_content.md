# Stage: Core Content Generation — Reading Material

## Your Role
You are generating long-form tutorial content optimized for self-paced reading.

## What's Different from Session Pipelines
- **Tutorial style**: conversational but thorough, like a well-written blog post or textbook chapter
- Code blocks are embedded with line-by-line explanations
- Diagram descriptions replace live demonstrations
- "Check your understanding" prompts replace instructor questions
- Content must stand alone — no "as we discussed in class"

## Process
Follow `concept_explainer/03_core_content` with these modifications:

### Step 2: Generate Content Section by Section
For each section:

1. **Opening** (2-3 sentences): Connect to previous section or pose a motivating question
2. **Explanatory prose**: Clear, progressive explanation
   - More detailed than session content (reader can't ask questions)
   - Use analogies and visual language to compensate for lack of instructor
   - Define every term inline (no glossary dependency)
3. **Code blocks with explanation**:
   - Use fenced code blocks with language tags (```python)
   - Follow each code block with a line-by-line explanation
   - Include expected output in a separate code block
   - Mark important lines with comments: `# <-- This is the key line`
4. **Diagram descriptions**: Where a diagram would help, describe it in a callout:
   - `[Diagram: description of what the diagram shows and key relationships]`
5. **"Check your understanding"**: 1-2 reflective questions per major section
   - Not graded, just prompts for self-reflection
   - Include the answer in a collapsed/spoiler section
6. **Transition**: 1-2 sentences bridging to the next section

### Writing Standards
- Sentences average 15-20 words (readable)
- Paragraphs are 3-5 sentences max
- Use subheadings liberally (every 200-300 words)
- Bold key terms, use italic for emphasis

## Output Format
Same as `concept_explainer/03_core_content`, with additional fields:
```json
{
  "sections": [
    {
      "heading": "Understanding Recursion",
      "content_markdown": "...",
      "key_terms": ["recursion", "base case", "call stack"],
      "code_blocks": [{"language": "python", "description": "Factorial function"}],
      "diagram_descriptions": ["Call stack for factorial(4)"],
      "check_your_understanding": [
        {"question": "What happens if you remove the base case?", "answer": "Infinite recursion..."}
      ]
    }
  ],
  "word_count": 3200,
  "reading_time_minutes": 16
}
```

## Quality Criteria
- Word count is 2,000-5,000
- Every code block has a following explanation
- At least 1 "check your understanding" per major section
- No references to instructor, class, or session (fully self-contained)
- Diagram descriptions are specific enough for a designer to create
- Reading flow is smooth (no abrupt topic jumps)
