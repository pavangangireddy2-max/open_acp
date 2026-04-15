"""Episodic memory — stores past runs, decisions, and fix history (JSON v1)."""
import json
from pathlib import Path
from typing import Optional
from open_acp.memory.base import MemoryStore


class JSONEpisodicStore(MemoryStore):
    """JSON file-based episodic memory."""

    def __init__(self, storage_dir: Optional[str] = None):
        if storage_dir:
            self.storage_dir = Path(storage_dir)
        else:
            self.storage_dir = Path(__file__).parent.parent.parent.parent / "storage" / "episodic"
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
        for filepath in self.storage_dir.glob("*.json"):
            data = json.loads(filepath.read_text())
            match = all(data.get(k) == v for k, v in filters.items())
            if match:
                results.append(data)
        return results

    def append(self, collection: str, data: dict) -> None:
        filepath = self.storage_dir / f"{collection}.jsonl"
        with open(filepath, "a") as f:
            f.write(json.dumps(data, default=str) + "\n")
