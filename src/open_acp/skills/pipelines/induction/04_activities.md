# Stage: Activities Design — Induction

## Your Role
You are designing onboarding activities: tool setup, introductions, and first-step tasks.

## What's Different from Concept Explainer
- Activities are **setup checklists** and **community-building exercises**, not learning exercises
- "Introduce yourself" activity builds community
- Tool setup is a guided checklist with verification
- First assignment preview gives learners a low-stakes win

## Process
Follow `concept_explainer/04_activities` with these modifications:

### Step 2: Design Onboarding Activities

**Tool setup checklist**:
- Checklist format with verification for each tool
- Pair learners to help each other troubleshoot
- Include a "health check" script that verifies the full setup

**"Introduce yourself" exercise**:
- Template: name, background, one interesting fact, what you hope to learn
- Post in the designated channel (Slack, forum)
- Optional: short verbal introduction in session

**First assignment preview**:
- Walk through the first assignment together
- Identify one small step learners can complete today
- Set up submission workflow (commit, push, submit link)

**Resource scavenger hunt**:
- "Find the syllabus," "locate the Slack help channel," "find office hours schedule"
- Ensures learners know where everything is

## Output Format
Same as `concept_explainer/04_activities`, with additional fields:
```json
{
  "activities": [
    {
      "type": "setup_checklist",
      "title": "Development Environment Setup",
      "checklist": ["Install Python 3.10+", "Install VS Code", "Install Git", "Run health_check.py"],
      "instructions": "...",
      "time_minutes": 20,
      "bloom_level": "apply",
      "objective_ids": ["obj_1"]
    }
  ]
}
```

## Quality Criteria
- Tool setup checklist covers ALL required tools
- At least one community-building activity
- At least one activity gives learners a tangible first win
- Activities don't require domain knowledge (no "solve a problem" tasks)
- Total activity time is 40-50% of session (rest is presentation/discussion)
