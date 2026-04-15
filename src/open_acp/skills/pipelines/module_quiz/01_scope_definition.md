# Stage: Scope Definition — Module Quiz

## Your Role
You are defining the scope for a module quiz covering ~4 sessions of material (10-15 questions, 25-35 minutes).

## Assessment Profile
- **Purpose**: Summative for the module — measures understanding of a coherent topic block
- **Duration**: 25-35 minutes
- **Question count**: 10-15 questions
- **Bloom focus**: Understand/Apply (with some Remember and Analyze)
- **Scope**: 4 sessions within one module
- **Stakes**: Medium — contributes to grades but is not the sole assessment

## Process
Follow `classroom_quiz/01_scope_definition` with these modifications:

### Step 1: Identify the Module Scope
- Review ALL sessions in the module (typically 4)
- List concepts from each session, noting which build on others
- Identify cross-session connections (concepts that span multiple sessions)
- Weight coverage: more questions for foundational/complex topics

### Step 2: Define the Bloom Distribution
Target for module quiz:
- **Remember**: 20-25% (2-3 questions)
- **Understand**: 35-40% (4-5 questions)
- **Apply**: 25-30% (3-4 questions)
- **Analyze**: 10-15% (1-2 questions)

### Step 3: Cross-Session Integration
- At least 2 questions should require knowledge from MULTIPLE sessions
- These integration questions should be at Apply or Analyze level
- Test whether learners can connect concepts, not just recall isolated facts

## Output Format
Same structure as `classroom_quiz/01_scope_definition`, with:
```json
{
  "assessment_profile": {
    "type": "module_quiz",
    "purpose": "summative_module",
    "duration_minutes": 30,
    "question_count": 12,
    "module_scope": "Module 2: Data Structures",
    "sessions_covered": ["Session 5", "Session 6", "Session 7", "Session 8"],
    "stakes": "medium"
  },
  "cross_session_questions": 2,
  "session_weight": {"session_5": 3, "session_6": 3, "session_7": 3, "session_8": 3}
}
```

## Quality Criteria
- 10-15 questions covering all 4 sessions
- At least 2 cross-session integration questions
- Bloom distribution weighted toward Understand/Apply
- No single session has more than 40% of questions
- Duration is 25-35 minutes
