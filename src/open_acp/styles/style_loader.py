"""Load and compose runtime guidance for Loop B and Loop C."""
from pathlib import Path
from typing import Optional

import yaml

from open_acp.models.content_types import normalize_content_type
from open_acp.styles.pedagogy_resolver import PedagogyResolver
from open_acp.config.curriculum_context import find_project_root


class StyleLoader:
    """Load and compose pedagogy, delivery, stack, and brand guidance."""

    def __init__(self, styles_dir: Optional[str] = None):
        if styles_dir:
            self.base_dir = Path(styles_dir)
        else:
            self.base_dir = find_project_root() / "knowledge" / "guidance"
        self.pedagogy_resolver = PedagogyResolver(str(self.base_dir))

    # ── Single-file loaders ────────────────────────────────────────────

    def load(self, name: str = "default") -> dict:
        """Load a single YAML file by name (searches guidance subdirs)."""
        # Direct path
        path = self.base_dir / f"{name}.yaml"
        if path.exists():
            return self._load_yaml(path)
        # Search subdirectories
        for subdir in self._guidance_subdirs():
            path = self.base_dir / subdir / f"{name}.yaml"
            if path.exists():
                return self._load_yaml(path)
        raise FileNotFoundError(f"Style file not found: {name}")

    def load_as_text(self, name: str = "default") -> str:
        """Load a YAML file as raw text (for injecting into prompts)."""
        path = self.base_dir / f"{name}.yaml"
        if path.exists():
            return path.read_text(encoding="utf-8")
        for subdir in self._guidance_subdirs():
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
        learning_unit_type: Optional[str] = None,
        presentation_surface: Optional[str] = None,
        instructional_pattern: Optional[str] = None,
    ) -> dict:
        """Load and compose all applicable guidance for a pipeline content type.

        Returns layered guidance with keys such as pedagogy_core, pedagogy_profile,
        learning_unit_type, presentation_surface, instructional_pattern, teaching_mode_contract,
        stack, and brand when available.
        """
        content_type = normalize_content_type(content_type)
        result = {}
        stack_key = stack or domain
        resolved_profile = pedagogy_profile or self.pedagogy_resolver.resolve(content_type, domain=stack_key)
        contract = self.resolve_guidance_contract(
            content_type=content_type,
            learning_unit_type=learning_unit_type,
            presentation_surface=presentation_surface,
            instructional_pattern=instructional_pattern,
        )
        result["guidance_contract"] = contract

        # Tier 1: Pedagogy core
        core_path = self.base_dir / "pedagogy" / "core.yaml"
        if core_path.exists():
            result["pedagogy_core"] = self._load_yaml(core_path)

        # Tier 2: Resolved pedagogy profile
        profile_path = self.base_dir / "pedagogy" / "profiles" / f"{resolved_profile}.yaml"
        if profile_path.exists():
            result["pedagogy_profile"] = self._load_yaml(profile_path)

        # Tier 3: Learning-unit guidance
        unit_type_id = contract.get("learning_unit_type")
        if unit_type_id:
            unit_type_path = self.base_dir / "learning_unit_types" / f"{unit_type_id}.yaml"
        else:
            unit_type_path = None
        if unit_type_path and unit_type_path.exists():
            result["learning_unit_type"] = self._load_yaml(unit_type_path)

        # Tier 4: Presentation-surface guidance
        surface_id = contract.get("presentation_surface")
        if surface_id:
            surface_path = self.base_dir / "presentation_surfaces" / f"{surface_id}.yaml"
        else:
            surface_path = None
        if surface_path and surface_path.exists():
            result["presentation_surface"] = self._load_yaml(surface_path)

        # Tier 5: Instructional-pattern guidance
        pattern_id = contract.get("instructional_pattern")
        if pattern_id:
            pattern_path = self.base_dir / "instructional_patterns" / f"{pattern_id}.yaml"
        else:
            pattern_path = None
        if pattern_path and pattern_path.exists():
            result["instructional_pattern"] = self._load_yaml(pattern_path)

        profile_guidance = result.get("pedagogy_profile", {})
        pattern_guidance = result.get("instructional_pattern", {})
        teaching_mode_contract = self._build_teaching_mode_contract(profile_guidance, pattern_guidance)
        if teaching_mode_contract:
            result["teaching_mode_contract"] = teaching_mode_contract

        # Tier 6: Stack-specific guidance
        if stack_key:
            stack_path = self.base_dir / "stacks" / f"{stack_key}.yaml"
            if stack_path.exists():
                result["stack"] = self._load_yaml(stack_path)

        # Tier 7: Brand/visual guidelines
        brand_path = self.base_dir / "brand" / "default.yaml"
        if brand_path.exists():
            result["brand"] = self._load_yaml(brand_path)

        return result

    def load_for_pipeline_as_text(
        self,
        content_type: str,
        domain: Optional[str] = None,
        stack: Optional[str] = None,
        pedagogy_profile: Optional[str] = None,
        learning_unit_type: Optional[str] = None,
        presentation_surface: Optional[str] = None,
        instructional_pattern: Optional[str] = None,
    ) -> str:
        """Load composed guidelines as a single text block for prompt injection."""
        content_type = normalize_content_type(content_type)
        stack_key = stack or domain
        resolved_profile = pedagogy_profile or self.pedagogy_resolver.resolve(content_type, domain=stack_key)
        composed = self.load_for_pipeline(
            content_type=content_type,
            domain=domain,
            stack=stack,
            pedagogy_profile=resolved_profile,
            learning_unit_type=learning_unit_type,
            presentation_surface=presentation_surface,
            instructional_pattern=instructional_pattern,
        )
        parts = []

        if "guidance_contract" in composed:
            contract = composed["guidance_contract"]
            parts.append("## Guidance Contract")
            parts.append(f"- pipeline_content_type: {contract.get('pipeline_content_type')}")
            if contract.get("learning_unit_type"):
                parts.append(f"- learning_unit_type: {contract['learning_unit_type']}")
            if contract.get("presentation_surface"):
                parts.append(f"- presentation_surface: {contract['presentation_surface']}")
            if contract.get("instructional_pattern"):
                parts.append(f"- instructional_pattern: {contract['instructional_pattern']}")

        parts.append("## Resolved Pedagogy Profile")
        parts.append(f"- profile_id: {resolved_profile}")

        if "pedagogy_core" in composed:
            parts.append("\n## Pedagogy Core\n")
            parts.append(yaml.dump(composed["pedagogy_core"], default_flow_style=False)[:2500])

        if "pedagogy_profile" in composed:
            parts.append("\n## Pedagogy Profile\n")
            parts.append(yaml.dump(composed["pedagogy_profile"], default_flow_style=False)[:2500])

        if "teaching_mode_contract" in composed:
            parts.append("\n## Teaching Mode Contract\n")
            parts.append(yaml.dump(composed["teaching_mode_contract"], default_flow_style=False)[:1600])

        if "learning_unit_type" in composed:
            parts.append("\n## Learning Unit Type Guidance\n")
            parts.append(yaml.dump(composed["learning_unit_type"], default_flow_style=False)[:1800])

        if "presentation_surface" in composed:
            parts.append("\n## Presentation Surface Guidance\n")
            parts.append(yaml.dump(composed["presentation_surface"], default_flow_style=False)[:2400])

        if "instructional_pattern" in composed:
            parts.append("\n## Instructional Pattern Guidance\n")
            parts.append(yaml.dump(composed["instructional_pattern"], default_flow_style=False)[:1800])

        if "stack" in composed:
            parts.append("\n## Stack Guidance\n")
            parts.append(yaml.dump(composed["stack"], default_flow_style=False)[:1800])

        if "brand" in composed:
            parts.append("\n## Brand Guidelines\n")
            parts.append(yaml.dump(composed["brand"], default_flow_style=False)[:2000])

        return "\n".join(parts)

    # ── Utility ────────────────────────────────────────────────────────

    def list_available(self) -> dict[str, list[str]]:
        """List all available style files organized by tier."""
        result = {
            "brand_playbooks": [f.stem for f in (self.base_dir / "brand").glob("*.yaml")] if (self.base_dir / "brand").exists() else [],
            "pedagogy": [f.stem for f in (self.base_dir / "pedagogy").glob("*.yaml")] if (self.base_dir / "pedagogy").exists() else [],
            "pedagogy_profiles": [f.stem for f in (self.base_dir / "pedagogy" / "profiles").glob("*.yaml")] if (self.base_dir / "pedagogy" / "profiles").exists() else [],
            "learning_unit_types": [f.stem for f in (self.base_dir / "learning_unit_types").glob("*.yaml")] if (self.base_dir / "learning_unit_types").exists() else [],
            "presentation_surfaces": [f.stem for f in (self.base_dir / "presentation_surfaces").glob("*.yaml")] if (self.base_dir / "presentation_surfaces").exists() else [],
            "instructional_patterns": [f.stem for f in (self.base_dir / "instructional_patterns").glob("*.yaml")] if (self.base_dir / "instructional_patterns").exists() else [],
            "stacks": [f.stem for f in (self.base_dir / "stacks").glob("*.yaml")] if (self.base_dir / "stacks").exists() else [],
        }
        return result

    def resolve_guidance_contract(
        self,
        content_type: str,
        learning_unit_type: Optional[str] = None,
        presentation_surface: Optional[str] = None,
        instructional_pattern: Optional[str] = None,
    ) -> dict:
        """Resolve the non-pedagogy guidance contract for a pipeline content type."""
        content_type = normalize_content_type(content_type)
        resolved_unit_type = learning_unit_type or self._content_type_to_learning_unit_type(content_type)
        resolved_pattern = instructional_pattern or self._content_type_to_instructional_pattern(content_type)
        resolved_surface = presentation_surface or self._resolve_presentation_surface(
            content_type=content_type,
            learning_unit_type=resolved_unit_type,
            instructional_pattern=resolved_pattern,
        )
        return {
            "pipeline_content_type": content_type,
            "learning_unit_type": resolved_unit_type,
            "presentation_surface": resolved_surface,
            "instructional_pattern": resolved_pattern,
        }

    @staticmethod
    def _guidance_subdirs() -> list[str]:
        return [
            "brand",
            "pedagogy",
            "pedagogy/profiles",
            "learning_unit_types",
            "presentation_surfaces",
            "instructional_patterns",
            "stacks",
        ]

    @staticmethod
    def _content_type_to_learning_unit_type(content_type: str) -> Optional[str]:
        session_types = {
            "concept_explainer",
            "problem_solving",
            "project_building",
            "learning_support",
            "platform_walkthrough",
            "induction",
        }
        if content_type in session_types:
            return "video_session_unit"
        if content_type in {"reading_material", "summary_cheatsheet"}:
            return "reading_material_unit"
        if content_type == "mcq_practice":
            return "mcq_practice_unit"
        if content_type == "coding_practice":
            return "coding_practice_unit"
        if content_type == "classroom_quiz":
            return "classroom_quiz_unit"
        if content_type == "module_quiz":
            return "module_quiz_unit"
        if content_type == "final_course_quiz":
            return "final_course_quiz_unit"
        if content_type == "skill_assessment":
            return "skill_assessment_unit"
        if content_type == "graded_assessment":
            return "graded_assessment_unit"
        return None

    @staticmethod
    def _content_type_to_instructional_pattern(content_type: str) -> Optional[str]:
        pattern_types = {
            "concept_explainer",
            "problem_solving",
            "project_building",
            "learning_support",
            "platform_walkthrough",
            "induction",
        }
        if content_type in pattern_types:
            return content_type
        return None

    @staticmethod
    def _resolve_presentation_surface(
        content_type: str,
        learning_unit_type: Optional[str],
        instructional_pattern: Optional[str],
    ) -> Optional[str]:
        if instructional_pattern == "platform_walkthrough":
            return "screen_demo_session"
        if learning_unit_type == "video_session_unit":
            return "slide_backed_session"
        if learning_unit_type == "reading_material_unit":
            return "portal_reading_surface"
        if learning_unit_type in {
            "mcq_practice_unit",
            "classroom_quiz_unit",
            "module_quiz_unit",
            "final_course_quiz_unit",
            "skill_assessment_unit",
            "graded_assessment_unit",
        }:
            return "assessment_portal_surface"
        if learning_unit_type == "coding_practice_unit":
            return "coding_workspace_surface"
        return None

    @staticmethod
    def _build_teaching_mode_contract(profile_guidance: dict, pattern_guidance: dict) -> dict:
        allowed_modes = list(profile_guidance.get("allowed_teaching_modes", []) or [])
        preferred_sequence = list(pattern_guidance.get("common_teaching_mode_sequence", []) or [])
        resolved_sequence = [mode for mode in preferred_sequence if mode in allowed_modes]
        if not resolved_sequence:
            resolved_sequence = allowed_modes or preferred_sequence
        dropped_modes = [mode for mode in preferred_sequence if mode not in resolved_sequence]
        if not (allowed_modes or preferred_sequence or resolved_sequence):
            return {}
        return {
            "allowed_modes": allowed_modes,
            "preferred_sequence": preferred_sequence,
            "resolved_sequence": resolved_sequence,
            "dropped_pattern_modes": dropped_modes,
        }

    @staticmethod
    def _load_yaml(path: Path) -> dict:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
