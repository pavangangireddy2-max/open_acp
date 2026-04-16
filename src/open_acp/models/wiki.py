"""Wiki / knowledge-base entity models."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EntityType(str, Enum):
    SKILL = "skill"
    COMPETITOR = "competitor"
    AUDIENCE_SEGMENT = "audience_segment"
    CONCEPT = "concept"
    DOMAIN = "domain"
    PRODUCT = "product"


class WikiConfidence(BaseModel):
    score: float = Field(ge=0.0, le=1.0)
    sources_count: int
    last_verified: str
    durability: str  # "durable" | "perishable" | "unknown"


class WikiRelationship(BaseModel):
    from_entity: str
    to_entity: str
    rel_type: str  # "prerequisite" | "related" | "supersedes" | "competes_with" | "contains"
    confidence: float


class WikiEntity(BaseModel):
    entity_id: str
    entity_type: EntityType
    title: str
    content: str
    confidence: WikiConfidence
    sources: list[str]
    cross_references: list[str]
    supersedes: Optional[str] = None
    created_at: str
    updated_at: str


class StackProfileType(str, Enum):
    SKILL = "skill"


class StackSkillProfile(BaseModel):
    stack_id: str
    canonical_entity_id: str
    canonical_entity_type: StackProfileType = StackProfileType.SKILL
    title: str
    summary: str
    relevance_score: float = Field(ge=0.0, le=1.0)
    role_in_stack: str
    prerequisite_skills: list[str] = []
    downstream_skills: list[str] = []
    pedagogy_notes: list[str] = []
    assessment_implications: list[str] = []
    sources: list[str] = []
    created_at: str
    updated_at: str
