# Stage: Core Content Generation — Project Building

## Your Role
You are generating instructional content structured as a project build guide with code walkthroughs.

## What's Different from Concept Explainer
- Content follows the **spec → architecture → build → integrate** flow
- Each section is a build guide with runnable code, not a concept explanation
- Code walkthroughs show the building process incrementally (not just final state)
- Architecture decisions are explained with trade-off analysis

## Process
Follow `concept_explainer/03_core_content` with these modifications:

### Step 2: Generate Content Section by Section
For each section:

1. **Goal statement** (what this milestone achieves, 1-2 sentences)
2. **Architecture context** (where this component fits in the overall system)
3. **Step-by-step build guide**:
   - File/folder structure needed
   - Code with inline comments explaining design decisions
   - Show the code INCREMENTALLY (version 1 → add feature → version 2)
   - Test/verify step after each significant addition
4. **Integration points**: How this connects to previous and next milestones
5. **Design decisions**: Why this approach vs alternatives (brief trade-off table)

### Code Standards
- All code must be **copy-paste runnable** in sequence
- Include setup commands (pip install, mkdir, etc.)
- Show expected output after each runnable step
- Use consistent project structure across all sections

## Output Format
Same as `concept_explainer/03_core_content`, with additional fields:
```json
{
  "sections": [
    {
      "heading": "Milestone 1: Project Skeleton",
      "content_markdown": "...",
      "key_terms": ["flask", "virtual environment"],
      "files_created": ["app.py", "requirements.txt", "tests/test_app.py"],
      "setup_commands": ["pip install flask", "mkdir -p tests"],
      "verification_step": "Run `python app.py` and visit localhost:5000/health"
    }
  ]
}
```

## Quality Criteria
- Every section produces code that runs when copy-pasted in sequence
- Setup commands are explicit (no assumed tooling)
- Each milestone has a verification step (how to know it works)
- Architecture decisions include brief trade-off reasoning
- File structure is consistent across all sections
