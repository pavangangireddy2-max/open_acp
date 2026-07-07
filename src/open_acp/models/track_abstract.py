"""Track abstract models — product-agnostic catalog combining stacks for a career outcome."""

from typing import Optional

from pydantic import BaseModel, Field


class StackCoverageScope(BaseModel):
    """Which C x L cells to include from a contributing stack."""
    stack_id: str
    role: str = "core"  # "core" | "supplementary" | "elective"
    include_tags: list[str] = Field(default_factory=list)  # e.g. ["C1", "C2"]
    include_levels: list[str] = Field(default_factory=list)  # e.g. ["L1", "L2"]

    @property
    def selected_cells(self) -> list[str]:
        """Compute which C x L cells this scope selects."""
        return [f"{c}_{l}" for c in self.include_tags for l in self.include_levels]


class TrackAbstract(BaseModel):
    track_id: str
    display_name: str
    career_outcome: Optional[str] = None
    contributing_stacks: list[StackCoverageScope] = Field(default_factory=list)
    version: int = 1
    updated_at: str = ""
