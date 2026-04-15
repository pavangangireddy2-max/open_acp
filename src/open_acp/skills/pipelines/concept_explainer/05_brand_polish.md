# Stage: Brand Polish — Concept Explainer

## Your Role
You are applying brand voice, formatting, and terminology guidelines to the assembled content.

## Prerequisites
- Core content artifact (the raw instructional material)
- Activities artifact (the learning activities)
- Brand playbook (styles/default.yaml) — if available

## Input Artifacts
- `core_content` — instructional material
- `activities` — learning activities

## Process

### Step 1: Load Brand Guidelines
If a brand playbook exists (styles/default.yaml), load it. Key sections to apply:
- **Voice**: tone, perspective, formality, personality traits
- **Formatting**: heading style, code blocks, lists, emphasis
- **Terminology**: preferred terms, terms to avoid, domain glossary
- **Content patterns**: intro pattern, transition phrases, summary pattern, callout types

If no playbook exists, use sensible defaults:
- Semi-formal, encouraging tone
- Second person ("you will learn...")
- Sentence case headings
- Bold for key terms, italic for definitions

### Step 2: Apply Voice Guidelines
- Rewrite sections that don't match the target tone
- Ensure consistent perspective (don't switch between "you" and "the learner")
- Check formality level — not too casual, not too academic
- Add encouraging language where appropriate

### Step 3: Apply Formatting Guidelines
- Standardize heading levels and styles
- Ensure code blocks have language tags
- Standardize list formats
- Apply callout patterns (tip, warning, deep-dive, common-mistake)
- Add transition phrases between sections

### Step 4: Apply Terminology Guidelines
- Replace non-preferred terms with preferred alternatives
- Ensure domain-specific jargon is defined on first use
- Check for consistency — same concept should use the same term throughout

### Step 5: Assemble and Score
- Combine the polished content into a single document
- Score style compliance (0-1) based on how well the result matches guidelines
- Document all changes made (for audit trail)

## Output Format
Return a JSON object matching `brand_polish.schema.json`:
```json
{
  "polished_content": "# Module Title\n\n## Section 1...",
  "changes_made": [
    {"section": "Section 1", "change_type": "tone", "before": "One must consider...", "after": "You should consider..."}
  ],
  "style_compliance_score": 0.85,
  "brand_voice_notes": "Applied semi-formal tone, second person perspective throughout"
}
```

## Quality Criteria
- All changes are documented in changes_made
- No meaning changes — only voice/formatting
- Style compliance score > 0.7
- Consistent terminology throughout
