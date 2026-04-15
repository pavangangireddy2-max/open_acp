# Stage: Outline Generation — Concept Explainer

## Your Role
You are generating the document skeleton for a Concept Explainer session. This outline will guide all subsequent stages.

## Prerequisites
- Module metadata: title, domain, estimated_hours, sequence
- Learning objectives with Bloom levels
- Prerequisite modules (what learners already know)
- Resolved pedagogy profile and layered style guidance

## Input Artifacts
- `objectives` — the approved learning objectives for this session

## Process

### Step 1: Analyze the Module Context
- Read the module title, domain, and estimated hours
- Identify the core concept being explained
- Check prerequisites — what can you assume learners already know?
- If wiki entities exist for this topic, read them for context

### Step 2: Design the Teaching Flow
Use backward design from the approved objectives:
1. Group related objectives together
2. Decide the teaching progression needed to achieve them
3. Sequence the session from activation -> explanation -> example -> practice -> reflection

For each section, assign one `teaching_mode` from this allowed set:
- `motivation`
- `prior_knowledge_bridge`
- `concept_explain`
- `worked_example`
- `guided_practice`
- `reflection_summary`

### Step 3: Generate Section Outline
For each section, define:
- **heading**: Clear, descriptive title
- **purpose**: What this section achieves in the learning journey
- **estimated_minutes**: Realistic time allocation
- **bloom_level**: The cognitive level this section targets
- **teaching_mode**: What pedagogical move this section is making
- **objective_ids**: Which objectives this section advances
- **subsections**: Optional breakdown of key points

### Step 4: Validate Completeness
- Every objective must map to at least one section
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
      "teaching_mode": "concept_explain",
      "objective_ids": ["obj_1"],
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
- `teaching_mode` choices should create a coherent learner journey, not a random label assortment
