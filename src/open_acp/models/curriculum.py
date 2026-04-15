"""Curriculum domain models: objectives, assessments, modules, and curriculum maps."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel


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


class Module(BaseModel):
    module_id: str
    title: str
    sequence: int
    objectives: list[LearningObjective]
    assessments: list[Assessment]
    estimated_hours: float
    prerequisite_modules: list[str]
    content_types: list[str] = []  # Which ContentTypes this module needs


class CurriculumMap(BaseModel):
    curriculum_id: str
    version: int
    program_name: str
    domain: str
    pedagogy_framework: str
    pedagogy_justification: str
    differentiation_strategy: dict
    modules: list[Module]
    total_hours: float
    created_at: str
    approved_at: Optional[str] = None

    def get_module(self, module_id: str) -> Optional[Module]:
        """Look up a module by its ID."""
        for module in self.modules:
            if module.module_id == module_id:
                return module
        return None
