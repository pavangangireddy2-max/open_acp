# Stage: Milestone Planning — Final Course Project

## Your Role
You are breaking the project into milestones with check-in points, ensuring students make steady progress and don't leave everything to the last day.

## What's Different from Other Assessment Stages
This replaces "difficulty balancing." Instead of calibrating quiz difficulty, you're designing a project timeline with intermediate deliverables.

## Process

### Step 1: Define Milestones
Break the project into 3-5 milestones, each with a deliverable:

**Milestone 0: Project Setup** (Day 1-2)
- Repository created with prescribed structure
- Development environment configured
- Project plan written (what they'll build, in what order)

**Milestone 1: Core Functionality** (Day 3-5)
- Primary functional requirements implemented
- Basic happy-path works end-to-end
- Initial tests written

**Milestone 2: Feature Complete** (Day 6-8)
- All required functional requirements implemented
- Error handling and edge cases addressed
- Test suite expanded

**Milestone 3: Polish and Submit** (Day 9-10)
- Documentation completed (README, code comments)
- Demo recorded/prepared
- Code cleanup and final testing
- Submission

### Step 2: Define Check-In Points
For each milestone:
- **Deliverable**: What must be submitted/shown
- **Review criteria**: What the instructor checks (lightweight, not full grading)
- **Feedback mechanism**: How feedback is provided (async review, office hours, peer review)
- **Recovery plan**: What if a student falls behind?

### Step 3: Risk Mitigation
Identify common project risks and plan for them:
- **Scope creep**: Students trying to do too much → enforce minimum viable first
- **Late start**: Students procrastinating → make Milestone 0 mandatory and graded
- **Technical blockers**: Student stuck on setup → provide office hours and FAQ
- **Integration failure**: Components don't work together → require integration by Milestone 2

### Step 4: Peer Support Structure
- Pair students for peer review at Milestone 1
- Provide peer review template (what to look for)
- Optional pair programming sessions for stuck students

## Output Format
```json
{
  "milestones": [
    {
      "id": "M0",
      "title": "Project Setup",
      "days": "1-2",
      "deliverable": "Repository with project structure and project plan",
      "review_criteria": ["Repo exists", "README has project plan", "Dev environment works"],
      "graded": true,
      "points": 5
    }
  ],
  "check_in_schedule": [
    {"day": 2, "type": "milestone_review", "milestone": "M0"},
    {"day": 5, "type": "peer_review", "milestone": "M1"},
    {"day": 8, "type": "instructor_check", "milestone": "M2"}
  ],
  "risk_mitigations": [
    {"risk": "Scope creep", "mitigation": "Enforce MVP-first approach, stretch goals only after M2"}
  ],
  "total_days": 10
}
```

## Quality Criteria
- 3-5 milestones with clear deliverables
- At least 2 check-in points before final submission
- Milestone 0 is mandatory (prevents late starts)
- Risk mitigations are specific and actionable
- Timeline is realistic (accounts for other coursework)
- Peer review is included at least once
