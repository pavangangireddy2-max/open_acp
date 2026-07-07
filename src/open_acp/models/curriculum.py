"""Curriculum domain models: objectives, assessments, courses, and curriculum maps."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class BloomLevel(str, Enum):
    REMEMBER = "remember"
    UNDERSTAND = "understand"
    APPLY = "apply"
    ANALYZE = "analyze"
    EVALUATE = "evaluate"
    CREATE = "create"


class LearningObjective(BaseModel):
    objective_id: str
    statement: str
    bloom_level: BloomLevel
    skill_ids: list[str]


class Assessment(BaseModel):
    assessment_id: str
    type: str  # "quiz" | "coding" | "project" | "peer_review"
    objectives_assessed: list[str]
    rubric: dict
    time_limit_minutes: Optional[int] = None


class SourceModule(BaseModel):
    """Traces a course's module back to its stack curriculum abstract origin."""
    stack: str
    abstract_ref: str  # AbstractModule.module_id
    tags: list[str] = Field(default_factory=list)  # e.g. ["C1", "L1"]


class Course(BaseModel):
    course_id: str
    title: str
    sequence: int
    objectives: list[LearningObjective]
    estimated_hours: float
    pedagogy_profile: Optional[str] = None
    prerequisite_courses: list[str] = Field(default_factory=list)
    content_types: list[str] = []
    skill_ids: list[str] = []
    canonical_course_id: Optional[str] = None
    course_variant_id: Optional[str] = None
    course_kind: str = "stack_course"
    course_variant_reason: Optional[str] = None
    source_modules: list[SourceModule] = Field(default_factory=list)
    domain_rollup: list[str] = Field(default_factory=list)
    origin: Optional[str] = None  # "stack" | "product_addon" | "refresher"


class ParallelTrack(BaseModel):
    """A parallel track within a learning phase."""
    courses: list[str] = Field(default_factory=list)
    weekly_hours: Optional[float] = None
    active_weeks: list[int] = Field(default_factory=list)


class LearningPhase(BaseModel):
    """A phase in the learning path with sequencing and parallelism."""
    phase_id: str
    title: str
    sequence: int
    duration_weeks: Optional[float] = None
    courses: list[str] = Field(default_factory=list)  # course_ids
    units: list[str] = Field(default_factory=list)  # standalone unit_ids (capstone, grand_quiz)
    parallelism: str = "sequential"  # "sequential" | "partial" | "na"
    parallel_tracks: list[ParallelTrack] = Field(default_factory=list)
    transition_gate: Optional[str] = None
    purpose: Optional[str] = None


class StackProgression(BaseModel):
    """When a stack enters and exits the learning path."""
    stack_id: str
    enters_phase: str
    exits_phase: str
    role: str = "core"  # "core" | "supplementary"


class WeeklyLoadEntry(BaseModel):
    """Weekly load for a single week."""
    week: int
    hours: float
    active_courses: list[str] = Field(default_factory=list)


class LearningPath(BaseModel):
    """Learning path with phases, parallelism, and stack progression."""
    total_duration_weeks: Optional[int] = None
    target_weekly_hours: Optional[float] = None
    max_concurrent_courses: int = 2
    phases: list[LearningPhase] = Field(default_factory=list)
    stack_progression: list[StackProgression] = Field(default_factory=list)
    weekly_load_profile: list[WeeklyLoadEntry] = Field(default_factory=list)


class DroppedModule(BaseModel):
    """Record of a module dropped during composition."""
    stack: str
    module: str
    reason: str


class CompositionTrace(BaseModel):
    """Audit trail of how curriculum was composed from stack abstracts."""
    contributing_stacks: list[str] = Field(default_factory=list)
    modules_selected_per_stack: dict[str, list[str]] = Field(default_factory=dict)
    modules_dropped: list[DroppedModule] = Field(default_factory=list)
    coverage_cells_selected_per_stack: dict[str, list[str]] = Field(default_factory=dict)
    refreshers_added: list[str] = Field(default_factory=list)
    addons_injected: list[dict] = Field(default_factory=list)
    cross_stack_prereq_verification: dict = Field(default_factory=dict)
    abstract_versions_pinned: dict[str, int] = Field(default_factory=dict)


class CurriculumMap(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    curriculum_id: str
    version: int = 1
    brief_ref: Optional[str] = None
    packaging_profile_ref: Optional[str] = None
    stack_name: str
    domain: str
    composition_mode: str = "single_stack"  # "single_stack" | "multi_stack"
    courses: list[Course]
    capstone_project: dict = Field(default_factory=dict)
    grand_quiz: dict = Field(default_factory=dict)
    total_hours: float
    hours_check: dict = Field(default_factory=dict)
    composition_trace: Optional[CompositionTrace] = None
    learning_path: Optional[LearningPath] = None
    created_at: str = ""
    approved_at: Optional[str] = None

    def get_course(self, course_id: str) -> Optional[Course]:
        """Look up a course by its ID."""
        for course in self.courses:
            if course.course_id == course_id:
                return course
        return None
