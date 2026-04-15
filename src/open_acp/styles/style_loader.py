"""Load and compose the V1 layered style system."""
from pathlib import Path
from typing import Optional

import yaml

from open_acp.styles.pedagogy_resolver import PedagogyResolver


class StyleLoader:
    """Load and compose pedagogy, format, stack/domain, and brand guidance."""

    def __init__(self, styles_dir: Optional[str] = None):
        if styles_dir:
            self.base_dir = Path(styles_dir)
        else:
            self.base_dir = Path(__file__).parent
        self.pedagogy_resolver = PedagogyResolver(str(self.base_dir))

    # ── Single-file loaders ────────────────────────────────────────────

    def load(self, name: str = "default") -> dict:
        """Load a single YAML file by name (searches root, then subdirs)."""
        # Direct path
        path = self.base_dir / f"{name}.yaml"
        if path.exists():
            return self._load_yaml(path)
        # Search subdirectories
        for subdir in ["pedagogy", "pedagogy/profiles", "formats", "stacks"]:
            path = self.base_dir / subdir / f"{name}.yaml"
            if path.exists():
                return self._load_yaml(path)
        raise FileNotFoundError(f"Style file not found: {name}")

    def load_as_text(self, name: str = "default") -> str:
        """Load a YAML file as raw text (for injecting into prompts)."""
        path = self.base_dir / f"{name}.yaml"
        if path.exists():
            return path.read_text(encoding="utf-8")
        for subdir in ["pedagogy", "pedagogy/profiles", "formats", "stacks"]:
            path = self.base_dir / subdir / f"{name}.yaml"
            if path.exists():
                return path.read_text(encoding="utf-8")
        return ""

    # ── Composed loader (the key method) ───────────────────────────────

    def load_for_pipeline(
        self,
        content_type: str,
        domain: Optional[str] = None,
        stack: Optional[str] = None,
        pedagogy_profile: Optional[str] = None,
    ) -> dict:
        """Load and compose all applicable guidelines for a content type.

        Returns layered guidance with keys: pedagogy_core, pedagogy_profile, format,
        brand, and domain when available.
        """
        result = {}
        stack_key = stack or domain
        resolved_profile = pedagogy_profile or self.pedagogy_resolver.resolve(content_type, domain=stack_key)

        # Tier 1: Pedagogy core
        core_path = self.base_dir / "pedagogy" / "core.yaml"
        if core_path.exists():
            result["pedagogy_core"] = self._load_yaml(core_path)

        # Tier 2: Resolved pedagogy profile
        profile_path = self.base_dir / "pedagogy" / "profiles" / f"{resolved_profile}.yaml"
        if profile_path.exists():
            result["pedagogy_profile"] = self._load_yaml(profile_path)

        # Tier 3: Format-specific guidelines
        format_name = self._content_type_to_format(content_type)
        format_path = self.base_dir / "formats" / f"{format_name}.yaml"
        if format_path.exists():
            result["format"] = self._load_yaml(format_path)

        # Tier 4: Stack/domain-specific guidance
        if stack_key:
            stack_path = self.base_dir / "stacks" / f"{stack_key}.yaml"
            if stack_path.exists():
                result["domain"] = self._load_yaml(stack_path)

        # Tier 5: Brand/visual guidelines
        brand_path = self.base_dir / "default.yaml"
        if brand_path.exists():
            result["brand"] = self._load_yaml(brand_path)

        return result

    def load_for_pipeline_as_text(
        self,
        content_type: str,
        domain: Optional[str] = None,
        stack: Optional[str] = None,
        pedagogy_profile: Optional[str] = None,
    ) -> str:
        """Load composed guidelines as a single text block for prompt injection."""
        stack_key = stack or domain
        resolved_profile = pedagogy_profile or self.pedagogy_resolver.resolve(content_type, domain=stack_key)
        composed = self.load_for_pipeline(
            content_type=content_type,
            domain=domain,
            stack=stack,
            pedagogy_profile=resolved_profile,
        )
        parts = []

        parts.append("## Resolved Pedagogy Profile")
        parts.append(f"- profile_id: {resolved_profile}")

        if "pedagogy_core" in composed:
            parts.append("\n## Pedagogy Core\n")
            parts.append(yaml.dump(composed["pedagogy_core"], default_flow_style=False)[:2500])

        if "pedagogy_profile" in composed:
            parts.append("\n## Pedagogy Profile\n")
            parts.append(yaml.dump(composed["pedagogy_profile"], default_flow_style=False)[:2500])

        if "format" in composed:
            parts.append("\n## Format Guidelines\n")
            parts.append(yaml.dump(composed["format"], default_flow_style=False)[:2000])

        if "domain" in composed:
            parts.append("\n## Domain Guidelines\n")
            parts.append(yaml.dump(composed["domain"], default_flow_style=False)[:1800])

        if "brand" in composed:
            parts.append("\n## Brand Guidelines\n")
            parts.append(yaml.dump(composed["brand"], default_flow_style=False)[:2000])

        return "\n".join(parts)

    # ── Utility ────────────────────────────────────────────────────────

    def list_available(self) -> dict[str, list[str]]:
        """List all available style files organized by tier."""
        result = {
            "brand": [f.stem for f in self.base_dir.glob("*.yaml")],
            "pedagogy": [f.stem for f in (self.base_dir / "pedagogy").glob("*.yaml")] if (self.base_dir / "pedagogy").exists() else [],
            "pedagogy_profiles": [f.stem for f in (self.base_dir / "pedagogy" / "profiles").glob("*.yaml")] if (self.base_dir / "pedagogy" / "profiles").exists() else [],
            "formats": [f.stem for f in (self.base_dir / "formats").glob("*.yaml")] if (self.base_dir / "formats").exists() else [],
            "stacks": [f.stem for f in (self.base_dir / "stacks").glob("*.yaml")] if (self.base_dir / "stacks").exists() else [],
        }
        return result

    @staticmethod
    def _content_type_to_format(content_type: str) -> str:
        """Map a content type to its format guideline file name."""
        SESSION_TYPES = {"concept_explainer", "problem_solving",
                         "learning_support", "platform_walkthrough", "induction"}
        if content_type == "project_building":
            return "project_session"
        if content_type in SESSION_TYPES:
            return "ppt_session"
        # Future: reading_material, mcq_quiz, coding_exercise, etc.
        return content_type

    @staticmethod
    def _load_yaml(path: Path) -> dict:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
