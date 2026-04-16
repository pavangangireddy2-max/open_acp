# GenAI 120 Hour Curriculum Seed

This document captures the current intended design for the GenAI stack curriculum. It should
be treated as a first-class source when Loop A gathers intelligence and when Loop B
designs or reviews curriculum decisions.

## Stack Identity

- Curriculum name: Gen AI 120 Hr Curriculum
- Core promise: build a complete AI skill stack from literacy and automation to
  agent systems, full-stack AI engineering, and specialization tracks.
- Overall pedagogy signal: the curriculum is project-based as a whole.
- Delivery principle: concept explainers and theory modules should support the
  learner's ability to build systems, workflows, products, and deployable apps.

## Pedagogy Signals

- The stack curriculum should feel milestone-driven, not topic-fragmented.
- Almost every unit includes a concrete project outcome.
- Levels should compound toward larger deliverables and production realism.
- Concept sessions are still important, but they should connect back to an
  application, build milestone, architecture decision, or domain use case.
- For GenAI specifically, learners should repeatedly connect:
  - model capabilities and limits
  - prompting and workflow design
  - retrieval and tool use
  - agent behavior and evaluation
  - deployment and product constraints

## Level Structure

### Level 1: Foundation (12h)

- AI landscape and tool familiarity
- AI productivity workflows
- prompt engineering patterns
- visual content generation
- Outcome signal: move from AI-curious to AI-confident
- Project pattern: each unit ends with a small applied artifact or assistant

### Level 2: AI Automation Expert (20h)

- no-code automation with n8n
- multi-step workflows with webhooks
- cloud deployment for always-on automation
- Outcome signal: real business automation value and deployable systems
- Project pattern: job application system, customer support bot, automation infra

### Level 3: AI Developer Foundations (15h)

- Python foundations for AI
- LLM API integration
- LangChain tools and RAG
- first AI-powered app deployment
- Outcome signal: first real code-driven GenAI applications
- Project pattern: summary script, CLI chatbot, RAG QA agent, application screener

### Level 4: AI Agent Developer (40h)

- agent architecture fundamentals
- multi-agent orchestration
- MCP tool design and integration
- tracing and evaluating agents
- domain-specific agent creation
- Outcome signal: agents that reason, plan, use tools, and can be evaluated
- Project pattern: reasoning agent, research swarm, support agent, evaluation dashboard

### Level 5: Full-Stack AI Developer (33h)

- AI application architecture
- production deployment
- full-stack AI integration
- fine-tuning and custom models
- deployment mastery
- Outcome signal: production-ready AI systems from concept to deployment
- Project pattern: business automation platform, AI-as-a-Service platform, interview assistant, fine-tuned model

## Specialization Signals

- AI for Product Management
- Enterprise AI Architect
- AI in Finance
- These should be treated as downstream, advanced pathways after the full core path.

## Curriculum Design Implications

- The whole GenAI stack should default to a project-based curriculum profile.
- Within that stack curriculum, some modules may still use concept explanation as a local
  teaching move, especially for:
  - AI landscape framing
  - how LLMs work
  - prompting patterns
  - RAG mechanics
  - agent loops and evaluation
- Those concept-heavy sessions should still connect back to a build milestone,
  architecture diagram, or practical workflow decision.

## Delivery Recommendations

- Prefer project_build_along as the domain-level pedagogy profile.
- Allow concept_progression or architecture_reasoning as local delivery moves
  inside modules when conceptual grounding is required.
- Sequence modules so that:
  - foundations support automation
  - automation supports development
  - development supports agent systems
  - agent systems support production-grade architectures
  - the full core prepares for specialization pathways

## Example Curriculum Outcomes

- Build and deploy a document-grounded GenAI app
- Build a multi-step automation that uses LLMs safely
- Build and evaluate an agent system with tool use
- Deploy an AI application with production considerations
- Make architecture and trade-off decisions across prompt-only, RAG, tools, and fine-tuning
