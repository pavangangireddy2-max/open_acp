"""Pipeline and loop state models for the 4-loop orchestrator."""

from typing import Optional

from pydantic import BaseModel, ConfigDict

from open_acp.models.artifacts import StageArtifact
from open_acp.models.curriculum import CurriculumMap
from open_acp.models.evaluation import EvalReport
from open_acp.models.feedback import FixRoute, InsightClassification
from open_acp.models.gates import GateOutcome
from open_acp.models.learner import LearnerModel
from open_acp.models.signals import SignalBatch
from open_acp.models.skill_graph import SkillGraph


class PipelineState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    pipeline_id: str
    content_type: str
    current_stage: str
    stage_artifacts: dict[str, StageArtifact] = {}
    iteration: int = 1
    status: str = "in_progress"


class LoopAState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    cycle_id: str
    domain: str
    product_family: Optional[str] = None
    product_version: Optional[str] = None
    require_product_context: bool = False
    strict_domain_inputs: bool = False
    signal_batch: Optional[SignalBatch] = None
    bootstrap_warnings: list[str] = []
    detected_patterns: list[dict] = []
    pattern_detection_status: str = "not_started"
    pattern_detection_note: Optional[str] = None
    drift_score: float = 0.0
    skill_outcomes_signal_digest: Optional[dict] = None
    skill_outcomes_digest_artifact_path: Optional[str] = None
    market_and_community_digest: Optional[dict] = None
    market_and_community_digest_artifact_path: Optional[str] = None
    product_context: Optional[dict] = None
    structure_profile: Optional[dict] = None
    wiki_entries_created: list[str] = []
    wiki_entries_updated: list[str] = []
    stack_profiles_created: list[str] = []
    stack_profiles_updated: list[str] = []
    # v9 abstract artifacts
    domain_definition: Optional[dict] = None
    domain_definition_artifact_path: Optional[str] = None
    stack_skill_graph: Optional[dict] = None
    stack_skill_graph_artifact_path: Optional[str] = None
    stack_curriculum_abstract: Optional[dict] = None
    stack_curriculum_abstract_artifact_path: Optional[str] = None
    activity_types_library: Optional[dict] = None
    activity_types_library_artifact_path: Optional[str] = None
    gate_g1_outcome: Optional[GateOutcome] = None


class LoopBState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    cycle_id: str
    domain: str
    product_family: Optional[str] = None
    product_version: Optional[str] = None
    require_product_context: bool = False
    strict_domain_inputs: bool = False
    skill_graph: Optional[SkillGraph] = None
    learner_model: Optional[LearnerModel] = None
    skill_outcomes_signal_digest: Optional[dict] = None
    market_and_community_digest: Optional[dict] = None
    curriculum_source_context: str = ""
    skill_outcomes_context: str = ""
    market_and_community_context: str = ""
    # v9 abstract inputs
    domain_definition: Optional[dict] = None
    stack_abstracts: Optional[dict] = None  # stack_id -> StackCurriculumAbstract dict
    track_abstract: Optional[dict] = None
    coverage_policy: Optional[dict] = None  # stack_id -> {include_tags, include_levels}
    product_context: Optional[dict] = None
    structure_profile: Optional[dict] = None
    design_priority_profile: Optional[dict] = None
    time_budget_context: Optional[dict] = None
    pedagogy_profile: Optional[str] = None
    brief_generation_status: str = "not_started"
    brief_generation_note: Optional[str] = None
    brief_generation_raw_response: Optional[str] = None
    brief: Optional[dict] = None
    brief_artifact_path: Optional[str] = None
    curriculum_generation_status: str = "not_started"
    curriculum_generation_note: Optional[str] = None
    curriculum_generation_raw_response: Optional[str] = None
    previous_curriculum_map: Optional[dict] = None
    curriculum_map: Optional[CurriculumMap] = None
    curriculum_artifact_path: Optional[str] = None
    curriculum_validation_report: Optional[dict] = None
    design_artifact_paths: Optional[dict] = None
    curriculum_change_report: Optional[dict] = None
    packaging_profile: Optional[dict] = None
    course_design: Optional[dict] = None
    course_design_artifact_path: Optional[str] = None
    module_design: Optional[dict] = None
    module_design_artifact_path: Optional[str] = None
    topic_design: Optional[dict] = None
    topic_design_artifact_path: Optional[str] = None
    learning_unit_plan: Optional[dict] = None
    learning_unit_plan_artifact_path: Optional[str] = None
    practice_design: Optional[dict] = None
    practice_design_artifact_path: Optional[str] = None
    learning_assessment_plan: Optional[dict] = None
    learning_assessment_plan_artifact_path: Optional[str] = None
    skill_assessment_requirements: Optional[dict] = None
    skill_assessment_requirements_artifact_path: Optional[str] = None
    assessment_alignment_report: Optional[dict] = None
    assessment_alignment_report_artifact_path: Optional[str] = None
    gate_g2_outcome: Optional[GateOutcome] = None


class LoopCState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    cycle_id: str
    domain: str
    content_type: str = "concept_explainer"
    curriculum_map: Optional[CurriculumMap] = None
    current_module_id: Optional[str] = None
    pipeline_state: Optional[PipelineState] = None
    eval_report: Optional[EvalReport] = None
    gate_g3_outcome: Optional[GateOutcome] = None


class LoopDState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    cycle_id: str
    raw_feedback: list[dict] = []
    insights: list[InsightClassification] = []
    fix_routes: list[FixRoute] = []
    health_report: dict = {}
    gate_g4_outcome: Optional[GateOutcome] = None


class MasterState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    run_id: str
    cycle_id: str
    domain: str
    current_loop: str = "A"
    iteration_count: int = 0
    escalations: list[dict] = []
    completed_loops: list[str] = []
