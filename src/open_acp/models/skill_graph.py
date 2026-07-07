"""Skill graph models: nodes, edges, and the full skill graph."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class DurabilityRating(str, Enum):
    DURABLE = "durable"
    PERISHABLE = "perishable"
    UNKNOWN = "unknown"


class SkillNode(BaseModel):
    skill_id: str
    name: str
    domain: str
    demand_score: float = Field(ge=0.0, le=1.0)
    durability: DurabilityRating
    prerequisites: list[str]
    related_skills: list[str]
    confidence: float = Field(ge=0.0, le=1.0)
    last_updated: str


class SkillEdge(BaseModel):
    from_skill: str
    to_skill: str
    relationship: str  # "prerequisite" | "related" | "supersedes"
    weight: float


class SkillGraph(BaseModel):
    graph_id: str
    nodes: list[SkillNode]
    edges: list[SkillEdge]
    domain: str
    version: int
    updated_at: str
    stack_id: Optional[str] = None
    domain_ref: Optional[str] = None
