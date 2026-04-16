"""Resolve pedagogy profiles from deterministic config."""
from pathlib import Path
from typing import Any, Optional

import yaml

from open_acp.config.curriculum_context import find_project_root


GLOBAL_DEFAULT_PROFILE = "concept_progression"
CONTENT_TYPE_FALLBACK_PROFILES: dict[str, str] = {
    "concept_explainer": "concept_progression",
    "problem_solving": "worked_example_scaffold",
    "project_building": "project_build_along",
    "platform_walkthrough": "guided_tool_walkthrough",
    "learning_support": "practice_with_feedback",
    "induction": "concept_progression",
    "reading_material": "concept_progression",
    "summary_cheatsheet": "concept_progression",
    "mcq_practice": "practice_with_feedback",
    "coding_practice": "worked_example_scaffold",
    "classroom_quiz": "assessment_evidence_check",
    "module_quiz": "assessment_evidence_check",
    "skill_assessment": "assessment_evidence_check",
    "final_course_quiz": "assessment_evidence_check",
    "final_course_project": "project_build_along",
    "graded_assessment": "assessment_evidence_check",
}


class PedagogyResolver:
    """Resolve the effective pedagogy profile for a domain/content_type pair."""

    def __init__(self, styles_dir: Optional[str] = None):
        if styles_dir:
            self.base_dir = Path(styles_dir)
        else:
            self.base_dir = find_project_root() / "knowledge" / "guidance"
        self.stack_manifest_dir = self._find_stack_manifest_dir()

    def resolve(self, content_type: str, domain: Optional[str] = None) -> str:
        """Return the resolved pedagogy profile ID."""
        return self.resolve_with_reason(content_type, domain)["profile"]

    def resolve_with_reason(self, content_type: str, domain: Optional[str] = None) -> dict[str, str]:
        """Return the resolved profile and the path used.

        Resolution order for non-product calls:
        1. stack manifest content-type override
        2. stack manifest default
        3. fallback content-type default
        4. global fallback default
        """
        normalized_domain = self._normalize(domain)
        normalized_type = self._normalize(content_type)

        stack_resolution = self._resolve_stack_profile(
            domain=normalized_domain,
            content_type=normalized_type,
        )
        if stack_resolution:
            return stack_resolution

        if normalized_type in CONTENT_TYPE_FALLBACK_PROFILES:
            profile = CONTENT_TYPE_FALLBACK_PROFILES[normalized_type]
            return {
                "profile": profile,
                "reason": f"content-type default: {normalized_type} -> {profile}",
            }

        profile = GLOBAL_DEFAULT_PROFILE
        return {
            "profile": profile,
            "reason": f"global default -> {profile}",
        }

    def resolve_domain_profile(
        self,
        domain: Optional[str],
        content_type: Optional[str] = None,
        product_context: Optional[dict[str, Any]] = None,
    ) -> dict[str, str]:
        """Resolve a domain-level pedagogy profile, preferring product-aware canonical overrides."""
        product_resolution = self._resolve_product_profile(
            product_context=product_context or {},
            domain=domain,
        )
        if product_resolution:
            if content_type:
                product_resolution.setdefault("content_type", self._normalize(content_type))
            return product_resolution

        resolution = self.resolve_with_reason(content_type=content_type or "", domain=domain)
        source = resolution["reason"].split(" -> ")[0]
        resolution["rationale"] = resolution.get("rationale") or resolution["reason"]
        resolution["source"] = source
        resolution["resolution_layers"] = [source]
        return resolution

    def resolve_program_profile(
        self,
        domain: Optional[str],
        content_type: Optional[str] = None,
    ) -> dict[str, str]:
        """Compatibility alias for older call sites."""
        return self.resolve_domain_profile(domain=domain, content_type=content_type)

    def list_profiles(self) -> list[str]:
        """List profile files available under guidance/pedagogy/profiles."""
        profiles_dir = self.base_dir / "pedagogy" / "profiles"
        if not profiles_dir.exists():
            return []
        return sorted(path.stem for path in profiles_dir.glob("*.yaml"))

    def _load_stack_manifest(self, domain: Optional[str]) -> dict:
        normalized_domain = self._normalize(domain)
        if not normalized_domain or not self.stack_manifest_dir.exists():
            return {}

        manifest_path = self.stack_manifest_dir / f"{normalized_domain}.yaml"
        if not manifest_path.exists():
            return {}

        with open(manifest_path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def _resolve_stack_profile(
        self,
        domain: str,
        content_type: str,
    ) -> dict[str, str]:
        manifest = self._load_stack_manifest(domain)
        if not manifest:
            return {}

        pedagogy = manifest.get("pedagogy") or {}
        type_layers = pedagogy.get("content_types") or {}
        if content_type and content_type in type_layers:
            type_layer = type_layers[content_type] or {}
            profile = type_layer.get("pedagogy_profile")
            rationale = type_layer.get("pedagogy_rationale") or f"stack content-type override for {domain}:{content_type}"
            if profile:
                return {
                    "profile": profile,
                    "reason": f"stack_content_type:{domain}:{content_type} -> {profile}",
                    "rationale": rationale,
                    "source": f"stack_content_type:{domain}:{content_type}",
                    "resolution_layers": [f"stack_content_type:{domain}:{content_type}"],
                }

        default_layer = pedagogy.get("default") or {}
        profile = default_layer.get("pedagogy_profile")
        rationale = default_layer.get("pedagogy_rationale") or f"stack default override for {domain}"
        if profile:
            return {
                "profile": profile,
                "reason": f"stack_default:{domain} -> {profile}",
                "rationale": rationale,
                "source": f"stack_default:{domain}",
                "resolution_layers": [f"stack_default:{domain}"],
            }

        return {}

    def _find_stack_manifest_dir(self) -> Path:
        for ancestor in [self.base_dir.resolve(), *self.base_dir.resolve().parents]:
            candidate = ancestor / "knowledge" / "manifests" / "stacks"
            if candidate.exists():
                return candidate
        return Path("knowledge/manifests/stacks")

    def _resolve_product_profile(
        self,
        product_context: dict[str, Any],
        domain: Optional[str],
    ) -> dict[str, str]:
        layers = product_context.get("pedagogy_layers", {}) or {}
        normalized_domain = self._normalize(domain)
        product_family = product_context.get("product_family") or "default"
        product_version = product_context.get("product_version") or "default_version"
        product_label = product_context.get("product_label", product_family)

        merged: dict[str, str] = {}
        field_sources: dict[str, str] = {}
        resolution_layers: list[str] = []

        ordered_layers = [
            ("product_default", layers.get("product_default") or {}, f"product_default:{product_family}"),
            ("product_domain", layers.get("product_domain") or {}, f"product_domain:{product_family}:{normalized_domain}"),
            ("product_version", layers.get("product_version") or {}, f"product_version:{product_family}:{product_version}"),
            (
                "product_version_domain",
                layers.get("product_version_domain") or {},
                f"product_version_domain:{product_family}:{product_version}:{normalized_domain}",
            ),
        ]

        for _, layer, source_label in ordered_layers:
            if not layer:
                continue
            resolution_layers.append(source_label)
            for key, value in layer.items():
                if value is None:
                    continue
                merged[key] = value
                field_sources[key] = source_label

        profile = merged.get("pedagogy_profile")
        if not profile:
            return {}

        rationale = merged.get("pedagogy_rationale") or f"product pedagogy override for {product_label}"
        source = field_sources.get("pedagogy_profile", "product_default")
        return {
            "profile": profile,
            "reason": f"{source} -> {profile}",
            "rationale": rationale,
            "source": source,
            "resolution_layers": resolution_layers or [source],
        }

    @staticmethod
    def _normalize(value: Optional[str]) -> str:
        return (value or "").strip().lower().replace(" ", "-")
