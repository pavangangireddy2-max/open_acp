"""Load and validate YAML pipeline definitions with inheritance resolution."""
import os
from pathlib import Path
from typing import Any, Optional

import yaml
from pydantic import BaseModel

from open_acp.models.content_types import normalize_content_type, pipeline_lookup_content_type


class StageDefinition(BaseModel):
    id: str
    skill: str                          # path relative to skills/pipelines/
    tools: list[str] = []               # tool names from registry
    artifact_schema: str = ""           # filename in schemas/
    model_tier: str = "strong"
    review_focus: list[str] = []
    success_criteria: list[str] = []
    checkpoint_required: bool = True
    human_approval_default: bool = False


class PipelineDefinition(BaseModel):
    pipeline_id: str
    content_type: str
    display_name: str
    description: str = ""
    version: str = "1.0"
    family: str = ""                    # session, written, practice, assessment
    inherits: Optional[str] = None

    stages: list[StageDefinition] = []

    # Defaults (inherited from _base.yaml)
    eval_threshold: float = 3.5
    max_iterations: int = 5
    model_tier: str = "strong"
    review_max_rounds: int = 2
    gate_type: str = "G3"
    gate_blocking: bool = True
    required_dimensions: list[str] = []
    style: str = "default"
    strict_execution: bool = False


def _resolve_path(filename: str, base_dir: Path) -> Path:
    """Resolve a pipeline YAML path relative to pipeline_defs/."""
    # Check direct path
    path = base_dir / filename
    if path.exists():
        return path
    # Check with .yaml extension
    path = base_dir / f"{filename}.yaml"
    if path.exists():
        return path
    raise FileNotFoundError(f"Pipeline definition not found: {filename} (searched in {base_dir})")


def _load_yaml(path: Path) -> dict:
    """Load a YAML file."""
    with open(path) as f:
        return yaml.safe_load(f) or {}


def _merge_dicts(base: dict, override: dict) -> dict:
    """Deep merge override into base. Override wins for scalar values."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


class PipelineLoader:
    """Loads pipeline definitions with inheritance resolution."""

    def __init__(self, pipeline_dir: Optional[str] = None):
        if pipeline_dir:
            self.base_dir = Path(pipeline_dir)
        else:
            self.base_dir = Path(__file__).parent

    def load(self, content_type: str) -> PipelineDefinition:
        """Load a pipeline definition by content type, resolving inheritance."""
        canonical_content_type = normalize_content_type(content_type)
        # Search for the YAML file across subdirectories
        yaml_path = self._find_pipeline_yaml(canonical_content_type)
        raw = _load_yaml(yaml_path)

        # Resolve inheritance chain
        resolved = self._resolve_inheritance(raw)

        # Build stages
        stages = []
        for stage_raw in resolved.get("stages", []):
            stages.append(StageDefinition(**stage_raw))

        # Extract defaults
        defaults = resolved.get("defaults", {})
        review = defaults.get("review", {})
        gate = defaults.get("gate", {})

        return PipelineDefinition(
            pipeline_id=normalize_content_type(resolved.get("pipeline_id", canonical_content_type)),
            content_type=normalize_content_type(resolved.get("content_type", canonical_content_type)),
            display_name=resolved.get("display_name", canonical_content_type.replace("_", " ").title()),
            description=resolved.get("description", ""),
            version=resolved.get("version", "1.0"),
            family=resolved.get("family", ""),
            stages=stages,
            eval_threshold=defaults.get("eval_threshold", 3.5),
            max_iterations=defaults.get("max_iterations", 5),
            model_tier=defaults.get("model_tier", "strong"),
            review_max_rounds=review.get("max_review_rounds", 2),
            gate_type=gate.get("type", "G3"),
            gate_blocking=gate.get("blocking", True),
            required_dimensions=resolved.get("required_dimensions", []),
            style=resolved.get("style", "default"),
            strict_execution=resolved.get("strict_execution", False),
        )

    def _find_pipeline_yaml(self, content_type: str) -> Path:
        """Search subdirectories for a pipeline YAML matching content_type."""
        lookup_key = pipeline_lookup_content_type(content_type)
        for subdir in ["academics", "practice", "assessments", ""]:
            candidate = self.base_dir / subdir / f"{lookup_key}.yaml"
            if candidate.exists():
                return candidate
        raise FileNotFoundError(
            f"No pipeline definition found for content_type={content_type} in {self.base_dir}"
        )

    def _resolve_inheritance(self, raw: dict) -> dict:
        """Resolve the 'inherits' chain, merging parent → child."""
        inherits = raw.get("inherits")
        if not inherits:
            # Still merge with _base.yaml if it exists
            base_path = self.base_dir / "_base.yaml"
            if base_path.exists():
                base = _load_yaml(base_path)
                return _merge_dicts(base, raw)
            return raw

        # Load parent
        parent_path = _resolve_path(inherits, self.base_dir)
        parent_raw = _load_yaml(parent_path)

        # Recursively resolve parent's inheritance
        parent_resolved = self._resolve_inheritance(parent_raw)

        # Merge parent into child (child wins)
        return _merge_dicts(parent_resolved, raw)

    def list_available(self) -> list[str]:
        """List all available pipeline content types."""
        types = []
        for yaml_file in self.base_dir.rglob("*.yaml"):
            if yaml_file.name.startswith("_"):
                continue
            types.append(normalize_content_type(yaml_file.stem))
        return sorted(set(types))
