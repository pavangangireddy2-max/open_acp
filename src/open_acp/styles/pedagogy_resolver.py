"""Resolve pedagogy profiles from deterministic config."""
from pathlib import Path
from typing import Optional

import yaml


class PedagogyResolver:
    """Resolve the effective pedagogy profile for a domain/content_type pair."""

    def __init__(self, styles_dir: Optional[str] = None):
        if styles_dir:
            self.base_dir = Path(styles_dir)
        else:
            self.base_dir = Path(__file__).parent
        self.matrix_path = self.base_dir / "pedagogy" / "profile_matrix.yaml"

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

    def list_profiles(self) -> list[str]:
        """List profile files available under styles/pedagogy/profiles."""
        profiles_dir = self.base_dir / "pedagogy" / "profiles"
        if not profiles_dir.exists():
            return []
        return sorted(path.stem for path in profiles_dir.glob("*.yaml"))

    def _load_matrix(self) -> dict:
        if not self.matrix_path.exists():
            return {"global_default": "concept_progression"}
        with open(self.matrix_path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    @staticmethod
    def _normalize(value: Optional[str]) -> str:
        return (value or "").strip().lower().replace(" ", "-")
