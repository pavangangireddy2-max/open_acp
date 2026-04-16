"""Resolve pedagogy profiles from deterministic config."""
from pathlib import Path
from typing import Optional

import yaml

from open_acp.config.curriculum_context import find_project_root


class PedagogyResolver:
    """Resolve the effective pedagogy profile for a domain/content_type pair."""

    def __init__(self, styles_dir: Optional[str] = None):
        if styles_dir:
            self.base_dir = Path(styles_dir)
        else:
            self.base_dir = find_project_root() / "knowledge" / "guidance"
        self.matrix_path = self.base_dir / "pedagogy" / "profile_matrix.yaml"
        self.stack_manifest_dir = self._find_stack_manifest_dir()

    def resolve(self, content_type: str, domain: Optional[str] = None) -> str:
        """Return the resolved pedagogy profile ID."""
        return self.resolve_with_reason(content_type, domain)["profile"]

    def resolve_with_reason(self, content_type: str, domain: Optional[str] = None) -> dict[str, str]:
        """Return the resolved profile and the fallback path used."""
        matrix = self._load_matrix()
        normalized_domain = self._normalize(domain)
        normalized_type = self._normalize(content_type)

        domain_overrides = matrix.get("domain_overrides", {})
        if normalized_domain in domain_overrides:
            domain_map = domain_overrides[normalized_domain] or {}
            if normalized_type in domain_map:
                profile = domain_map[normalized_type]
                return {
                    "profile": profile,
                    "reason": f"exact match: ({normalized_domain}, {normalized_type}) -> {profile}",
                }

        type_defaults = matrix.get("content_type_defaults", {})
        if normalized_type in type_defaults:
            profile = type_defaults[normalized_type]
            return {
                "profile": profile,
                "reason": f"content-type default: {normalized_type} -> {profile}",
            }

        profile = matrix.get("global_default", "concept_progression")
        return {
            "profile": profile,
            "reason": f"global default -> {profile}",
        }

    def resolve_domain_profile(
        self,
        domain: Optional[str],
        content_type: Optional[str] = None,
    ) -> dict[str, str]:
        """Resolve a domain-level pedagogy profile, preferring stack manifest overrides."""
        manifest = self._load_stack_manifest(domain)
        if manifest:
            profile = manifest.get("domain_pedagogy_profile") or manifest.get("program_pedagogy_profile")
            rationale = manifest.get("domain_pedagogy_rationale") or manifest.get("program_pedagogy_rationale", "")
            if profile:
                normalized_domain = self._normalize(domain)
                return {
                    "profile": profile,
                    "reason": f"stack manifest override: {normalized_domain} -> {profile}",
                    "rationale": rationale or f"stack manifest override for {normalized_domain}",
                }

        if content_type:
            resolution = self.resolve_with_reason(content_type=content_type, domain=domain)
            resolution["rationale"] = resolution["reason"]
            return resolution

        profile = self._load_matrix().get("global_default", "concept_progression")
        return {
            "profile": profile,
            "reason": f"global default -> {profile}",
            "rationale": f"global default -> {profile}",
        }

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

    def _load_matrix(self) -> dict:
        if not self.matrix_path.exists():
            return {"global_default": "concept_progression"}
        with open(self.matrix_path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def _load_stack_manifest(self, domain: Optional[str]) -> dict:
        normalized_domain = self._normalize(domain)
        if not normalized_domain or not self.stack_manifest_dir.exists():
            return {}

        manifest_path = self.stack_manifest_dir / f"{normalized_domain}.yaml"
        if not manifest_path.exists():
            return {}

        with open(manifest_path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def _find_stack_manifest_dir(self) -> Path:
        for ancestor in [self.base_dir.resolve(), *self.base_dir.resolve().parents]:
            candidate = ancestor / "knowledge" / "manifests" / "stacks"
            if candidate.exists():
                return candidate
        return Path("knowledge/manifests/stacks")

    @staticmethod
    def _normalize(value: Optional[str]) -> str:
        return (value or "").strip().lower().replace(" ", "-")
