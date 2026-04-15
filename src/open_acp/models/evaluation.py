"""Evaluation models: dimensions, scores, and reports."""

from enum import Enum

from pydantic import BaseModel, Field


class EvalDimension(str, Enum):
    ACCURACY = "accuracy"
    PEDAGOGY = "pedagogy"
    ENGAGEMENT = "engagement"
    BRAND = "brand"
    CITATION_PROVENANCE = "citation_provenance"


class EvalScore(BaseModel):
    dimension: EvalDimension
    score: float = Field(ge=1.0, le=5.0)
    evidence: str
    failing_elements: list[str]


class EvalReport(BaseModel):
    report_id: str
    content_type: str
    module_id: str
    scores: list[EvalScore]
    final_score: float  # min of all dimension scores
    passed: bool
    iteration: int
    evaluated_at: str
