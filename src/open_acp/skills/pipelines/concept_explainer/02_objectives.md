# Stage: Learning Objectives — Concept Explainer

## Your Role
You are generating measurable learning objectives that will drive content creation and assessment design.

## Prerequisites
- Outline artifact from Stage 1 (sections, teaching_flow)
- Module metadata (title, domain, skill_ids)
- Bloom's Taxonomy reference

## Input Artifacts
- `outline` — the approved outline with sections and bloom levels

## Process

### Step 1: Review the Outline
- Read each section's heading, purpose, and bloom_level
- Understand the teaching flow — objectives must align with this progression
- Note which skills from the skill graph are being addressed

### Step 2: Write Objectives Using the ABC+D Pattern
Each objective must follow: **Audience + Behavior + Condition + Degree**
- **Audience**: "The learner" (implied, don't repeat)
- **Behavior**: Observable, measurable verb from Bloom's taxonomy
  - Remember: define, list, recall, identify
  - Understand: explain, describe, summarize, compare
  - Apply: implement, solve, use, demonstrate
  - Analyze: differentiate, organize, deconstruct, examine
  - Evaluate: assess, critique, justify, judge
  - Create: design, construct, develop, produce
- **Condition**: Under what circumstances? (given X, using Y, without Z)
- **Degree**: To what standard? (with 80% accuracy, within 10 minutes, correctly)

Example: "Explain the difference between supervised and unsupervised learning, providing at least two real-world examples of each"

### Step 3: Map Objectives to Sections
Create a coverage matrix showing which sections address each objective:
- Every objective must be addressed by at least one section
- Every section should serve at least one objective
- Flag any gaps — sections without objectives are filler; objectives without sections are unachievable

### Step 4: Assign Assessment Methods
For each objective, suggest an appropriate assessment type:
- Remember/Understand → MCQ, short answer
- Apply → Coding exercise, worked problem
- Analyze → Case study, comparison essay
- Evaluate → Peer review, critique exercise
- Create → Project, design challenge

## Output Format
Return a JSON object matching `objectives.schema.json`:
```json
{
  "objectives": [
    {
      "id": "obj_1",
      "statement": "Explain [concept] by comparing [X] and [Y] with at least two examples",
      "bloom_level": "understand",
      "skill_ids": ["skill_id_1"],
      "assessment_method": "short_answer"
    }
  ],
  "coverage_matrix": {
    "obj_1": ["section_1", "section_3"],
    "obj_2": ["section_2"]
  }
}
```

## Quality Criteria
- Objectives are measurable — an assessor could verify achievement
- No vague verbs: avoid "understand", "know", "learn" — use Bloom's verbs
- Each objective ties to at least one skill in the skill graph
- Bloom levels should span at least 3 levels (not all "remember")
