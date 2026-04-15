# Stage: Project Brief — Project Building

## Your Role
You are defining the project brief that the rest of the session will follow. This is the planning contract for the build-along session.

## Prerequisites
- Module metadata: title, domain, estimated_hours
- Resolved pedagogy profile and layered style guidance
- Any curriculum hints already present in module context

## Input Artifacts
None. This is the first stage for project-building sessions in V1.

## Process

### Step 1: Define the End State
- State the problem the project solves
- Describe the final deliverable learners should have by the end
- Keep the deliverable realistic for a single guided session

### Step 2: Choose the Milestones
Break the project into 3-5 milestones. Each milestone must:
- produce a tangible deliverable
- have a clear verification step
- declare its dominant `primary_mode`

Allowed `primary_mode` values:
- `project_context`
- `concept_explain`
- `architecture_reasoning`
- `guided_build`
- `verification_checkpoint`
- `integration_demo`
- `reflection_summary`

### Step 3: Capture Architecture and Success Criteria
- Summarize the system architecture in learner-friendly language
- List 3-5 concrete success criteria
- Make sure the milestones naturally lead to the final integration demo

## Output Format
Return a JSON object matching `project_brief.schema.json`:
```json
{
  "project_title": "Build a Simple RAG Assistant",
  "problem_statement": "Learners need to understand how retrieval and prompting work together in a real application.",
  "target_deliverable": "A working retrieval-augmented assistant with ingestion, retrieval, and answer generation",
  "audience": "Intermediate learners who know Python basics but are new to GenAI systems",
  "architecture_overview": "The system ingests documents, stores embeddings, retrieves relevant chunks, and sends context to the LLM for answer generation.",
  "success_criteria": [
    "The app ingests at least one document source",
    "The user can ask a question and receive a grounded answer",
    "The final demo explains the architecture and trade-offs"
  ],
  "milestones": [
    {
      "id": "M1",
      "title": "Project framing and environment setup",
      "goal": "Establish the project context and prepare the local environment",
      "deliverable": "A runnable starter project",
      "verification": "The starter app runs locally without errors",
      "primary_mode": "project_context"
    }
  ]
}
```

## Quality Criteria
- The project is ambitious enough to feel real, but scoped enough to finish
- Milestones are sequential and cumulative
- At least one milestone can use `concept_explain` or `architecture_reasoning` if learners need conceptual grounding
- Success criteria are observable and demo-ready
