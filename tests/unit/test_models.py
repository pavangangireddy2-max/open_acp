"""Unit tests for all Pydantic domain models."""
import pytest
from datetime import datetime, UTC


# ── Content Types ──────────────────────────────────────────────────────────────

def test_content_type_enum():
    from open_acp.models.content_types import ContentType, PipelineFamily, normalize_content_type

    assert len(ContentType) == 16
    assert ContentType.CONCEPT_EXPLAINER.family == PipelineFamily.SESSION
    assert ContentType.READING_MATERIAL.family == PipelineFamily.WRITTEN
    assert ContentType.MCQ_PRACTICE.family == PipelineFamily.PRACTICE
    assert ContentType.CLASSROOM_QUIZ.family == PipelineFamily.ASSESSMENT
    assert ContentType.SKILL_ASSESSMENT.family == PipelineFamily.ASSESSMENT
    assert ContentType.GRADED_ASSESSMENT.family == PipelineFamily.ASSESSMENT
    assert normalize_content_type("fortnight_quiz") == "skill_assessment"
    assert normalize_content_type("graded_assessment") == "graded_assessment"


def test_pipeline_family_enum():
    from open_acp.models.content_types import PipelineFamily

    assert len(PipelineFamily) == 4


def test_delivery_taxonomy_enums():
    from open_acp.models.delivery import (
        AssessmentNature,
        AssessmentSystem,
        InstructionalPattern,
        LearningUnitType,
        ModuleChangeType,
        PlacementEligibilityRole,
        QuestionFormat,
    )

    assert LearningUnitType.VIDEO_SESSION_UNIT.value == "video_session_unit"
    assert LearningUnitType.GRADED_ASSESSMENT_UNIT.value == "graded_assessment_unit"
    assert InstructionalPattern.CONCEPT_EXPLAINER.value == "concept_explainer"
    assert AssessmentSystem.SKILL.value == "skill"
    assert AssessmentNature.SUMMATIVE.value == "summative"
    assert ModuleChangeType.MODULE_UPDATE.value == "module_update"
    assert PlacementEligibilityRole.GATING_SIGNAL.value == "gating_signal"
    assert QuestionFormat.MULTI_ANSWER_MCQ.value == "multi_answer_mcq"


def test_module_work_plan():
    from open_acp.models.delivery import ModuleWorkPlan, ProductionTarget, TopicDeliveryPlan

    plan = ModuleWorkPlan(
        curriculum_id="cur_1",
        curriculum_title="GenAI Stack Curriculum",
        course_id="course_1",
        course_title="Foundations",
        module_id="module_1",
        module_title="Foundations — Core workflow",
        module_change_type="module_creation",
        instructional_pattern="concept_explainer",
        topic_count=1,
        learning_unit_count=2,
        learning_unit_types=["reading_material_unit", "video_session_unit"],
        assessment_question_types=["mcq", "fib"],
        topics=[
            TopicDeliveryPlan(
                topic_id="topic_1",
                title="Problem Framing",
                sequence_within_module=1,
                estimated_minutes=30,
                learning_units=[
                    {"learning_unit_id": "topic_1_u1", "unit_type": "reading_material_unit"},
                    {"learning_unit_id": "topic_1_u2", "unit_type": "video_session_unit"},
                ],
                classroom_quiz={"question_types": ["mcq", "fib"]},
            )
        ],
        production_targets=[
            ProductionTarget(
                target_scope="learning_unit",
                target_id="topic_1_u2",
                title="Problem Framing — Instructor-led PPT session",
                learning_unit_type="video_session_unit",
                instructional_pattern="concept_explainer",
            )
        ],
    )

    dumped = plan.model_dump()
    assert dumped["module_title"] == "Foundations — Core workflow"
    assert dumped["topics"][0]["learning_units"][1]["unit_type"] == "video_session_unit"
    assert dumped["production_targets"][0]["instructional_pattern"] == "concept_explainer"


# ── Curriculum ─────────────────────────────────────────────────────────────────

def test_bloom_level():
    from open_acp.models.curriculum import BloomLevel

    assert BloomLevel.REMEMBER.value == "remember"
    assert len(BloomLevel) == 6


def test_learning_objective():
    from open_acp.models.curriculum import LearningObjective, BloomLevel

    obj = LearningObjective(
        objective_id="obj_1",
        statement="Apply binary search to sorted arrays",
        bloom_level=BloomLevel.APPLY,
        skill_ids=["skill_binary_search"],
    )
    assert obj.bloom_level == BloomLevel.APPLY
    assert obj.model_dump()["objective_id"] == "obj_1"


def test_course():
    from open_acp.models.curriculum import Course, LearningObjective, BloomLevel

    course = Course(
        course_id="c1",
        title="Introduction to Algorithms",
        sequence=1,
        objectives=[
            LearningObjective(
                objective_id="obj_1",
                statement="Understand time complexity",
                bloom_level=BloomLevel.UNDERSTAND,
                skill_ids=["skill_tc"],
            )
        ],
        estimated_hours=4.0,
        prerequisite_courses=[],
        content_types=["concept_explainer"],
        skill_ids=["skill_tc"],
    )
    assert course.sequence == 1
    dumped = course.model_dump()
    assert dumped["title"] == "Introduction to Algorithms"


def test_curriculum_map():
    from open_acp.models.curriculum import Course, CurriculumMap

    cmap = CurriculumMap(
        curriculum_id="cur_1",
        version=1,
        program_name="ML Engineering",
        domain="ml-engineering",
        pedagogy_profile="concept_progression",
        pedagogy_rationale="Progressive conceptual sequencing",
        differentiation_strategy={"focus": "hands-on"},
        courses=[
            Course(
                course_id="c1",
                title="Programming Foundations",
                sequence=1,
                objectives=[],
                estimated_hours=20.0,
                prerequisite_courses=[],
                content_types=["concept_explainer"],
                skill_ids=["python"],
            )
        ],
        total_hours=40.0,
        created_at=datetime.now(UTC).isoformat(),
    )
    assert cmap.get_course("c1") is not None
    assert cmap.approved_at is None
    assert cmap.pedagogy_profile == "concept_progression"
    assert cmap.courses[0].course_id == "c1"


# ── Signals ────────────────────────────────────────────────────────────────────

def test_channel_category():
    from open_acp.models.signals import ChannelCategory, ChannelType

    assert len(ChannelCategory) == 11
    assert ChannelType.REACTIVE.value == "reactive"


def test_raw_signal():
    from open_acp.models.signals import RawSignal, ChannelCategory, ChannelType

    sig = RawSignal(
        signal_id="sig_1",
        channel_category=ChannelCategory.STUDENT_LEARNING,
        channel_name="Queries team",
        content="Students struggle with recursion",
        timestamp=datetime.now(UTC).isoformat(),
        signal_type=ChannelType.REACTIVE,
        metadata={},
    )
    assert sig.channel_category == ChannelCategory.STUDENT_LEARNING


def test_signal_batch():
    from open_acp.models.signals import SignalBatch

    batch = SignalBatch(
        batch_id="batch_1",
        signals=[],
        ingested_at=datetime.now(UTC).isoformat(),
        source_domain="ml-engineering",
    )
    assert len(batch.signals) == 0


# ── Skill Graph ────────────────────────────────────────────────────────────────

def test_skill_node():
    from open_acp.models.skill_graph import SkillNode, DurabilityRating

    node = SkillNode(
        skill_id="sk_1",
        name="Python",
        domain="programming",
        demand_score=0.85,
        durability=DurabilityRating.DURABLE,
        prerequisites=[],
        related_skills=["sk_2"],
        confidence=0.9,
        last_updated=datetime.now(UTC).isoformat(),
    )
    assert node.demand_score == 0.85


def test_skill_graph():
    from open_acp.models.skill_graph import SkillGraph

    graph = SkillGraph(
        graph_id="g1",
        nodes=[],
        edges=[],
        domain="ml-engineering",
        version=1,
        updated_at=datetime.now(UTC).isoformat(),
    )
    assert graph.version == 1


# ── Learner ────────────────────────────────────────────────────────────────────

def test_learner_persona():
    from open_acp.models.learner import LearnerPersona, KnowledgeGap

    persona = LearnerPersona(
        persona_id="p1",
        name="Career Switcher",
        description="Non-CS background moving to tech",
        prior_knowledge=["basic math"],
        knowledge_gaps=[
            KnowledgeGap(topic="data structures", severity="moderate", evidence="survey")
        ],
        misconceptions=[],
        motivation_drivers=["career growth"],
        learning_preferences=["visual"],
    )
    assert len(persona.knowledge_gaps) == 1


# ── Competitor ─────────────────────────────────────────────────────────────────

def test_competitor_map():
    from open_acp.models.competitor import CompetitorMap

    cmap = CompetitorMap(
        map_id="cm1",
        domain="ml-engineering",
        competitors=[],
        our_positioning="Practice-first",
        gaps=["advanced MLOps"],
        updated_at=datetime.now(UTC).isoformat(),
    )
    assert cmap.domain == "ml-engineering"


# ── Evaluation ─────────────────────────────────────────────────────────────────

def test_eval_dimension():
    from open_acp.models.evaluation import EvalDimension

    assert len(EvalDimension) == 5
    assert EvalDimension.ACCURACY.value == "accuracy"


def test_eval_report():
    from open_acp.models.evaluation import EvalReport, EvalScore, EvalDimension

    report = EvalReport(
        report_id="er1",
        content_type="concept_explainer",
        module_id="m1",
        scores=[
            EvalScore(dimension=EvalDimension.ACCURACY, score=4.0, evidence="good", failing_elements=[]),
            EvalScore(dimension=EvalDimension.PEDAGOGY, score=3.5, evidence="ok", failing_elements=[]),
        ],
        final_score=3.5,
        passed=True,
        iteration=1,
        evaluated_at=datetime.now(UTC).isoformat(),
    )
    assert report.passed is True
    assert report.final_score == 3.5


# ── Feedback ───────────────────────────────────────────────────────────────────

def test_fix_type_and_severity():
    from open_acp.models.feedback import FixType, Severity

    assert len(FixType) == 5
    assert len(Severity) == 4


def test_insight_classification():
    from open_acp.models.feedback import InsightClassification, FixType, Severity

    insight = InsightClassification(
        insight_id="ins_1",
        fix_type=FixType.CONTENT_FIX,
        severity=Severity.HIGH,
        description="Inaccurate example in module 3",
        source_channels=["student_learning"],
        evidence="3 students flagged same issue",
        created_at=datetime.now(UTC).isoformat(),
    )
    assert insight.fix_type == FixType.CONTENT_FIX


def test_fix_route():
    from open_acp.models.feedback import FixRoute, FixType, Severity, InsightClassification

    insight = InsightClassification(
        insight_id="ins_1",
        fix_type=FixType.BRAND_FIX,
        severity=Severity.LOW,
        description="Tone inconsistency",
        source_channels=["internal_team"],
        evidence="Brand lead flagged",
        created_at=datetime.now(UTC).isoformat(),
    )
    route = FixRoute(
        route_id="r1",
        fix_type=FixType.BRAND_FIX,
        severity=Severity.LOW,
        target_loop="C",
        target_nodes=["brand_polish"],
        target_stages=["brand_polish"],
        requires_gate=True,
        gate_type="G3",
        auto_approved=True,
        insight=insight,
        created_at=datetime.now(UTC).isoformat(),
    )
    assert route.auto_approved is True


# ── Gates ──────────────────────────────────────────────────────────────────────

def test_gate_outcome():
    from open_acp.models.gates import GateOutcome, GateType, GateDecision

    outcome = GateOutcome(
        gate_type=GateType.G2,
        decision=GateDecision.APPROVE,
        approver="Curriculum Architect",
        reason="Looks good",
        decided_at=datetime.now(UTC).isoformat(),
    )
    assert outcome.decision == GateDecision.APPROVE


# ── Wiki ───────────────────────────────────────────────────────────────────────

def test_wiki_entity():
    from open_acp.models.wiki import WikiEntity, EntityType, WikiConfidence

    entity = WikiEntity(
        entity_id="skill_python",
        entity_type=EntityType.SKILL,
        title="Python Programming",
        content="A versatile programming language...",
        confidence=WikiConfidence(
            score=0.9,
            sources_count=5,
            last_verified=datetime.now(UTC).isoformat(),
            durability="durable",
        ),
        sources=["job_posting_1", "industry_report_3"],
        cross_references=["skill_ml", "skill_data_science"],
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat(),
    )
    assert entity.entity_type == EntityType.SKILL
    assert entity.confidence.score == 0.9


# ── Artifacts ──────────────────────────────────────────────────────────────────

def test_stage_artifact():
    from open_acp.models.artifacts import StageArtifact

    artifact = StageArtifact(
        artifact_id="art_1",
        stage_id="outline",
        pipeline_id="concept_explainer",
        content_type="concept_explainer",
        data={"sections": [], "teaching_flow": "progressive"},
        schema_path="outline.schema.json",
        created_at=datetime.now(UTC).isoformat(),
    )
    assert artifact.validated is False


# ── State ──────────────────────────────────────────────────────────────────────

def test_pipeline_state():
    from open_acp.models.state import PipelineState

    state = PipelineState(
        pipeline_id="concept_explainer",
        content_type="concept_explainer",
        current_stage="outline",
    )
    assert state.iteration == 1
    assert state.status == "in_progress"
    assert state.stage_artifacts == {}


def test_master_state():
    from open_acp.models.state import MasterState

    state = MasterState(
        run_id="run_1",
        cycle_id="cycle_1",
        domain="ml-engineering",
    )
    assert state.current_loop == "A"
    assert state.iteration_count == 0
    assert state.completed_loops == []


def test_loop_states_instantiate():
    from open_acp.models.state import LoopAState, LoopBState, LoopCState, LoopDState

    a = LoopAState(cycle_id="c1", domain="ml")
    b = LoopBState(cycle_id="c1", domain="ml")
    c = LoopCState(cycle_id="c1", domain="ml")
    d = LoopDState(cycle_id="c1")

    assert a.drift_score == 0.0
    assert b.pedagogy_profile is None
    assert c.content_type == "concept_explainer"
    assert d.fix_routes == []


# ── Serialization roundtrip ────────────────────────────────────────────────────

def test_all_models_serialize_deserialize():
    """Verify all key models survive a model_dump -> model_validate roundtrip."""
    from open_acp.models.curriculum import CurriculumMap
    from open_acp.models.skill_graph import SkillGraph
    from open_acp.models.state import MasterState

    for ModelClass, kwargs in [
        (CurriculumMap, dict(
            curriculum_id="c1", version=1, program_name="Test", domain="test",
            pedagogy_profile="concept_progression", pedagogy_rationale="test",
            differentiation_strategy={}, courses=[], total_hours=10,
            created_at=datetime.now(UTC).isoformat(),
        )),
        (SkillGraph, dict(
            graph_id="g1", nodes=[], edges=[], domain="test",
            version=1, updated_at=datetime.now(UTC).isoformat(),
        )),
        (MasterState, dict(
            run_id="r1", cycle_id="c1", domain="test",
        )),
    ]:
        instance = ModelClass(**kwargs)
        dumped = instance.model_dump()
        restored = ModelClass.model_validate(dumped)
        assert restored == instance
