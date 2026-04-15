"""Competitor intelligence models."""

from pydantic import BaseModel


class CompetitorSnapshot(BaseModel):
    competitor_id: str
    name: str
    domain: str
    coverage: dict  # skill_id -> coverage_level
    positioning: str
    strengths: list[str]
    weaknesses: list[str]
    last_analyzed: str


class CompetitorMap(BaseModel):
    map_id: str
    domain: str
    competitors: list[CompetitorSnapshot]
    our_positioning: str
    gaps: list[str]
    updated_at: str
