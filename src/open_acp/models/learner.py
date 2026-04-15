"""Learner persona and model definitions."""

from pydantic import BaseModel


class KnowledgeGap(BaseModel):
    topic: str
    severity: str  # "minor" | "moderate" | "critical"
    evidence: str


class Misconception(BaseModel):
    concept: str
    description: str
    frequency: float


class LearnerPersona(BaseModel):
    persona_id: str
    name: str
    description: str
    prior_knowledge: list[str]
    knowledge_gaps: list[KnowledgeGap]
    misconceptions: list[Misconception]
    motivation_drivers: list[str]
    learning_preferences: list[str]


class LearnerModel(BaseModel):
    model_id: str
    domain: str
    personas: list[LearnerPersona]
    updated_at: str
