# Runtime Flow

## Loop A: Intelligence

Loop A ingests signals and updates the system's operating knowledge.

## What `knowledge/sources/` Is For

`knowledge/sources/` is the canonical seeded text-source layer for runtime intelligence.

In practice, it is used for:

- `sources/`
  - stack or domain source documents such as curriculum notes, trend notes, and other reference inputs
- `job_postings/`
  - hiring-signal inputs that help shape skill and placement-oriented understanding
- `competitors/`
  - competitor and market comparison inputs
- `learner/`
  - product-specific or product-aware target-audience inputs

Loop A consumes these inputs primarily through stack manifests, not by blindly scanning the filesystem first.
That means the manifest decides which raw files are canonical for a run, and strict mode can reject runs
that do not have manifest-backed domain inputs.

Stack manifests now point to explicit `source_family_manifests` rather than the older
shared-manifest pattern.
Those source-family manifests describe reusable evidence families such as:

- Dimension 1 job-outcome bootstrap signals
- Dimension 9 market and community bootstrap signals

Loop B also reads some of these raw inputs directly, especially stack curriculum source files such as
`curriculum_sources`.

Important distinction:

- `knowledge/sources/` = canonical seeded text inputs for runtime intelligence
- `knowledge/raw/brand/` = larger style and brand corpus assets used by the style system
- `storage/wiki/` = the runtime knowledge store, not canonical source input

So `knowledge/sources` is not “the wiki,” and it is not the final curriculum output either.
It is the starting evidence layer that Loop A and Loop B reason from.

Important architecture note:

- canonical seeded text inputs now belong under `knowledge/sources/`
- the broader target direction is still to organize non-code inputs under purpose-based root `knowledge/` folders such as:
  - `knowledge/corpus/`
  - `knowledge/analyses/`
  - `knowledge/guidance/`

The older `src/open_acp/knowledge/raw/` tree has been removed from the repo.

See also:

- [Source And Guidance Model](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/source_and_guidance_model.md)
- [Feedback Channels](/Users/pavangangireddy/Desktop/projects/open_acp/docs/architecture/feedback_channels.md)

Bootstrap mode is allowed in Loop A for market, hiring, and competitor signals: if stack-specific inputs are thin or missing, the loop can continue with reusable dimension-family seed sources, surface explicit coverage warnings, and let the runtime knowledge store compound from those inputs instead of blocking execution.

Here, "shared" means the **source family is reusable across stacks**.
It does not mean the evidence cannot still carry stack identifiers or stack-specific exports.

Important exception:

- explicit product runs should not bootstrap learner context from a shared persona seed
- explicit product runs should not bootstrap target-audience context from a shared persona seed
- `update_learner_model` should fail when a product run has no product-specific canonical learner inputs
  and no canonical product-specific target-audience sources

Within Loop A, the intended chain is: signals -> detected patterns -> wiki entity updates. Pattern detection should actively guide later skill, learner, and competitor extraction instead of being treated as a disconnected side report.

Planned next step:

- Loop A should gradually derive dimension-specific digests before entity updates
- the first intended digest is `skill_outcomes_signal_digest` for Dimension 1
- later dimensions should follow the same model rather than bypassing it
- high-volume channels such as interview intelligence should prefer canonical aggregated exports or normalized snapshots instead of direct raw-event ingestion in the first implementation wave

TODO:

- add an explicit human review capture step for detected-pattern quality and correctness
- persist that operator feedback into runtime storage so later runs can learn from accepted, corrected, or rejected patterns
- connect that feedback into the longer-term feedback store rather than keeping it only inside review packets

The current intended Loop A flow is:

1. ingest signals
2. detect patterns
3. derive skill outcomes digest
4. derive market and community digest
5. update skill graph
6. update learner model
7. update product context
8. update wiki index

Market and competitor signals are now expected to influence Loop A primarily through
`market_and_community_digest`, not through a standalone competitor-entity update stage.

Product note:

- product and structure manifests are canonical
- Loop A writes only a derived runtime summary into the runtime knowledge store for explicit products
- stack-only runs skip product wiki writes and keep moving
- for clean simulations, it is valid to reset `storage/wiki` and rebuild runtime knowledge from scratch
- explicit product runs should carry product-specific learner inputs instead of relying on any shared learner seed
- explicit product runs should carry product-specific target-audience inputs instead of relying on any shared learner seed

Knowledge-model note:

- Loop A now updates both canonical skill entities and stack-scoped skill overlay profiles
- the canonical entity answers “what is this skill in general?”
- the stack overlay answers “what role does this skill play in this stack?”

Typical outputs:

- wiki entries
- drift observations
- skill or market updates
- learner or competitor signals

Learner-model note:

- `update_learner_model` is a runtime materialization step, not the canonical source of target-audience profiles
- canonical target-audience inputs should come from product-aware sources and manifests
- the runtime knowledge store should hold the derived audience summary or overlay, not invent the base learner definition from a generic shared seed

## Loop B: Curriculum

Loop B translates intelligence into instructional structure.

It is responsible for:

- curriculum mapping
- curriculum change visibility
- packaging-aware course, module, topic, and learning-unit design
- pedagogy profile resolution
- practice and learning-assessment design
- external skill-assessment requirement resolution
- learning-to-skill assessment alignment

This layer should decide the educational shape of the output before content generation begins.

The current intended Loop B flow is:

1. load wiki context
   - wiki skill summaries
   - learner summaries
   - Dimension 1 digest summary
   - Dimension 9 digest summary
2. resolve product context
3. resolve structure profile
4. resolve packaging profile
5. resolve design-priority profile
6. resolve time-budget context
7. resolve pedagogy profile
8. generate brief
9. generate curriculum
10. compare curriculum changes
11. design courses
12. design modules
13. design topics
14. design learning units
15. design practice
16. design learning assessments
17. resolve skill-assessment requirements
18. align learning with skill assessments


Brief-first note:

- `generate_brief` should be the first true design artifact in Loop B
- `compose_product_specific_curriculum_container` should consume that brief plus structural inputs, not directly redo all upstream interpretation work
- `generate_brief` and `compose_product_specific_curriculum_container` should consume both:
  - wiki-derived skill / learner context
  - synthesized dimension digests such as `skill_outcomes_signal_digest` and `market_and_community_digest`
- downstream design stages should keep inheriting from the brief and curriculum artifacts instead of re-reading raw context
- `compose_product_specific_curriculum_container` now emits packaged `courses` as its native structure output
- `compose_product_specific_curriculum_container` should output packaged course structure, not explicit level objects
- source-defined levels or phases should act as ordering and scope cues for courses, not as mandatory output fields
- topic placement should be decided later and should eventually be informed by channel-analysis digests
- `compose_product_specific_curriculum_container` should read canonical stack course definitions plus any declared
  `course_variants`, `product_only_courses`, and `course_variant_overrides`
- `brief.yaml` and `curriculum.yaml` should be persisted under `storage/design/<domain>/<cycle_id>/`
- downstream course/module/topic/unit stages should persist:
  - `courses/index.yaml` and `course.<id>.yaml`
  - `modules/index.yaml` and `module.<id>.yaml`
  - `topics/index.yaml` and `topic.<id>.yaml`
  - `units/index.yaml` and `unit.<id>.yaml`
- downstream practice/assessment stages should persist:
  - `practice.yaml`
  - `learning_assessments.yaml`
  - `skill_assessment_requirements.yaml`
  - `assessment_alignment.yaml`
- downstream Loop B stages should increasingly reload those artifacts instead of trusting only in-memory state
- curriculum generation now includes a strict hours validator against:
  - packaging / time-budget target hours
  - curriculum total hours
  - sum of course hours, capstone hours, and grand quiz hours
- if the first parsed Stage 1 curriculum fails that validator, the system may run one structured repair pass, but only a validator-clean artifact may be persisted as the accepted curriculum

Runtime policy note:

- for real product-driven runs, Loop B should eventually stop if product context is missing
- for real domain runs, Loop A and Loop B should eventually stop if domain-specific canonical inputs are missing instead of borrowing unrelated defaults
- for explicit product runs, pedagogy resolution should prefer canonical product pedagogy overrides before falling back to stack-level pedagogy defaults

## Loop C: Content Production

Loop C executes a stage-based pipeline for a chosen content type.

The stage lifecycle is:

1. load stage instructions
2. inject module, style, and prior artifact context
3. generate artifact
4. parse and validate artifact
5. review against declared criteria
6. revise if needed
7. persist accepted artifact

For stricter pipelines, schema and review failures should block progress rather than merely producing warnings.

Loop C consumes the course-native curriculum output plus the downstream module/topic/unit design artifacts.
Its runtime context should include:

- selected course context
- selected module context
- selected topic context
- learning unit type
- practice intent
- learning-assessment context

So the effect on Loop C is architectural now, even where the repo has not fully migrated every content pipeline to those richer inputs yet.

Loop B knowledge note:

- Loop B can now consume both canonical skill context and stack-profile summaries from the runtime knowledge store
- this is still a lightweight context feed, not yet a full stack-graph retrieval system

Guidance note:

- Loop C now loads runtime playbooks from `knowledge/guidance/` through the loader code in `src/open_acp/styles/`
- the data path is no longer inside `src/`
- the current runtime guidance contract is composed from:
  - pedagogy core
  - pedagogy profile
  - teaching-mode contract
  - learning unit type guidance
  - presentation surface guidance
  - instructional pattern guidance
  - domain guidance
  - brand guidance
- product and packaging overlays are still later work

## Loop D: Evaluation and Backpropagation

Loop D evaluates outputs and decides what kind of remediation is needed.

Typical results:

- content fixes
- pedagogy fixes
- brand fixes
- curriculum fixes

The long-term goal is not only to score outputs, but to create reliable improvement work that can be routed back into the right loop or stage.

This means Loop D should eventually become more specific about Loop B targets.

Instead of routing only to broad curriculum nodes, it should be able to point remediation toward:

- curriculum generation
- packaging resolution
- module design
- topic design
- learning-unit design
- practice design
- learning-assessment design
- skill-assessment alignment

## Inner vs Outer Agentic Behavior

Open ACP should remain:

- deterministic at the loop-routing level
- agentic at the stage-execution level

That split keeps the system understandable while still letting stage-level generation and review benefit from model reasoning.

## Recommended Operating Mode

For real product, curriculum, and content work, Open ACP should be run in staged review mode.

Recommended order:

1. `review-loop loop_a`
2. `review-loop loop_b`
3. `review` for Loop C
4. `run --full` only after earlier checkpoints are reviewed

This is the intended “agentic way” to operate the system:

- one loop node at a time in Loop A and Loop B
- one stage at a time in Loop C
- explicit review packets before proceeding

The repo should treat full unattended execution as secondary.
The primary operating pattern is:

- inspect signals
- inspect detected patterns
- inspect curriculum decisions
- inspect content artifacts
- then proceed

Helpful operator commands:

- `oacp guide`
- `oacp review-loop loop_a --domain genai --cycle-id genai_niat_b3_v1 --product-family NIAT --product-version B3`
- `oacp review-loop loop_b --domain genai --content-type concept_explainer --cycle-id genai_niat_b3_v1 --product-family NIAT --product-version B3`
- `oacp review --content-type concept_explainer --domain genai --title "How Retrieval-Augmented Generation Works" --module-id rag_intro --hours 1.0`
