"""Stack curriculum abstract models — module catalogs with C/L tagging.

C-tags (concept coverage tier):
  C1: 80% interview-frequent; must-cover
  C2: 20% interview-relevant; should-cover
  C3: Extensions beyond interview; nice-to-cover

L-tags (difficulty level):
  L1: Entry
  L2: Intermediate
  L3: Advanced

The C x L matrix is intentionally sparse — not every cell is populated.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class CTag(str, Enum):
    C1 = "C1"
    C2 = "C2"
    C3 = "C3"


class LTag(str, Enum):
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"


class HoursRange(BaseModel):
    min: float
    max: float


class ExternalPrerequisite(BaseModel):
    from_stack: str
    required_skill_ids: list[str] = Field(default_factory=list)
    kind: str = "hard_prereq"  # "hard_prereq" | "soft_prereq"


class AbstractModule(BaseModel):
    module_id: str
    title: str
    tags: list[str] = Field(default_factory=list)  # e.g. ["C1", "L1"]
    estimated_hours_range: HoursRange = Field(default_factory=lambda: HoursRange(min=4, max=6))
    default_pedagogy_profile: Optional[str] = None
    skill_ids: list[str] = Field(default_factory=list)
    prerequisite_modules: list[str] = Field(default_factory=list)
    prerequisite_external_skills: list[str] = Field(default_factory=list)
    concepts: list[str] = Field(default_factory=list)
    interview_frequency: Optional[str] = None  # "high" | "medium" | "low"

    @property
    def c_tag(self) -> Optional[str]:
        """Extract the C-tag from tags list."""
        for tag in self.tags:
            if tag in (CTag.C1, CTag.C2, CTag.C3):
                return tag
        return None

    @property
    def l_tag(self) -> Optional[str]:
        """Extract the L-tag from tags list."""
        for tag in self.tags:
            if tag in (LTag.L1, LTag.L2, LTag.L3):
                return tag
        return None

    @property
    def cl_cell(self) -> Optional[str]:
        """Return the C x L cell key, e.g. 'C1_L1'."""
        c, l = self.c_tag, self.l_tag
        if c and l:
            return f"{c}_{l}"
        return None


class StackCurriculumAbstract(BaseModel):
    stack_id: str
    domain_ref: str
    version: int = 1
    interview_intelligence_ref: Optional[str] = None
    modules: list[AbstractModule] = Field(default_factory=list)
    external_prerequisites: list[ExternalPrerequisite] = Field(default_factory=list)
    updated_at: str = ""

    @property
    def coverage_matrix_view(self) -> dict[str, list[str]]:
        """Compute module counts per C x L cell. Derived, not authored."""
        matrix: dict[str, list[str]] = {}
        for mod in self.modules:
            cell = mod.cl_cell
            if cell:
                matrix.setdefault(cell, []).append(mod.module_id)
        return matrix
