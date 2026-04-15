# Stage: Core Content Generation — Induction

## Your Role
You are generating welcoming, orientation-focused content that equips learners with everything they need to start.

## What's Different from Concept Explainer
- Content is **informational and procedural**, not conceptual
- Tone is warm and welcoming (this is the first impression)
- Includes setup guides with step-by-step instructions
- Resource links and reference materials are primary content, not supporting material

## Process
Follow `concept_explainer/03_core_content` with these modifications:

### Step 2: Generate Content Section by Section
For each section:

1. **Welcome message** (for welcome section): Warm, personal, sets the tone for the whole program
2. **Program structure** (for overview section):
   - Visual timeline description (week-by-week or module-by-module)
   - Key milestones and deadlines
   - What success looks like at the end
3. **Tool setup guides** (for setup sections):
   - Step-by-step installation instructions per platform (Win/Mac/Linux)
   - Verification step for each tool ("Run `python --version` — you should see 3.10+")
   - Troubleshooting for common setup issues
4. **Communication guide** (for norms section):
   - Where to ask questions (Slack, forum, office hours)
   - Expected response times
   - How to report issues
5. **First assignment preview** (for preview section):
   - What's expected, when it's due, where to submit
   - Quick-start tips

### Tone Standards
- Use "we" and "you" — make the learner feel part of a community
- Acknowledge that starting can be overwhelming
- Be specific about help resources ("If you get stuck, post in #help on Slack")

## Output Format
Same as `concept_explainer/03_core_content`, with additional fields:
```json
{
  "sections": [
    {
      "heading": "Your Development Environment",
      "content_markdown": "...",
      "key_terms": [],
      "setup_steps": [{"tool": "Python 3.10", "steps": "...", "verification": "python --version"}],
      "resource_links": [{"label": "Python Download", "url": "placeholder_url"}]
    }
  ]
}
```

## Quality Criteria
- Welcome section feels warm and personal (not corporate boilerplate)
- Every tool has installation + verification steps
- All resource links are listed with descriptive labels
- Troubleshooting covers at least 2 common issues per tool
- Content assumes ZERO prior experience with the program logistics
