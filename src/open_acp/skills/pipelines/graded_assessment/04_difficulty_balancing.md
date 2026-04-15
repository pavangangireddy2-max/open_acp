# Stage: Difficulty Balancing — Graded Assessment

## Your Role
You are calibrating difficulty for a formal exam to produce a fair, bell-curve-appropriate grade distribution.

## What's Different from Final Course Quiz
- Must produce a proper grade distribution (bell curve centered on pass mark)
- Strict time limits require careful time-per-question calibration
- Section-level balancing (each section should be internally balanced)
- University standards: average score should be 55-65% (not too easy, not too hard)

## Process

### Step 1: Per-Section Difficulty Calibration

**Section A (MCQ + Short Answer)**:
- Easy: 30% (confident start, build momentum)
- Medium: 50% (solid understanding required)
- Hard: 20% (discriminator questions)
- Time: ~2 minutes per question

**Section B (Applied Problems)**:
- Easy: 20% (straightforward application)
- Medium: 50% (requires design thinking)
- Hard: 30% (complex scenarios, edge cases)
- Time: ~4-5 minutes per question

**Section C (Analysis/Design)**:
- Medium: 40% (structured analysis)
- Hard: 40% (requires genuine insight)
- Very Hard: 20% (differentiates top students)
- Time: ~8-12 minutes per question

### Step 2: Overall Distribution Targeting
- Target mean score: 55-65%
- Target standard deviation: 12-18%
- Pass rate target: 70-80% of students
- High distinction (>80%): 5-10% of students
- Fail (<40%): 5-15% of students

### Step 3: Time Budget Verification
For 120-minute exam:
- Section A: ~40 minutes (20 questions)
- Section B: ~45 minutes (10 questions)
- Section C: ~35 minutes (3-5 questions)
- Buffer: 0 minutes (exams are time-pressured by design)

### Step 4: Discrimination Analysis
- Easy questions should have high pass rate (>85%) — they build confidence
- Medium questions discriminate between pass and fail students
- Hard questions discriminate between good and excellent students
- If a question is so hard that <20% would get it right, reconsider its inclusion

## Output Format
```json
{
  "calibration_report": {
    "target_mean": 60,
    "target_std": 15,
    "section_difficulty": {
      "A": {"easy": 6, "medium": 10, "hard": 4},
      "B": {"easy": 2, "medium": 5, "hard": 3},
      "C": {"medium": 2, "hard": 2, "very_hard": 1}
    },
    "time_budget": {"A": 40, "B": 45, "C": 35, "total": 120},
    "expected_pass_rate": 0.75,
    "adjustments_made": ["Simplified B3 from hard to medium", "Added 1 easy question to Section A"]
  }
}
```

## Quality Criteria
- Target mean is 55-65%
- Each section is internally balanced (not all hard questions in one section)
- Time budget is feasible (total does not exceed exam duration)
- Discrimination: easy questions >85% pass, hard questions <50% pass
- No question is so hard that <15% would get it right (unless it's clearly marked as a bonus)
