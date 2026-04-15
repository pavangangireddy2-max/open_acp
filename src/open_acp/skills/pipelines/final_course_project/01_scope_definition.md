# Stage: Scope Definition — Final Course Project

## Your Role
You are defining the scope for a capstone project that demonstrates comprehensive course mastery through an open-ended deliverable.

## Assessment Profile
- **Purpose**: Summative capstone — demonstrates ability to CREATE, not just recall
- **Duration**: Multi-day (typically 1-2 weeks)
- **Bloom focus**: Create (with supporting Apply, Analyze, Evaluate)
- **Scope**: Entire course — must integrate concepts from multiple modules
- **Stakes**: High — major grade component, often the culminating assessment
- **Format**: Open-ended project deliverable (code, report, presentation, or combination)

## Process

### Step 1: Define the Project Domain
- Review the full course curriculum and identify 3-5 possible project themes
- Each theme should require integrating concepts from at least 3 modules
- Themes should be relevant to real-world applications in the domain
- Consider offering 2-3 project options for student choice

### Step 2: Define Scope Boundaries
- **Minimum viable deliverable**: What MUST the project include to pass?
- **Expected deliverable**: What should a solid project look like?
- **Stretch goals**: What would make an exceptional project?
- **Out of scope**: What should students explicitly NOT attempt?

### Step 3: Identify Required Competencies
Map project requirements to course modules:
- Which modules provide essential skills for this project?
- Which skills are "must demonstrate" vs "nice to demonstrate"?
- Are there any skills NOT covered in the course that might be needed? (If so, provide resources)

### Step 4: Define Deliverables
List all required submissions:
- Source code / main artifact
- Documentation (README, design doc)
- Presentation / demo (if applicable)
- Reflection / write-up (what they learned, challenges faced)

## Output Format
```json
{
  "assessment_profile": {
    "type": "final_course_project",
    "purpose": "capstone_summative",
    "duration_days": 10,
    "scope": "Full course (Modules 1-8)",
    "stakes": "high"
  },
  "project_options": [
    {
      "title": "Personal Finance Tracker API",
      "description": "Build a REST API for tracking personal finances...",
      "modules_integrated": ["Module 2", "Module 4", "Module 6"],
      "minimum_viable": "3 endpoints, SQLite database, basic CRUD",
      "expected": "5+ endpoints, authentication, error handling, tests",
      "stretch_goals": ["Deployment to cloud", "Front-end dashboard"]
    }
  ],
  "deliverables": ["source_code", "readme", "design_document", "demo_video"],
  "required_competencies": ["REST API design", "database operations", "testing"]
}
```

## Quality Criteria
- Project requires integrating at least 3 modules
- Minimum viable deliverable is achievable by an average student
- Stretch goals challenge top students without being mandatory
- Scope boundaries are clear (students know what's expected)
- Timeline is realistic (1-2 weeks, accounting for other coursework)
