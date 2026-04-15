# Stage: Core Content Generation — Platform Walkthrough

## Your Role
You are generating step-by-step platform instruction content with screenshot references and troubleshooting guidance.

## What's Different from Concept Explainer
- Content is **procedural** (numbered steps), not explanatory prose
- Every section includes screenshot/visual placeholders
- Keyboard shortcuts and quick tips are called out prominently
- Common errors and their fixes are included inline (not as an afterthought)

## Process
Follow `concept_explainer/03_core_content` with these modifications:

### Step 2: Generate Content Section by Section
For each section:

1. **Goal statement** (what the learner will have done by end of this section)
2. **Step-by-step instructions**:
   - Numbered steps with specific UI paths: "Click File > Preferences > Settings"
   - Screenshot placeholder after each significant step: `[Screenshot: settings panel with Python extension highlighted]`
   - Bold the exact text/buttons to click
   - Include keyboard shortcuts in parentheses: **Save** (Ctrl+S / Cmd+S)
3. **Tips and shortcuts**: Callout box with power-user tips
4. **Common errors and fixes**:
   - "If you see [error], try [fix]"
   - Platform-specific gotchas (Windows vs Mac vs Linux differences)
5. **Verification**: How to confirm the step worked ("You should see...")

### Formatting Standards
- Use numbered lists for procedural steps (not bullets)
- Bold all UI element names and button labels
- Use code blocks for terminal commands
- Screenshot placeholders are descriptive: `[Screenshot: description of what should be visible]`

## Output Format
Same as `concept_explainer/03_core_content`, with additional fields:
```json
{
  "sections": [
    {
      "heading": "Installing the Python Extension",
      "content_markdown": "...",
      "key_terms": ["extension marketplace", "interpreter"],
      "screenshot_placeholders": ["Extensions sidebar with search bar", "Python extension install button"],
      "keyboard_shortcuts": ["Ctrl+Shift+X: Open extensions", "Ctrl+Shift+P: Command palette"],
      "common_errors": [{"error": "Python not found", "fix": "Install Python and restart VS Code"}]
    }
  ]
}
```

## Quality Criteria
- Every multi-step procedure uses numbered lists
- Screenshot placeholders are included for every significant UI interaction
- Keyboard shortcuts are provided for all mentioned actions
- Common errors section covers at least 2 issues per section
- Platform differences (Win/Mac/Linux) are noted where relevant
