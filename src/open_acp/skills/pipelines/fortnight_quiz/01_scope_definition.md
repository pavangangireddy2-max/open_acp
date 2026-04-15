# Stage: Scope Definition — Fortnight Quiz

## Your Role
You are defining the scope for a fortnight (biweekly) quiz — cumulative, covering ~2 modules (15-20 questions, 35-45 minutes).

## Assessment Profile
- **Purpose**: Cumulative check — reinforces retention and integration across modules
- **Duration**: 35-45 minutes
- **Question count**: 15-20 questions
- **Bloom focus**: Apply/Analyze (with supporting Understand)
- **Scope**: ~2 modules (~8 sessions), cumulative
- **Stakes**: Medium-high — significant grade component

## Process
Follow `module_quiz/01_scope_definition` with these modifications:

### Step 1: Identify Cumulative Scope
- Review all sessions across the 2-module span
- Identify topics that have matured enough for Apply/Analyze level testing
- Weight recent material slightly more (60/40 split recent/earlier)
- Identify cross-MODULE connections (not just cross-session)

### Step 2: Define the Bloom Distribution
Target for fortnight quiz:
- **Remember**: 10-15% (2-3 questions: key facts that must be internalized by now)
- **Understand**: 25-30% (4-5 questions)
- **Apply**: 35-40% (6-7 questions: the bulk)
- **Analyze**: 15-20% (3-4 questions: compare approaches, debug, optimize)

### Step 3: Cumulative Integration
- At least 3-4 questions require knowledge from BOTH modules
- Earlier material should be tested at a HIGHER Bloom level than when first taught
- "Did you retain and can you now apply what you learned 2 weeks ago?"

## Output Format
Same structure as `module_quiz/01_scope_definition`, with:
```json
{
  "assessment_profile": {
    "type": "fortnight_quiz",
    "purpose": "cumulative_check",
    "duration_minutes": 40,
    "question_count": 18,
    "scope": "Modules 1-2 (Sessions 1-8)",
    "stakes": "medium_high"
  },
  "cross_module_questions": 4,
  "module_weight": {"module_1": 7, "module_2": 11},
  "retention_questions": 3
}
```

## Quality Criteria
- 15-20 questions covering 2 modules cumulatively
- At least 3 cross-module integration questions
- Earlier material tested at higher Bloom level (retention + application)
- Recent material weighted slightly more (60/40)
- Duration is 35-45 minutes
