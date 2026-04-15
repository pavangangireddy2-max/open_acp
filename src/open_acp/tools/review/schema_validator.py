"""SchemaValidator tool — validates artifacts against JSON schemas."""
import json
import time
from pathlib import Path

import jsonschema

from open_acp.tools.base_tool import BaseTool, ToolResult, ToolStatus, ToolTier


def _find_schemas_dir() -> Path:
    """Walk up from this file to locate the project-level schemas/ directory."""
    current = Path(__file__).resolve()
    for ancestor in current.parents:
        candidate = ancestor / "schemas"
        if candidate.is_dir():
            return candidate
    # Fallback: assume standard project layout (src/open_acp/tools/review -> 4 levels up)
    return current.parents[4] / "schemas"


class SchemaValidator(BaseTool):
    """Validate stage artifacts against JSON schemas."""

    name = "schema_validator"
    capability = "review"
    provider = "local"
    tier = ToolTier.LOCAL
    cost_per_call = 0.0
    description = "Validate stage artifacts against JSON schemas"

    def execute(self, **kwargs) -> ToolResult:
        """Validate data against a JSON schema.

        Args:
            data: The artifact dict to validate.
            schema_path: Schema filename (e.g. "outline.schema.json").
        """
        data: dict = kwargs.get("data", {})
        schema_path: str = kwargs.get("schema_path", "")

        if not data:
            return ToolResult(success=False, error="data is required")
        if not schema_path:
            return ToolResult(success=False, error="schema_path is required")

        schemas_dir = _find_schemas_dir()
        full_path = schemas_dir / schema_path

        if not full_path.exists():
            return ToolResult(
                success=False,
                error=f"Schema file not found: {full_path}",
            )

        try:
            start = time.time()
            with open(full_path) as f:
                schema = json.load(f)

            jsonschema.validate(instance=data, schema=schema)
            duration = time.time() - start

            return ToolResult(
                success=True,
                data={"valid": True},
                duration_seconds=round(duration, 4),
            )
        except jsonschema.ValidationError as e:
            return ToolResult(
                success=False,
                data={"valid": False},
                error=f"Validation failed: {e.message} (path: {'.'.join(str(p) for p in e.absolute_path)})",
            )
        except json.JSONDecodeError as e:
            return ToolResult(
                success=False,
                error=f"Invalid JSON schema file: {e}",
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))

    def get_status(self) -> ToolStatus:
        """Available if the schemas directory exists."""
        schemas_dir = _find_schemas_dir()
        if schemas_dir.is_dir():
            return ToolStatus.AVAILABLE
        return ToolStatus.UNAVAILABLE
