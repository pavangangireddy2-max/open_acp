"""Domain definition models for the three-tier conceptual model (Domain > Stack > Track)."""

from typing import Optional

from pydantic import BaseModel, Field


class ReviewOwnership(BaseModel):
    content_review_queue: Optional[str] = None
    domain_lead: Optional[str] = None


class DomainDefinition(BaseModel):
    domain_id: str
    version: int = 1
    display_name: str
    poc: Optional[str] = None
    stacks: list[str] = Field(default_factory=list)
    review_ownership: ReviewOwnership = Field(default_factory=ReviewOwnership)
    related_domains: list[str] = Field(default_factory=list)
    updated_at: str = ""
