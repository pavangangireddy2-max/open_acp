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
    signal_batch: Optional[SignalBatch] = None
    detected_patterns: list[dict] = []
    drift_score: float = 0.0
    wiki_entries_created: list[str] = []
    wiki_entries_updated: list[str] = []
    gate_g1_outcome: Optional[GateOutcome] = None


class LoopBState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    cycle_id: str
    domain: str
    skill_graph: Optional[SkillGraph] = None
    learner_model: Optional[LearnerModel] = None
    pedagogy_profile: Optional[str] = None
    curriculum_map: Optional[CurriculumMap] = None
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
