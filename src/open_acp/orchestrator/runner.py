"""PipelineRunner — manages cycle execution and high-level checkpointing."""
import json
from datetime import datetime, UTC
from pathlib import Path

from open_acp.orchestrator.master_graph import run_master
from open_acp.memory.episodic import JSONEpisodicStore


class PipelineRunner:
    """High-level runner that manages cycles and stores results."""

    def __init__(self):
        self.episodic = JSONEpisodicStore()

    def run_cycle(
        self,
        domain: str,
        content_type: str = "concept_explainer",
        module_title: str = "Introduction",
        module_id: str = "m1",
        estimated_hours: float = 1.0,
        auto_approve: bool = False,
        cycle_id: str = "cycle_1",
    ) -> dict:
        """Run a complete A→B→C→D cycle and store results."""
        start_time = datetime.now(UTC)

        result = run_master(
            domain=domain,
            content_type=content_type,
            module_title=module_title,
            module_id=module_id,
            estimated_hours=estimated_hours,
            auto_approve=auto_approve,
            cycle_id=cycle_id,
        )

        end_time = datetime.now(UTC)
        duration = (end_time - start_time).total_seconds()

        # Store run record
        run_record = {
            "run_id": result.get("run_id", "unknown"),
            "cycle_id": cycle_id,
            "domain": domain,
            "content_type": content_type,
            "started_at": start_time.isoformat(),
            "completed_at": end_time.isoformat(),
            "duration_seconds": duration,
            "loop_a_entries_created": len(result.get("loop_a_result", {}).get("wiki_entries_created", [])),
            "loop_b_modules": len(result.get("loop_b_result", {}).get("curriculum_map", {}).get("modules", [])),
            "loop_c_stages": result.get("loop_c_result", {}).get("stages_completed", 0),
            "loop_d_insights": result.get("loop_d_result", {}).get("health_report", {}).get("insights_count", 0),
        }
        self.episodic.store(f"run_{cycle_id}", run_record)

        return result
