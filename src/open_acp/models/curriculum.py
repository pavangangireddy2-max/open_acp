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


class CurriculumMap(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    curriculum_id: str
    version: int = 1
    brief_ref: Optional[str] = None
    packaging_profile_ref: Optional[str] = None
    stack_name: str
    domain: str
    courses: list[Course]
    capstone_project: dict = Field(default_factory=dict)
    grand_quiz: dict = Field(default_factory=dict)
    total_hours: float
    hours_check: dict = Field(default_factory=dict)
    created_at: str = ""
    approved_at: Optional[str] = None

    def get_course(self, course_id: str) -> Optional[Course]:
        """Look up a course by its ID."""
        for course in self.courses:
            if course.course_id == course_id:
                return course
        return None
