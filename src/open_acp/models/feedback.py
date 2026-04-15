"""Feedback loop models: insight classification and fix routing."""

from enum import Enum

from pydantic import BaseModel


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FixType(str, Enum):
    CONTENT_FIX = "content_fix"
    BRAND_FIX = "brand_fix"
    DESIGN_FIX = "design_fix"
    CURRICULUM_FIX = "curriculum_fix"
    PEDAGOGY_FIX = "pedagogy_fix"


class InsightClassification(BaseModel):
    insight_id: str
    fix_type: FixType
    severity: Severity
    description: str
    source_channels: list[str]
    evidence: str
    created_at: str


class FixRoute(BaseModel):
    route_id: str
    fix_type: FixType
    severity: Severity
    target_loop: str
    target_nodes: list[str]
    target_stages: list[str]
    requires_gate: bool
    gate_type: str
    auto_approved: bool
    insight: InsightClassification
    created_at: str
