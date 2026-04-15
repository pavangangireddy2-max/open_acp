# Stage: Outline Generation — Concept Explainer

## Your Role
You are generating the document skeleton for a Concept Explainer session. This outline will guide all subsequent stages.

## Prerequisites
- Module metadata: title, domain, estimated_hours, sequence
- Learning objectives with Bloom levels (from curriculum map)
- Prerequisite modules (what learners already know)
- Skill graph context (demand scores, related skills) — from wiki if available

## Input Artifacts
None (this is the first stage)

## Process

### Step 1: Analyze the Module Context
- Read the module title, domain, and estimated hours
- Identify the core concept being explained
- Check prerequisites — what can you assume learners already know?
- If wiki entities exist for this topic, read them for context

### Step 2: Design the Teaching Flow
Use backward design:
1. Start with the terminal outcome — what should the learner be able to DO after this session?
2. Identify the prerequisite knowledge needed to reach that outcome
3. Design the progression: activate prior knowledge → introduce new concept → build understanding → apply

Choose an appropriate teaching pattern:
- **Concept-first**: Define → Explain → Illustrate → Practice (good for abstract concepts)
- **Example-first**: Show concrete case → Extract pattern → Generalize → Apply (good for practical skills)
- **Problem-first**: Pose a challenge → Explore why it's hard → Introduce the concept as a solution → Practice (good for motivation)

### Step 3: Generate Section Outline
For each section, define:
- **heading**: Clear, descriptive title
- **purpose**: What this section achieves in the learning journey
- **estimated_minutes**: Realistic time allocation
- **bloom_level**: The cognitive level this section targets
- **subsections**: Optional breakdown of key points

### Step 4: Validate Completeness
- Every learning objective must map to at least one section
- Bloom levels should progress (don't jump from remember to create)
- Total estimated_minutes should be within 10% of module.estimated_hours × 60
- Include time for activities (at least 40% of session should be practice)

## Output Format
Return a JSON object matching `outline.schema.json`:
```json
{
  "sections": [
    {
      "heading": "Section title",
      "purpose": "What this section achieves",
      "estimated_minutes": 15,
      "bloom_level": "understand",
      "subsections": ["Key point 1", "Key point 2"]
    }
  ],
  "teaching_flow": "Description of the pedagogical progression...",
  "prerequisite_check": "How prior knowledge is activated at the start",
  "total_estimated_minutes": 60
}
```

## Quality Criteria
- No circular dependencies between sections
- Cognitive load per section: max 3-4 new concepts
- Duration estimates must account for discussion/processing time
- The teaching_flow must explain WHY this progression was chosen, not just list the sections
