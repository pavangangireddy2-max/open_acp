# Stage: Rubric Design — Final Course Project

## Your Role
You are creating a comprehensive rubric for evaluating an open-ended capstone project.

## What's Different from Quiz Rubrics
- Evaluates a DELIVERABLE, not question answers
- Uses quality-level rubrics (excellent/good/adequate/insufficient), not point-per-answer
- Multiple evaluation dimensions (functionality, code quality, documentation, presentation)
- Must handle variation (every student's project is slightly different)

## Process

### Step 1: Define Evaluation Dimensions
Typical dimensions (weighted by importance):
1. **Functionality** (30-40%): Does it work? Are requirements met?
2. **Code Quality** (20-25%): Clean code, good structure, appropriate patterns
3. **Testing** (10-15%): Test coverage, test quality, edge cases
4. **Documentation** (10-15%): README, code comments, design decisions
5. **Integration Depth** (10-15%): How well are course concepts integrated?
6. **Presentation** (5-10%): Demo quality, communication of design decisions

### Step 2: Create Quality-Level Rubric Per Dimension
For each dimension, define 4 levels:

| Level | Score Range | Description |
|-------|------------|-------------|
| Excellent | 90-100% | Exceeds expectations, demonstrates mastery |
| Good | 70-89% | Meets all requirements, competent execution |
| Adequate | 50-69% | Meets minimum requirements, some gaps |
| Insufficient | <50% | Does not meet minimum requirements |

Provide specific, observable criteria for each level per dimension.

### Step 3: Create the Checklist
Quick-scan checklist for initial assessment:
- [ ] All required functional requirements implemented
- [ ] Code runs without errors
- [ ] Tests pass
- [ ] README is complete
- [ ] Demo is provided

### Step 4: Define Grade Boundaries
- A: 85%+ (Excellent in most dimensions)
- B: 70-84% (Good in most, adequate in none)
- C: 55-69% (Adequate overall)
- D: 40-54% (Below adequate in some areas)
- F: <40%

## Output Format
```json
{
  "rubric": {
    "dimensions": [
      {
        "name": "Functionality",
        "weight": 0.35,
        "levels": {
          "excellent": "All required + optional requirements met, handles edge cases gracefully",
          "good": "All required requirements met, works correctly for standard inputs",
          "adequate": "Most required requirements met, some bugs in edge cases",
          "insufficient": "Major requirements missing or non-functional"
        }
      }
    ],
    "checklist": ["Code runs without errors", "All FR-required items implemented", "..."],
    "grade_boundaries": {"A": 85, "B": 70, "C": 55, "D": 40}
  }
}
```

## Quality Criteria
- At least 5 evaluation dimensions
- Each dimension has 4 clearly differentiated quality levels
- Observable criteria (not "good code" — instead "functions are < 20 lines, single responsibility")
- Weights reflect course priorities
- Quick-scan checklist for initial pass/fail assessment
- Grade boundaries are defined and fair
