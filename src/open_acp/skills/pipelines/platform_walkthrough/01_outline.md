# Stage: Outline Generation — Platform Walkthrough

## Your Role
You are generating the document skeleton for a Platform Walkthrough session that teaches learners to navigate and use a specific tool or platform.

## What's Different from Concept Explainer
- Sections map to **user workflows**, not concepts
- Teaching flow follows task-based learning: feature inventory → core workflow → advanced features → troubleshooting
- Each section produces a specific platform action the learner can replicate
- Heavy emphasis on step-by-step instructions and visual references

## Process
Follow `concept_explainer/01_outline` with these modifications:

### Step 2: Design the Walkthrough Flow
1. Create a **feature inventory** — list all platform features relevant to this module
2. Map features to **user workflows** (what tasks will learners need to do?)
3. Order by frequency of use: most common workflows first
4. Progression: **orientation → core workflow → supporting features → tips/shortcuts → troubleshooting**

Teaching patterns:
- **Task-based**: Organize around "how to do X" tasks
- **Exploration-based**: Guided tour of the interface, then practice
- **Scenario-based**: "You need to do X, here's how" realistic scenarios

### Step 3: Generate Section Outline
Include standard fields plus:
- **platform_feature**: Which platform feature/area this covers
- **user_task**: The task the learner will accomplish
- **screenshots_needed**: Number of screenshots/visuals expected

## Output Format
Same as `concept_explainer/01_outline`, with additional fields:
```json
{
  "sections": [
    {
      "heading": "Setting Up Your Workspace",
      "purpose": "Learner configures their IDE workspace for the course",
      "estimated_minutes": 10,
      "bloom_level": "apply",
      "platform_feature": "VS Code workspace settings",
      "user_task": "Create and configure a workspace with required extensions",
      "screenshots_needed": 4
    }
  ],
  "feature_inventory": ["List of all platform features covered"],
  "prerequisite_setup": "What must be installed/configured before the session"
}
```

## Quality Criteria
- Every section results in a completed platform action (not just understanding)
- Screenshots/visual references are planned for every section
- Troubleshooting section is included (what to do when things go wrong)
- Prerequisite setup is explicit (what to install before the session)
- Workflows are ordered by real-world usage frequency
