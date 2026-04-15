"""Load and compose the three-tier guideline system.

Tier 1: pedagogy/principles.yaml — universal learning principles
Tier 2: formats/{format}.yaml — content-format-specific guidelines
Tier 3: brand.yaml (default.yaml) — visual/brand rules
Future: stacks/{stack}.yaml — domain-stack-specific guidelines
"""
from pathlib import Path
from typing import Optional

import yaml


class StyleLoader:
    """Loads and composes guidelines from the three-tier style system."""

    def __init__(self, styles_dir: Optional[str] = None):
        if styles_dir:
            self.base_dir = Path(styles_dir)
        else:
            self.base_dir = Path(__file__).parent

    # ── Single-file loaders ────────────────────────────────────────────

    def load(self, name: str = "default") -> dict:
        """Load a single YAML file by name (searches root, then subdirs)."""
        # Direct path
        path = self.base_dir / f"{name}.yaml"
        if path.exists():
            return self._load_yaml(path)
        # Search subdirectories
        for subdir in ["pedagogy", "formats", "stacks"]:
            path = self.base_dir / subdir / f"{name}.yaml"
            if path.exists():
                return self._load_yaml(path)
        raise FileNotFoundError(f"Style file not found: {name}")

    def load_as_text(self, name: str = "default") -> str:
        """Load a YAML file as raw text (for injecting into prompts)."""
        path = self.base_dir / f"{name}.yaml"
        if path.exists():
            return path.read_text(encoding="utf-8")
        for subdir in ["pedagogy", "formats", "stacks"]:
            path = self.base_dir / subdir / f"{name}.yaml"
            if path.exists():
                return path.read_text(encoding="utf-8")
        return ""

    # ── Composed loader (the key method) ───────────────────────────────

    def load_for_pipeline(self, content_type: str, stack: Optional[str] = None) -> dict:
        """Load and compose all applicable guidelines for a content type.

        Returns a merged dict with keys: pedagogy, format, brand, stack (if available).
        This is what gets injected into stage director skills as context.
        """
        result = {}

        # Tier 1: Universal pedagogy principles (always loaded)
        principles_path = self.base_dir / "pedagogy" / "principles.yaml"
        if principles_path.exists():
            result["pedagogy"] = self._load_yaml(principles_path)

        # Tier 2: Format-specific guidelines
        format_name = self._content_type_to_format(content_type)
        format_path = self.base_dir / "formats" / f"{format_name}.yaml"
        if format_path.exists():
            result["format"] = self._load_yaml(format_path)

        # Tier 3: Brand/visual guidelines
        brand_path = self.base_dir / "default.yaml"
        if brand_path.exists():
            result["brand"] = self._load_yaml(brand_path)

        # Optional Tier 4: Stack-specific guidelines
        if stack:
            stack_path = self.base_dir / "stacks" / f"{stack}.yaml"
            if stack_path.exists():
                result["stack"] = self._load_yaml(stack_path)

        return result

    def load_for_pipeline_as_text(self, content_type: str, stack: Optional[str] = None) -> str:
        """Load composed guidelines as a single text block for prompt injection."""
        composed = self.load_for_pipeline(content_type, stack)
        parts = []

        if "pedagogy" in composed:
            parts.append("## Pedagogy Principles\n")
            parts.append(yaml.dump(composed["pedagogy"], default_flow_style=False)[:3000])

        if "format" in composed:
            parts.append("\n## Format Guidelines\n")
            parts.append(yaml.dump(composed["format"], default_flow_style=False)[:2000])

        if "brand" in composed:
            parts.append("\n## Brand Guidelines\n")
            parts.append(yaml.dump(composed["brand"], default_flow_style=False)[:2000])

        if "stack" in composed:
            parts.append("\n## Stack-Specific Guidelines\n")
            parts.append(yaml.dump(composed["stack"], default_flow_style=False)[:1500])

        return "\n".join(parts)

    # ── Utility ────────────────────────────────────────────────────────

    def list_available(self) -> dict[str, list[str]]:
        """List all available style files organized by tier."""
        result = {
            "brand": [f.stem for f in self.base_dir.glob("*.yaml")],
            "pedagogy": [f.stem for f in (self.base_dir / "pedagogy").glob("*.yaml")] if (self.base_dir / "pedagogy").exists() else [],
            "formats": [f.stem for f in (self.base_dir / "formats").glob("*.yaml")] if (self.base_dir / "formats").exists() else [],
            "stacks": [f.stem for f in (self.base_dir / "stacks").glob("*.yaml")] if (self.base_dir / "stacks").exists() else [],
        }
        return result

    @staticmethod
    def _content_type_to_format(content_type: str) -> str:
        """Map a content type to its format guideline file name."""
        SESSION_TYPES = {"concept_explainer", "problem_solving", "project_building",
                         "learning_support", "platform_walkthrough", "induction"}
        if content_type in SESSION_TYPES:
            return "ppt_session"
        # Future: reading_material, mcq_quiz, coding_exercise, etc.
        return content_type

    @staticmethod
    def _load_yaml(path: Path) -> dict:
        with open(path) as f:
            return yaml.safe_load(f) or {}
