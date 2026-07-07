# Open ACP — Architecture Artifact

> Agentic Content Production: A 4-loop LangGraph pipeline that transforms raw intelligence signals into schema-validated, pedagogically-grounded educational content.

---

## 1. System Identity

| Property | Value |
|----------|-------|
| Name | Open ACP (Agentic Content Production) |
| Runtime | Python 3.12+, LangGraph, DSPy |
| LLM Backend | Claude Opus 4.6 (strong) / Haiku 4.5 (cheap) |
| Architecture Style | Manifest-driven, loop-based, agentic pipeline |
| Orchestration | LangGraph StateGraph per loop + Master StateGraph |
| Quality Model | 5-dimension eval + 4 human-approval gates + deterministic backprop routing |

---

## 2. High-Level System Diagram

```
                    ┌─────────────────────────────────────────┐
                    │          MASTER ORCHESTRATOR             │
                    │   run_id · cycle_id · domain · content  │
                    └──────────────────┬──────────────────────┘
                                       │
         ┌─────────────┬───────────────┼───────────────┬─────────────┐
         │             │               │               │             │
         v             v               v               v             │
   ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐         │
   │  LOOP A   │ │  LOOP B   │ │  LOOP C   │ │  LOOP D   │         │
   │Intelligence│ │Curriculum │ │ Pipeline  │ │ Feedback  │         │
   │ Gathering │ │  Design   │ │ Execution │ │ & Routing │         │
   │           │ │           │ │           │ │           │         │
   │  Gate G1  │ │  Gate G2  │ │  Gate G3  │ │  Gate G4  │         │
   └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └─────┬─────┘         │
         │             │               │               │             │
         v             v               v               v             │
   ┌──────────┐  ┌──────────┐  ┌───────────┐  ┌───────────┐        │
   │  Wiki    │  │Curriculum│  │  Stage     │  │ BackProp  │────────┘
   │ Entities │─>│   Map    │─>│ Artifacts  │  │  Router   │ (routes fixes
   │          │  │          │  │            │  │           │  back to loops)
   └──────────┘  └──────────┘  └───────────┘  └───────────┘
```

---

## 3. The Four Loops

### 3.1 Loop A — Intelligence & Signal Gathering

**Purpose**: Ingest raw signals from 11 channel categories, detect patterns, build a compounding runtime wiki of skills, learner profiles, and market intelligence.

**Node Flow**:
```
ingest_signals
    → detect_patterns
        → derive_skill_outcomes_digest
            → derive_market_and_community_digest
                → update_skill_graph
                    → update_learner_model
                        → update_product_context
                            → update_wiki_index
                                → END
```

**Inputs**:
- Raw sources from `knowledge/sources/` (organized by source family manifests)
- 11 channel categories: Student Learning, Customer Support, Sales, Social Media, Placement, Platform Analytics, Performance Analytics, Interview Intel, Internal Team, Industry Market, Cross-Program

**Outputs**:
- Wiki entities (skills with demand_score + durability, learner personas with gaps/misconceptions, product summaries)
- Stack profiles
- Signal batch with detected patterns and drift scores

**Gate G1** (Strategy Review): Non-blocking advisory gate.

---

### 3.2 Loop B — Curriculum Design

**Purpose**: Transform wiki intelligence into a structured, pedagogically-grounded curriculum through deterministic profile resolution and LLM-guided design.

**Node Flow**:
```
load_wiki_context
    → resolve_product_context
        → resolve_structure_profile
            → resolve_packaging_profile
                → resolve_design_priority_profile
                    → resolve_time_budget_context
                        → resolve_pedagogy_profile          ← deterministic, no LLM
                            → generate_brief                ← single LLM call
                                → compose_product_specific_curriculum_container
                                    → compare_curriculum_changes
                                        → design_courses
                                            → design_modules
                                                → design_topics
                                                    → design_learning_units
                                                        → design_practice
                                                            → design_learning_assessments
                                                                → resolve_skill_assessment_requirements
                                                                    → align_learning_with_skill_assessments
                                                                        → END
```

**Inputs**:
- Wiki entities (skill graph, learner model, product context)
- Stack manifest, product manifest, structure profile, packaging profile
- Pedagogy guidance (core + profiles)

**Outputs**:
- `CurriculumMap` (courses → modules → topics → learning units)
- `ModuleWorkPlan` per module (production targets, topic delivery plans)
- Design artifacts: brief, course plans, module plans, topic plans, unit designs, practice designs, assessment plans

**Gate G2** (Curriculum Approval): Blocking gate — requires curriculum architect + SME panel.

---

### 3.3 Loop C — Pipeline Execution

**Purpose**: Execute stage-based content generation for each content type, with schema validation, review checkpoints, and revision loops.

**Execution Pattern** (per stage):
```
Load stage director skill
    → Load layered style context
        → Generate candidate artifact (Claude)
            → Parse artifact (JSON/YAML)
                → Schema-validate (jsonschema)
                    → Review against review_focus + success_criteria
                        → Revise (up to max_iterations if strict)
                            → Persist to storage/artifacts/
```

**Example Pipeline — Concept Explainer** (6 stages):

| Stage | Artifact Schema | Model | Review Focus |
|-------|----------------|-------|--------------|
| 1. objectives | objectives.schema.json | strong | Measurable verbs, Bloom progression, assessment fit |
| 2. outline | concept_outline.schema.json | strong | Objective mapping, teaching mode sequence, duration |
| 3. core_content | concept_core_content.schema.json | strong | Objective coverage, teaching modes, examples, citations |
| 4. activities | concept_activities.schema.json | strong | Bloom coverage, teaching mode preservation, time estimates |
| 5. brand_polish | brand_polish.schema.json | cheap | Voice, formatting, clarity |
| 6. slide_deck | concept_slide_deck.schema.json | strong | One-idea-per-slide, speaker notes, visuals |

**Style Layer Composition** (injected into every stage prompt):
```
pedagogy core → pedagogy profile → format guidance → stack/domain guidance → brand guidance
```

**Pipeline Families**:
- **Session** (6 types): concept_explainer, problem_solving, project_building, learning_support, platform_walkthrough, induction
- **Written** (2 types): reading_material, summary_cheatsheet
- **Practice** (2 types): mcq_practice, coding_practice
- **Assessment** (6 types): classroom_quiz, module_quiz, skill_assessment, final_course_quiz, final_course_project, graded_assessment

**Gate G3** (Content Quality): Blocking gate — requires SME + pedagogy + brand review.

---

### 3.4 Loop D — Feedback & Backpropagation

**Purpose**: Collect feedback, classify issues, route fixes back to the correct loop/node via deterministic routing rules.

**Node Flow**:
```
collect_feedback
    → classify_insights       ← LLM call
        → route_fixes         ← deterministic (BackpropRouter)
            → health_monitor
                → END
```

**Inputs**:
- Raw feedback signals (from channels or synthetic mock ingestor)
- Content artifacts from Loop C
- Evaluation scores

**Outputs**:
- `InsightClassification` list (fix_type + severity + evidence)
- `FixRoute` list (target_loop + target_nodes + gate + auto_approved flag)
- Health report (wiki lint + content health)

**Backprop Routing Table** (deterministic, no LLM):

| Fix Type | Severity | Target Loop | Target Nodes | Gate | Auto-Approved |
|----------|----------|-------------|--------------|------|---------------|
| CONTENT_FIX | Low | C | core_content, activities | G3 | Yes |
| CONTENT_FIX | High/Critical | C | core_content | G3 | No |
| BRAND_FIX | Any | C | brand_polish | G3 | Yes |
| DESIGN_FIX | Low | B | compose_curriculum_container | G2 | Yes |
| DESIGN_FIX | High/Critical | B | compose_curriculum_container | G2 | No |
| CURRICULUM_FIX | Any | A → B | update_skill_graph, compose_curriculum_container | G4 | No |
| PEDAGOGY_FIX | Any | B + C | resolve_pedagogy_profile, activities | G4 | No |

**Gate G4** (High-Severity Fix): Blocking gate — requires strategy lead.

---

## 4. State Models

### 4.1 Master State
```
MasterState
├── run_id: str
├── cycle_id: str
├── domain: str
├── content_type: str
├── module_title: str
├── module_id: str
├── estimated_hours: float
├── auto_approve: bool
├── current_loop: str
├── error: str | None
├── loop_a_result: dict
├── loop_b_result: dict
├── loop_c_result: dict
└── loop_d_result: dict
```

### 4.2 Loop A State
```
LoopAState
├── cycle_id, domain
├── product_family, product_version
├── signal_batch: SignalBatch (batch_id, signals[], ingested_at)
├── detected_patterns: list
├── skill_outcomes_digest: dict
├── market_and_community_digest: dict
├── wiki_entries_created: list      ← accumulator (merge reducer)
├── wiki_entries_updated: list      ← accumulator
├── stack_profiles_created: list    ← accumulator
├── stack_profiles_updated: list    ← accumulator
└── gate_g1_outcome: GateOutcome
```

### 4.3 Loop B State
```
LoopBState
├── cycle_id, domain, content_type
├── product_family, product_version
│
│  ── Input Contexts ──
├── skill_graph_context: dict
├── learner_context: dict
├── skill_outcomes_context: dict
├── market_and_community_context: dict
├── curriculum_source_context: dict
│
│  ── Resolved Profiles ──
├── product_context: dict
├── structure_profile: dict
├── packaging_profile: dict
├── design_priority_profile: dict
├── time_budget_context: dict
├── pedagogy_profile: dict
│
│  ── Design Outputs ──
├── brief: dict
├── curriculum_map: CurriculumMap
├── course_designs: list
├── module_designs: list
├── topic_designs: list
├── unit_designs: list
├── practice_designs: list
├── assessment_designs: list
├── skill_assessment_requirements: list
└── gate_g2_outcome: GateOutcome
```

### 4.4 Loop C State
```
LoopCState
├── cycle_id, domain
├── curriculum_map: CurriculumMap
├── current_module_id: str
├── pipeline_state: PipelineState
│   ├── pipeline_id, content_type
│   ├── current_stage: str
│   ├── stage_artifacts: dict[str, StageArtifact]
│   ├── iteration: int
│   └── status: str
├── eval_report: EvalReport
│   ├── scores: list[EvalScore]  (5 dimensions)
│   ├── final_score: float       (min of all)
│   └── passed: bool
└── gate_g3_outcome: GateOutcome
```

### 4.5 Loop D State
```
LoopDState
├── cycle_id, domain
├── raw_feedback: list[dict]
├── insights: list[InsightClassification]     ← accumulator
│   ├── fix_type: FixType
│   ├── severity: Severity
│   ├── description, evidence, source_channels
├── fix_routes: list[FixRoute]                ← accumulator
│   ├── target_loop, target_nodes, target_stages
│   ├── requires_gate, gate_type, auto_approved
├── health_report: dict
└── gate_g4_outcome: GateOutcome
```

---

## 5. Manifest & Knowledge System

### 5.1 Manifest Resolution Hierarchy

```
                    ┌──────────────────────────┐
                    │    Stack Manifest         │  knowledge/manifests/stacks/{domain}.yaml
                    │  domain, tracks, courses  │
                    │  source_family_manifests  │
                    └────────────┬─────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              v                  v                  v
   ┌──────────────────┐ ┌───────────────┐ ┌──────────────────┐
   │ Source Family     │ │Product Manifest│ │ Pedagogy Guidance│
   │ Manifests         │ │ products/     │ │ guidance/pedagogy│
   │ (seed inputs per  │ │ {family}.yaml │ │ core.yaml +      │
   │  channel category)│ │               │ │ profiles/        │
   └──────────────────┘ └───────┬───────┘ └──────────────────┘
                                │
                  ┌─────────────┼─────────────┐
                  v             v             v
         ┌──────────────┐ ┌──────────┐ ┌──────────────┐
         │ Structure    │ │Packaging │ │ Pipeline     │
         │ Profile      │ │Profile   │ │ Definition   │
         │ (hierarchy   │ │(content  │ │ (stages,     │
         │  template)   │ │ types,   │ │  schemas,    │
         │              │ │ surfaces)│ │  review)     │
         └──────────────┘ └──────────┘ └──────────────┘
```

### 5.2 Manifest Types

| Manifest | Location | Drives |
|----------|----------|--------|
| Stack | `manifests/stacks/{domain}.yaml` | Domain identity, tracks, course catalog, source families |
| Product | `manifests/products/{family}.yaml` | Product category, structure/packaging defaults, feature flags |
| Structure Profile | `manifests/structure_profiles/` | Course → Module → Topic hierarchy template |
| Packaging Profile | `manifests/packaging/` | Content types, delivery surfaces, timing model |
| Source Family | `manifests/source_families/` | Channel-organized seed input paths for Loop A |
| Channel | `manifests/channels/` | Feedback channel contracts (categories, targets, digests) |

### 5.3 Knowledge Layer

```
knowledge/
├── manifests/          ← Declarative configuration (checked into git)
│   ├── stacks/         ← Domain definitions (python, ds_ml, genai, ...)
│   ├── products/       ← Product families (default, grit, academy, ...)
│   ├── structure_profiles/
│   ├── packaging/
│   ├── source_families/
│   └── channels/
│
├── sources/            ← Raw intelligence inputs (checked into git)
│   ├── dimension_1_job_outcomes/
│   └── dimension_9_market_and_community/
│
├── guidance/           ← Style & pedagogy guidance (checked into git)
│   ├── pedagogy/       ← core.yaml + profiles/
│   ├── stacks/         ← Stack-specific guidance
│   ├── presentation_surfaces/
│   ├── learning_unit_types/
│   └── brand/
│
├── schemas/            ← JSON schemas for artifact validation
├── catalog/            ← Course catalog CSVs
├── analyses/           ← Analysis outputs
└── raw/                ← Unprocessed reference material

storage/                ← Runtime state (NOT in git)
├── wiki/               ← Compounding intelligence wiki
│   ├── entities/       ← skill, learner, product, competitor, ...
│   ├── stack_profiles/
│   ├── concepts/
│   ├── synthesis/
│   ├── index.md
│   └── log.md
├── artifacts/          ← Generated content artifacts
└── episodes/           ← Episodic memory (cycle results)
```

---

## 6. Runtime Wiki

The wiki is the system's compounding intelligence layer — it persists across cycles and builds cumulative understanding.

**Entity Types**: skill, competitor, audience_segment, concept, domain, product

**Entity Format** (markdown with YAML frontmatter):
```yaml
---
entity_id: skill_python_functions
entity_type: skill
title: Python Functions
confidence: 0.85           # 0.0 – 1.0, decays over time
durability: durable         # durable | perishable | unknown
sources: [dimension_1_job_outcomes/hiring/ml_engineer_requirements.md]
cross_references: [skill_python_basics, skill_decorators]
created_at: 2026-04-18T...
updated_at: 2026-04-18T...
---
```

**Operations**: create, update (delta + reason), supersede (old → new), confidence decay (0.05/cycle for stale entities)

---

## 7. Evaluation & Quality Model

### 5 Evaluation Dimensions

| Dimension | What It Measures |
|-----------|-----------------|
| **Accuracy** | Factual correctness of generated content |
| **Pedagogy** | Learning effectiveness, Bloom alignment, scaffolding |
| **Engagement** | Interest, motivation, relevance to learner |
| **Brand** | Voice, style, formatting consistency |
| **Citation/Provenance** | Source attribution, evidence backing |

Each dimension produces an `EvalScore` (1–5 scale). The `final_score` is the **minimum** across all dimensions (weakest-link model). Pass threshold: **3.5**.

### 4 Human-Approval Gates

| Gate | Loop | Blocking | Approvers |
|------|------|----------|-----------|
| G1 — Strategy Review | A | No (advisory) | Strategy lead |
| G2 — Curriculum Approval | B | Yes | Curriculum architect + SME panel |
| G3 — Content Quality | C | Yes | SME + pedagogy + brand reviewers |
| G4 — High-Severity Fix | D | Yes | Strategy lead |

---

## 8. Pipeline Execution Detail

### Stage Artifact Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                    Per-Stage Execution                       │
│                                                             │
│  ┌─────────────┐    ┌──────────────┐    ┌───────────────┐  │
│  │ Load Stage  │    │ Load Style   │    │   Compose     │  │
│  │ Director    │───>│ Context      │───>│   Prompt      │  │
│  │ Skill       │    │ (5 layers)   │    │               │  │
│  └─────────────┘    └──────────────┘    └───────┬───────┘  │
│                                                  │          │
│                                                  v          │
│                                         ┌───────────────┐  │
│                                         │ Claude LLM    │  │
│                                         │ Generate      │  │
│                                         └───────┬───────┘  │
│                                                  │          │
│                      ┌───────────────────────────┘          │
│                      v                                      │
│             ┌─────────────────┐                             │
│             │ Parse Response  │                             │
│             │ (JSON / YAML)   │                             │
│             └────────┬────────┘                             │
│                      │                                      │
│                      v                                      │
│             ┌─────────────────┐     ┌──────────────────┐   │
│             │ Schema Validate │────>│ Review Against   │   │
│             │ (jsonschema)    │     │ review_focus +   │   │
│             └─────────────────┘     │ success_criteria │   │
│                                     └────────┬─────────┘   │
│                                              │              │
│                              ┌───────┬───────┘              │
│                              │ pass  │ fail                 │
│                              v       v                      │
│                    ┌──────────┐  ┌──────────┐              │
│                    │ Persist  │  │ Revise   │──┐           │
│                    │ Artifact │  │ (retry)  │  │ up to     │
│                    └──────────┘  └──────────┘  │ max_iter  │
│                                       ^────────┘           │
└─────────────────────────────────────────────────────────────┘
```

### Style Layer Composition Order

```
1. Pedagogy Core          ← guidance/pedagogy/core.yaml
2. Pedagogy Profile       ← guidance/pedagogy/profiles/{profile}.yaml
3. Format / Surface       ← guidance/presentation_surfaces/{surface}.yaml
4. Stack / Domain         ← guidance/stacks/{domain}.yaml
5. Brand                  ← guidance/brand/default.yaml
```

---

## 9. Curriculum Data Model

```
CurriculumMap
├── curriculum_id, version, stack_name, domain
├── brief_ref                          ← pointer to design brief
├── total_hours
├── metadata
│
├── courses: list[Course]
│   ├── course_id, title, sequence
│   ├── estimated_hours
│   ├── pedagogy_profile
│   ├── prerequisite_courses
│   ├── content_types
│   ├── skill_ids
│   ├── canonical_course_id            ← for product variants
│   │
│   └── objectives: list[LearningObjective]
│       ├── objective_id, statement
│       ├── bloom_level (REMEMBER → CREATE)
│       └── skill_ids
│
├── capstone_project: dict
└── grand_quiz: dict

ModuleWorkPlan (per module, produced by Loop B)
├── curriculum_id, course_id, module_id, module_title
├── module_change_type
├── estimated_hours
├── pedagogy_profile, instructional_pattern
├── skill_ids, focus_outcomes
├── topic_count
│
├── topics: list[TopicDeliveryPlan]
│   ├── topic_id, title, sequence_within_module
│   ├── estimated_minutes
│   ├── skill_ids, focus_outcomes
│   ├── learning_units: list[ProductionTarget]
│   │   ├── target_scope, target_id, title
│   │   ├── learning_unit_type (9 types)
│   │   ├── instructional_pattern
│   │   ├── assessment_system, assessment_nature
│   │   ├── placement_eligibility_role
│   │   └── question_formats, metadata
│   ├── practice_item: ProductionTarget
│   └── classroom_quiz: ProductionTarget
│
├── module_quiz: ProductionTarget
└── production_targets: list[ProductionTarget]    ← flattened list for Loop C
```

---

## 10. Skill Graph Model

```
SkillGraph
├── graph_id, domain, version, updated_at
│
├── nodes: list[SkillNode]
│   ├── skill_id, name, domain
│   ├── demand_score: float (0–1)
│   ├── durability: DURABLE | PERISHABLE | UNKNOWN
│   ├── prerequisites: list[str]
│   ├── related_skills: list[str]
│   ├── confidence: float (0–1)
│   └── last_updated
│
└── edges: list[SkillEdge]
    ├── from_skill, to_skill
    ├── relationship: prerequisite | related | supersedes
    └── weight: float
```

---

## 11. Feedback Channel System

### 11 Channel Categories

| Category | Type | Example Signals |
|----------|------|-----------------|
| STUDENT_LEARNING | Reactive | Quiz scores, completion rates, struggles |
| CUSTOMER_SUPPORT | Reactive | Tickets about content quality |
| SALES | Reactive | Prospect objections, feature requests |
| SOCIAL_MEDIA | Reactive | Community feedback, mentions |
| PLACEMENT | Reactive | Interview outcomes, employer feedback |
| PLATFORM_ANALYTICS | Proactive | Engagement metrics, drop-off points |
| PERFORMANCE_ANALYTICS | Proactive | Score distributions, time-on-task |
| INTERVIEW_INTEL | Proactive | Interview question patterns, skill demands |
| INTERNAL_TEAM | Reactive | SME feedback, content team notes |
| INDUSTRY_MARKET | Proactive | Job market trends, technology shifts |
| CROSS_PROGRAM | Proactive | Cross-domain learner migration patterns |

### Channel Contract

```
FeedbackChannelContract
├── channel_id, label
├── channel_category: ChannelCategory
├── unit_of_data: str
├── owning_dimensions: list[str]
├── canonical_source_families: list[str]
├── runtime_digests: list[str]
├── knowledge_targets: list[str]          ← wiki entity types to update
└── backprop_targets: list[str]           ← loop nodes to trigger
```

---

## 12. CLI Entry Points

| Command | Description |
|---------|-------------|
| `oacp run` | Full A → B → C → D execution with gate approvals |
| `oacp review-loop {loop_id}` | Execute Loop A or B one node at a time with checkpoints |
| `oacp review-domain` | Execute Loop A + Loop B checkpoint |
| `oacp review` | Execute Loop C one stage at a time |
| `oacp guide` | Show recommended operating mode and example commands |

---

## 13. Key Configuration Constants

| Constant | Value | Purpose |
|----------|-------|---------|
| CONTENT_PASS_THRESHOLD | 3.5 | Minimum eval score to pass |
| MAX_COMPILER_ITERATIONS | 5 | Max revision attempts per stage |
| MAX_REVIEW_ROUNDS | 2 | Max review cycles per artifact |
| MAX_BACKPROP_CYCLES | 3 | Max feedback re-routing iterations |
| DRIFT_THRESHOLD | 0.3 | Signal drift detection sensitivity |
| WIKI_CONFIDENCE_DECAY_RATE | 0.05 | Per-cycle confidence decay for stale entities |
| WIKI_STALE_THRESHOLD_DAYS | 30 | Days before entity considered stale |
| GATE_G3_SAMPLE_RATE | 1.0 | Fraction of artifacts sent to G3 |

---

## 14. Directory Structure

```
open_acp/
├── src/open_acp/
│   ├── cli/                    ← CLI entry point (typer)
│   ├── config/                 ← Constants, curriculum context resolution
│   ├── models/                 ← Pydantic models (state, curriculum, signals, eval, ...)
│   ├── loops/
│   │   ├── loop_a/             ← Intelligence gathering (graph.py, nodes.py)
│   │   ├── loop_b/             ← Curriculum design (graph.py, nodes.py)
│   │   ├── loop_c/             ← Pipeline execution (pipeline_executor.py)
│   │   └── loop_d/             ← Feedback routing (graph.py, nodes.py)
│   ├── orchestrator/
│   │   ├── master_graph.py     ← Master state graph (A→B→C→D)
│   │   ├── router.py           ← BackpropRouter (deterministic fix routing)
│   │   ├── loop_review.py      ← Staged review runner
│   │   └── runner.py           ← PipelineRunner with episodic memory
│   ├── channels/               ← Feedback channel contracts & taxonomy
│   ├── evaluators/             ← 5-dimension eval (accuracy, pedagogy, engagement, brand, citation)
│   ├── gates/                  ← Human-approval gates G1–G4
│   ├── knowledge/              ← WikiEngine (runtime entity CRUD)
│   ├── skills/                 ← Stage director prompts + meta-skills
│   ├── styles/                 ← StyleLoader, PedagogyResolver
│   ├── tools/                  ← Tool registry + tool implementations
│   ├── memory/                 ← Episodic memory store
│   ├── pipeline_defs/          ← Pipeline YAML definitions (per content type)
│   └── utils/                  ← Claude client, helpers
│
├── knowledge/                  ← Declarative knowledge (git-tracked)
│   ├── manifests/              ← Stack, product, structure, packaging, channel configs
│   ├── sources/                ← Raw intelligence inputs
│   ├── guidance/               ← Pedagogy, style, brand guidance
│   ├── schemas/                ← JSON schemas for artifact validation
│   └── catalog/                ← Course catalog reference
│
├── storage/                    ← Runtime state (NOT git-tracked)
│   ├── wiki/                   ← Compounding intelligence wiki
│   ├── artifacts/              ← Generated content
│   └── episodes/               ← Cycle execution records
│
├── tests/
│   ├── unit/                   ← 15 unit test files
│   └── integration/            ← Pipeline integration tests
│
├── docs/architecture/          ← Architecture documentation
└── skills/pipelines/           ← Content-type stage director prompts
```

---

## 15. v9 Three-Tier Model (Domain → Stack → Track)

The system now implements the v9 Design Doc's three-tier conceptual model:

| Tier | Purpose | Manifest Location |
|------|---------|-------------------|
| **Domain** | Organizational grouping, ownership, review routing | `knowledge/manifests/domains/{domain_id}.yaml` |
| **Stack** | Atomic curriculum unit with skill graph and C/L-tagged module catalog | `knowledge/manifests/stacks/{stack_id}.yaml` + `{stack_id}_curriculum_abstract.yaml` |
| **Track** | Product-agnostic catalog combining stacks for career outcome | `knowledge/manifests/tracks/{track_id}.yaml` |

### C/L Tagging System

Modules in stack curriculum abstracts are tagged on two axes:

| C-Tags (Concept Coverage) | L-Tags (Difficulty Level) |
|---|---|
| C1: 80% interview-frequent, must-cover | L1: Entry |
| C2: 20% interview-relevant, should-cover | L2: Intermediate |
| C3: Extensions beyond interview, nice-to-cover | L3: Advanced |

The C × L matrix is intentionally sparse — not every cell is populated.

### Loop A Abstract Production (v9 nodes)

Loop A now produces versioned abstracts in addition to wiki entities:

```
... → derive_market_and_community_digest
    → produce_domain_definition        ← Loads/synthesizes domain manifest
    → update_skill_graph
    → materialize_stack_skill_graph    ← Collects skills into SkillGraph artifact
    → update_learner_model
    → produce_stack_curriculum_abstract ← Generates C/L-tagged module catalog
    → produce_activity_types_library   ← Per-stack activity type catalog
    → update_product_context           ← Now also persists product_abstract.yaml
    → update_wiki_index → END
```

### Loop B Abstract Consumption (v9 nodes)

Loop B now consumes stack abstracts and applies coverage policy:

```
load_wiki_context
    → load_stack_abstracts             ← Loads domain def, stack abstracts, track abstract
    → resolve_product_context → ... → generate_brief (now includes coverage_policy_per_stack)
        → compose_product_specific_curriculum_container
            ← Applies coverage policy (deterministic C×L filtering)
            ← Produces composition_trace (modules selected/dropped, cells, prereq verification)
            ← Persists abstract_versions.yaml (version pinning)
```

### Coverage Policy Engine

`src/open_acp/loops/loop_b/coverage.py` provides deterministic module selection:
- `apply_coverage_policy(abstract, include_tags, include_levels)` — Filters modules by C/L tags
- `verify_cross_stack_prerequisites(selected_modules, available_abstracts)` — Checks cross-stack skill deps

### Design Stage C/L Awareness

- **design_modules**: Inherits `tags`, `concepts`, `interview_frequency`, `pedagogy_profile` from abstract modules
- **design_topics**: Uses abstract `concepts` for topic titles
- **design_practice**: C1 topics get 30% practice time, C2/C3 get 20%
- **design_learning_assessments**: L-tags inform difficulty (L3 → hard, L1 → easy)

### Backprop Router v9 Extension

New fix type `CL_TAG_FIX` routes directly to `produce_stack_curriculum_abstract` in Loop A.
`CURRICULUM_FIX` now also targets `produce_stack_curriculum_abstract`.
All routes include `target_abstracts` field identifying which abstract artifacts are affected.

### New JSON Schemas

- `schemas/domain_definition.schema.json`
- `schemas/stack_curriculum_abstract.schema.json`
- `schemas/track_abstract.schema.json`
- `schemas/composition_trace.schema.json`
- `schemas/learning_path.schema.json`

---

## 16. Design Flow Summary (for diagram generation)

### Flow 1 — Full Cycle Execution (v9)
```
User invokes `oacp run`
  → Master Orchestrator creates run_id + cycle_id
    → Loop A: ingest → patterns → digests → domain_def → skill_graph → materialize_graph
              → learner_model → curriculum_abstract → activity_types → product_context → wiki → G1
      → Loop B: wiki_context → load_stack_abstracts → resolve profiles → brief (with coverage_policy)
                → compose curriculum (coverage filter → composition_trace → version pin)
                → courses → modules (C/L-aware) → topics (concept-grounded) → units → practice → assessments → G2
        → Loop C (per module): load pipeline def → execute stages → schema validate → review → persist → G3
          → Loop D: collect feedback → classify → route fixes (with target_abstracts) → health check → G4
            → (if fixes routed) → re-enter target loop/abstract at target nodes
```

### Flow 2 — Staged Review Mode
```
User invokes `oacp review-loop loop_a`
  → LoopReviewRunner executes one node at a time
    → After each node: checkpoint saved, review packet returned
      → User reviews and approves/requests revision
        → Next node executes
```

### Flow 3 — Backpropagation
```
Loop D classifies insight (e.g., PEDAGOGY_FIX, HIGH severity)
  → BackpropRouter looks up routing table
    → Route: target_loop=B+C, nodes=[resolve_pedagogy_profile, activities], gate=G4, auto=No
      → G4 gate approval requested
        → If approved: re-run target nodes in target loops
```
