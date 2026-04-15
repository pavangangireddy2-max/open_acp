"""Stage artifact model with JSON-schema validation support."""

import json
from pathlib import Path

from pydantic import BaseModel

import jsonschema


class StageArtifact(BaseModel):
    artifact_id: str
    stage_id: str
    pipeline_id: str
    content_type: str
    data: dict
    schema_path: str
    created_at: str
    validated: bool = False
    attempts: int = 1
    validation_errors: list[str] = []
    review_decision: str = "not_run"
    review_summary: str = ""
    review_findings: list[dict] = []

    def validate_against_schema(self) -> None:
        """Load JSON schema from schemas/{schema_path}, validate self.data.

        Sets self.validated = True on success; raises jsonschema.ValidationError
        on failure.
        """
        schema_file = self._find_schemas_dir() / self.schema_path
        with open(schema_file) as f:
            schema = json.load(f)
        jsonschema.validate(instance=self.data, schema=schema)
        self.validated = True

    @staticmethod
    def _find_schemas_dir() -> Path:
        current = Path(__file__).resolve()
        for ancestor in current.parents:
            candidate = ancestor / "schemas"
            if candidate.is_dir():
                return candidate
        return Path("schemas")
