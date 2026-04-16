"""Work-plan and assessment taxonomy models for module-first Loop C execution."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class LearningUnitType(str, Enum):
    VIDEO_SESSION_UNIT = "video_session_unit"
    READING_MATERIAL_UNIT = "reading_material_unit"
    MCQ_PRACTICE_UNIT = "mcq_practice_unit"
    CODING_PRACTICE_UNIT = "coding_practice_unit"
    CLASSROOM_QUIZ_UNIT = "classroom_quiz_unit"
    MODULE_QUIZ_UNIT = "module_quiz_unit"
    FINAL_COURSE_QUIZ_UNIT = "final_course_quiz_unit"
    SKILL_ASSESSMENT_UNIT = "skill_assessment_unit"


class InstructionalPattern(str, Enum):
    CONCEPT_EXPLAINER = "concept_explainer"
    PROBLEM_SOLVING = "problem_solving"
    PROJECT_BUILDING = "project_building"
    PLATFORM_WALKTHROUGH = "platform_walkthrough"
    INDUCTION = "induction"


class AssessmentSystem(str, Enum):
    LEARNING = "learning"
    SKILL = "skill"


class AssessmentNature(str, Enum):
    FORMATIVE = "formative"
    SUMMATIVE = "summative"


class PlacementEligibilityRole(str, Enum):
    NONE = "none"
    READINESS_SIGNAL = "readiness_signal"
    WEIGHTED_SIGNAL = "weighted_signal"
    GATING_SIGNAL = "gating_signal"


class ModuleChangeType(str, Enum):
    MODULE_CREATION = "module_creation"
    MODULE_UPDATE = "module_update"


class QuestionFormat(str, Enum):
    SINGLE_CORRECT_MCQ = "single_correct_mcq"
    MULTI_ANSWER_MCQ = "multi_answer_mcq"
    CODE_ANALYSIS_MCQ = "code_analysis_mcq"
    IMAGE_BASED_MCQ = "image_based_mcq"
    FILL_IN_THE_BLANK = "fill_in_the_blank"
    CODING_QUESTION = "coding_question"
    PROJECT = "project"
    SHORT_ANSWER = "short_answer"


class ProductionTarget(BaseModel):
    target_scope: str
    target_id: str
    title: str
    topic_id: Optional[str] = None
    learning_unit_type: Optional[str] = None
    instructional_pattern: Optional[str] = None
    assessment_system: Optional[str] = None
    assessment_nature: Optional[str] = None
    placement_eligibility_role: str = PlacementEligibilityRole.NONE.value
    question_formats: list[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)


class TopicDeliveryPlan(BaseModel):
    topic_id: str
    title: str
    sequence_within_module: int
    estimated_minutes: float
    skill_ids: list[str] = Field(default_factory=list)
    focus_outcomes: list[str] = Field(default_factory=list)
    learning_units: list[dict] = Field(default_factory=list)
    practice_item: Optional[dict] = None
    classroom_quiz: Optional[dict] = None


class ModuleWorkPlan(BaseModel):
    curriculum_id: Optional[str] = None
    curriculum_title: Optional[str] = None
    course_id: Optional[str] = None
    course_title: Optional[str] = None
    module_id: str
    module_title: str
    module_change_type: str = ModuleChangeType.MODULE_CREATION.value
    module_sequence_within_course: Optional[int] = None
    estimated_hours: float = 0.0
    pedagogy_profile: Optional[str] = None
    instructional_pattern: Optional[str] = None
    packaging_profile_id: Optional[str] = None
    skill_ids: list[str] = Field(default_factory=list)
    focus_outcomes: list[str] = Field(default_factory=list)
    topic_count: int = 0
    learning_unit_count: int = 0
    learning_unit_types: list[str] = Field(default_factory=list)
    practice_types: list[str] = Field(default_factory=list)
    classroom_quiz_count: int = 0
    assessment_question_types: list[str] = Field(default_factory=list)
    topics: list[TopicDeliveryPlan] = Field(default_factory=list)
    module_quiz: Optional[dict] = None
    skill_assessment_alignment: dict = Field(default_factory=dict)
    production_targets: list[ProductionTarget] = Field(default_factory=list)
