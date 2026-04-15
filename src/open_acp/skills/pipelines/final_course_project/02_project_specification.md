# Stage: Project Specification — Final Course Project

## Your Role
You are writing the detailed project specification that students will follow — the equivalent of a "requirements document" for the capstone.

## What's Different from Question Generation
This replaces question generation. Instead of writing questions, you're writing a project brief that students will work on for 1-2 weeks.

## Process

### Step 1: Write the Project Brief
- **Context/Scenario**: Real-world motivation for the project (2-3 paragraphs)
- **Problem statement**: What needs to be built and why
- **Target users**: Who would use this (even if hypothetical)

### Step 2: Define Functional Requirements
Numbered, testable requirements:
1. FR-1: "The system must support user registration with email and password"
2. FR-2: "The system must allow CRUD operations on [resource]"
- Each requirement should be verifiable (pass/fail)
- Tag each with the module/skill it exercises
- Distinguish: required (must have) vs optional (nice to have)

### Step 3: Define Technical Requirements
- Technology stack (prescribed or student-choice with constraints)
- Code quality standards (testing, documentation, style)
- Architecture constraints (if any)
- Performance requirements (if applicable)

### Step 4: Define Submission Format
- Repository structure (prescribed folder layout)
- README template (what sections to include)
- Demo format (video, live presentation, or written walkthrough)
- Submission deadline and method

### Step 5: Provide Starter Resources
- Starter code / boilerplate (if applicable)
- Reference APIs or datasets
- Recommended tutorials for techniques not fully covered in course
- Example project (different domain but similar scope)

## Output Format
```json
{
  "project_brief": {
    "title": "Personal Finance Tracker API",
    "context": "...",
    "problem_statement": "...",
    "target_users": "..."
  },
  "functional_requirements": [
    {"id": "FR-1", "description": "...", "priority": "required", "module_reference": "Module 4"}
  ],
  "technical_requirements": {
    "stack": "Python + Flask + SQLite",
    "testing": "At least 10 unit tests covering core functionality",
    "documentation": "README with setup instructions, API documentation"
  },
  "submission_format": {
    "repository_structure": "...",
    "readme_template": "...",
    "demo_format": "5-minute screen recording",
    "deadline": "..."
  },
  "starter_resources": ["boilerplate_repo_url", "reference_api_docs"]
}
```

## Quality Criteria
- Every functional requirement is testable (pass/fail)
- Requirements are tagged to course modules (demonstrates integration)
- Required vs optional is clearly distinguished
- Submission format is unambiguous
- Starter resources are provided (don't leave students with a blank page)
- Spec is detailed enough that two students would build similar-scoped projects
