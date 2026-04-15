"""Gate models: quality gates G1-G4 for the 4-loop pipeline."""

from enum import Enum

from pydantic import BaseModel


class GateType(str, Enum):
    G1 = "G1"
    G2 = "G2"
    G3 = "G3"
    G4 = "G4"


class GateDecision(str, Enum):
    APPROVE = "approve"
    REVISE = "revise"
    ABORT = "abort"


class GateOutcome(BaseModel):
    gate_type: GateType
    decision: GateDecision
    approver: str
    reason: str
    revision_notes: str = ""
    decided_at: str
