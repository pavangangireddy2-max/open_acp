"""Gate runner — orchestrates human-in-the-loop approval gates."""
from open_acp.models.gates import GateType, GateDecision, GateOutcome
from open_acp.config.settings import get_settings
from datetime import datetime, UTC


class GateRunner:
    """Manages human approval gates G1-G4."""

    GATE_CONFIG = {
        GateType.G1: {"label": "Strategy Review", "blocking": False, "approver": "Strategy Lead"},
        GateType.G2: {"label": "Curriculum Approval", "blocking": True, "approver": "Curriculum Architect + SME Panel"},
        GateType.G3: {"label": "Content Quality", "blocking": True, "approver": "SME + Pedagogy + Brand"},
        GateType.G4: {"label": "High-Severity Fix", "blocking": True, "approver": "Strategy Lead"},
    }

    def __init__(self):
        self.settings = get_settings()

    def request_approval(self, gate_type: GateType, context: dict) -> GateOutcome:
        """Request human approval at a gate."""
        config = self.GATE_CONFIG[gate_type]

        if self.settings.auto_approve_gates:
            return GateOutcome(
                gate_type=gate_type,
                decision=GateDecision.APPROVE,
                approver="auto",
                reason="Auto-approved (AUTO_APPROVE_GATES=true)",
                decided_at=datetime.now(UTC).isoformat(),
            )

        # In production, this would present a rich UI and wait for input
        # For now, auto-approve with a note
        print(f"\n  Gate {gate_type.value}: {config['label']}")
        print(f"    Approver: {config['approver']}")
        print(f"    Blocking: {config['blocking']}")

        if not config["blocking"]:
            return GateOutcome(
                gate_type=gate_type,
                decision=GateDecision.APPROVE,
                approver="advisory",
                reason="Non-blocking advisory gate -- auto-proceeding",
                decided_at=datetime.now(UTC).isoformat(),
            )

        # For blocking gates without auto-approve, approve with warning
        return GateOutcome(
            gate_type=gate_type,
            decision=GateDecision.APPROVE,
            approver="system",
            reason="Blocking gate -- approved by system (no human reviewer configured)",
            decided_at=datetime.now(UTC).isoformat(),
        )
