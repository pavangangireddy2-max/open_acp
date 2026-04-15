"""Feedback memory — stores signals, eval scores, and insights (JSON v1)."""
import json
from pathlib import Path
from typing import Optional
from open_acp.memory.base import MemoryStore


class JSONFeedbackStore(MemoryStore):
    """JSON file-based feedback memory (append-only)."""

    def __init__(self, storage_dir: Optional[str] = None):
        if storage_dir:
            self.storage_dir = Path(storage_dir)
        else:
            self.storage_dir = Path(__file__).parent.parent.parent.parent / "storage" / "feedback"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def store(self, key: str, data: dict) -> None:
        filepath = self.storage_dir / f"{key}.json"
        filepath.write_text(json.dumps(data, indent=2, default=str))

    def retrieve(self, key: str) -> Optional[dict]:
        filepath = self.storage_dir / f"{key}.json"
        if filepath.exists():
            return json.loads(filepath.read_text())
        return None

    def query(self, **filters) -> list[dict]:
        results = []
        collection = filters.pop("collection", None)
        if collection:
            filepath = self.storage_dir / f"{collection}.jsonl"
            if filepath.exists():
                for line in filepath.read_text().strip().split("\n"):
                    if line:
                        data = json.loads(line)
                        match = all(data.get(k) == v for k, v in filters.items())
                        if match:
                            results.append(data)
        return results

    def append(self, collection: str, data: dict) -> None:
        filepath = self.storage_dir / f"{collection}.jsonl"
        with open(filepath, "a") as f:
            f.write(json.dumps(data, default=str) + "\n")

    def store_eval_scores(self, report_id: str, scores: list[dict]) -> None:
        """Store evaluation scores for later analysis."""
        self.append("eval_scores", {"report_id": report_id, "scores": scores})

    def store_insight(self, insight: dict) -> None:
        """Store a classified insight."""
        self.append("insights", insight)
