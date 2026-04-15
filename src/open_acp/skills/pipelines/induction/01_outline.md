# Stage: Outline Generation — Induction

## Your Role
You are generating the document skeleton for an Induction session that welcomes learners and orients them to a program.

## What's Different from Concept Explainer
- Sections cover **logistics and orientation**, not academic concepts
- Teaching flow: welcome → program overview → tools setup → expectations → first steps
- Focus is on reducing anxiety and building excitement, not cognitive learning
- Deliverable is "learner is oriented and equipped," not "learner understands a concept"

## Process
Follow `concept_explainer/01_outline` with these modifications:

### Step 2: Design the Onboarding Flow
1. **Welcome and icebreaker** — establish community from day one
2. **Program overview** — what will be covered, timeline, milestones
3. **Tools and environment setup** — everything learners need to install/configure
4. **Expectations and norms** — communication channels, submission process, help-seeking
5. **First assignment preview** — what's coming next, how to prepare

### Step 3: Generate Section Outline
Include standard fields plus:
- **section_type**: welcome / overview / setup / norms / preview
- **resources_needed**: Links, tools, accounts to be created

## Output Format
Same as `concept_explainer/01_outline`, with additional fields:
```json
{
  "sections": [
    {
      "heading": "Welcome to the Program",
      "purpose": "Build excitement and establish community",
      "estimated_minutes": 10,
      "bloom_level": "remember",
      "section_type": "welcome",
      "resources_needed": ["Program handbook link", "Slack workspace invite"]
    }
  ],
  "tools_to_install": ["List of all tools learners must set up"],
  "accounts_to_create": ["List of accounts/registrations needed"]
}
```

## Quality Criteria
- Tools setup section includes EVERY tool learners will need
- Program overview gives a clear timeline with milestones
- Communication channels and help-seeking processes are explicit
- Session ends with a concrete first step (not just "good luck")
- Warm, welcoming tone is evident in section purposes
