"""Evaluator registry — tracks evaluator versions and weights."""
import json
from pathlib import Path
from typing import Optional


class EvaluatorRegistry:
    """Tracks evaluator versions, weights, and calibration data."""

    def __init__(self, storage_dir: Optional[str] = None):
        if storage_dir:
            self.storage_dir = Path(storage_dir)
        else:
            self.storage_dir = Path(__file__).parent.parent.parent.parent / "storage" / "evaluator_weights"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def get_weights(self) -> dict[str, float]:
        """Get current dimension weights (default: equal)."""
        weights_path = self.storage_dir / "weights.json"
        if weights_path.exists():
            return json.loads(weights_path.read_text())
        return {
            "accuracy": 1.0,
            "pedagogy": 1.0,
            "engagement": 1.0,
            "brand": 1.0,
            "citation_provenance": 1.0,
        }

    def save_weights(self, weights: dict[str, float]) -> None:
        """Save dimension weights."""
        weights_path = self.storage_dir / "weights.json"
        weights_path.write_text(json.dumps(weights, indent=2))

    def log_calibration(self, report: dict) -> None:
        """Log a calibration event."""
        log_path = self.storage_dir / "calibration_log.jsonl"
        with open(log_path, "a") as f:
            f.write(json.dumps(report) + "\n")
