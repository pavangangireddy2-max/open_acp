# Stage: Scope Definition — Skill Assessment

## Your Role
You are defining the scope for a placement-linked skill assessment. The exact cadence and assessment window come from product and packaging configuration.

## Assessment Profile
- **Purpose**: Placement-linked skill verification across a configured assessment window
- **Duration**: 35-45 minutes
- **Question count**: 15-20 questions
- **Bloom focus**: Apply/Analyze (with supporting Understand)
- **Scope**: Product-configured topic/module window
- **Stakes**: Medium-high — significant readiness signal

## Process
Follow `module_quiz/01_scope_definition` with these modifications:

### Step 1: Identify the Assessment Scope
- Review all sessions across the configured assessment window
- Identify topics that have matured enough for Apply/Analyze level testing
- Weight recent material slightly more when the window is cumulative
- Identify cross-topic or cross-module connections where they are reasonable

### Step 2: Define the Bloom Distribution
Target for skill assessment:
- **Remember**: 10-15% (2-3 questions: key facts that must already be internalized)
- **Understand**: 25-30% (4-5 questions)
- **Apply**: 35-40% (6-7 questions: the bulk)
- **Analyze**: 15-20% (3-4 questions: compare approaches, debug, optimize)

### Step 3: Integration and Readiness
- Include integration questions when the assessment window spans multiple modules or topics
- Earlier material should be tested at a higher Bloom level than when first taught
- Verify whether the learner can retain and apply previously taught material in a fresh context

## Output Format
Same structure as `module_quiz/01_scope_definition`, with:
```json
{
  "assessment_profile": {
    "type": "skill_assessment",
    "purpose": "placement_linked_skill_check",
    "duration_minutes": 40,
    "question_count": 18,
    "scope": "Configured assessment window",
    "stakes": "medium_high"
  },
  "integration_questions": 4,
  "scope_weighting": {"earlier": 7, "recent": 11},
  "retention_questions": 3
}
```

## Quality Criteria
- 15-20 questions covering the configured assessment window
- Integration questions are included when the assessment spans multiple modules or topics
- Earlier material is tested at higher Bloom level (retention + application)
- Recent material can be weighted slightly more when the assessment is cumulative
- Duration is 35-45 minutes
