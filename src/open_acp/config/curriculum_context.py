"""Shared loaders and resolvers for product, structure, and packaging context."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import yaml


def find_project_root() -> Path:
    current = Path(__file__).resolve()
    for ancestor in current.parents:
        if (ancestor / "pyproject.toml").exists():
            return ancestor
    return current.parents[3]


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(merged.get(key), dict) and isinstance(value, dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _normalize_token(value: Optional[str]) -> str:
    return (value or "").strip().lower().replace(" ", "_").replace("-", "_")


def _unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            ordered.append(value)
    return ordered


def load_stack_manifest(domain: Optional[str]) -> dict[str, Any]:
    normalized_domain = _normalize_token(domain)
    if not normalized_domain:
        return {}

    manifest_path = find_project_root() / "knowledge" / "manifests" / "stacks" / f"{normalized_domain}.yaml"
    data = load_yaml(manifest_path)
    if data:
        data["_manifest_path"] = str(manifest_path)
    return data


def load_product_manifest(product_family: Optional[str]) -> dict[str, Any]:
    manifests_root = find_project_root() / "knowledge" / "manifests" / "products"
    default_manifest_path = manifests_root / "default.yaml"
    default_manifest = load_yaml(default_manifest_path)

    normalized_family = _normalize_token(product_family)
    if not normalized_family or normalized_family == "default":
        if default_manifest:
            default_manifest["_manifest_path"] = str(default_manifest_path)
        return default_manifest

    product_manifest_path = manifests_root / f"{normalized_family}.yaml"
    product_manifest = load_yaml(product_manifest_path)
    merged = deep_merge(default_manifest, product_manifest)
    if merged:
        merged["_manifest_path"] = str(product_manifest_path if product_manifest else default_manifest_path)
    return merged


def resolve_product_context(
    domain: str,
    product_family: Optional[str] = None,
    product_version: Optional[str] = None,
) -> dict[str, Any]:
    explicit_product = bool(product_family)
    manifest = load_product_manifest(product_family)
    requested_version = str(product_version).strip() if product_version else ""
    versions = manifest.get("versions", {}) or {}

    resolved_version = requested_version or str(manifest.get("default_version", "") or "").strip()
    version_override = versions.get(resolved_version, {}) if resolved_version else {}
    resolved = deep_merge(manifest, version_override)

    feature_flags = resolved.get("feature_flags", {}) or {}
    packaging_overrides = resolved.get("packaging_overrides", {}) or {}
    notes = _unique(list(manifest.get("notes", []) or []) + list(version_override.get("notes", []) or []))

    if explicit_product:
        label = product_family if not resolved_version else f"{product_family} {resolved_version}"
        reason = f"explicit product selection: {product_family}{f'/{resolved_version}' if resolved_version else ''}"
    else:
        label = "Stack-only default"
        reason = "no product selected; using stack-only defaults"

    return {
        "domain": domain,
        "product_family": product_family if explicit_product else None,
        "product_version": resolved_version if explicit_product and resolved_version else None,
        "product_label": label,
        "product_category": resolved.get("product_category", "standard_product"),
        "structure_profile_id": resolved.get("default_structure_profile", "standard_product_structure"),
        "curriculum_container_kind": resolved.get("curriculum_container_kind", "standard_curriculum"),
        "default_packaging_profile_id": resolved.get("default_packaging_profile_id"),
        "focus_priority": resolved.get("focus_priority", "default"),
        "delivery_mode": resolved.get("delivery_mode"),
        "feature_flags": feature_flags,
        "packaging_overrides": packaging_overrides,
        "supported_domains": resolved.get("supported_domains", []),
        "variant_strategy": resolved.get("variant_strategy"),
        "notes": notes,
        "is_explicit_product": explicit_product,
        "resolution_reason": reason,
        "manifest_path": resolved.get("_manifest_path"),
    }


def load_structure_profile(structure_profile_id: Optional[str]) -> dict[str, Any]:
    profile_id = _normalize_token(structure_profile_id) or "standard_product_structure"
    profile_path = (
        find_project_root()
        / "knowledge"
        / "manifests"
        / "structure_profiles"
        / f"{profile_id}.yaml"
    )
    data = load_yaml(profile_path)
    if not data and profile_id != "standard_product_structure":
        profile_path = (
            find_project_root()
            / "knowledge"
            / "manifests"
            / "structure_profiles"
            / "standard_product_structure.yaml"
        )
        data = load_yaml(profile_path)
    if data:
        data["_manifest_path"] = str(profile_path)
    return data


def resolve_structure_profile(product_context: Optional[dict[str, Any]]) -> dict[str, Any]:
    product_context = product_context or {}
    profile_id = product_context.get("structure_profile_id") or "standard_product_structure"
    profile = load_structure_profile(profile_id)

    hierarchy = profile.get(
        "hierarchy",
        ["curriculum_container", "courses", "modules", "topics", "learning_units"],
    )
    return {
        "structure_profile_id": profile.get("structure_profile_id", profile_id),
        "label": profile.get("label", profile_id.replace("_", " ").title()),
        "curriculum_container_kind": profile.get(
            "curriculum_container_kind",
            product_context.get("curriculum_container_kind", "standard_curriculum"),
        ),
        "hierarchy": hierarchy,
        "design_priority_dimensions": profile.get("design_priority_dimensions", []),
        "notes": profile.get("notes", []),
        "manifest_path": profile.get("_manifest_path"),
        "resolution_reason": (
            f"product structure profile: {product_context.get('product_label', 'default')} -> "
            f"{profile.get('structure_profile_id', profile_id)}"
        ),
    }


def resolve_packaging_profile(
    domain: str,
    content_type: str,
    product_context: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    product_context = product_context or {}
    project_root = find_project_root()
    packaging_root = project_root / "knowledge" / "manifests" / "packaging"

    default_profile = load_yaml(packaging_root / "default.yaml")
    domain_override = load_yaml(packaging_root / f"{_normalize_token(domain)}.yaml")
    product_override = product_context.get("packaging_overrides", {}) or {}

    profile = deep_merge(default_profile, domain_override)
    profile = deep_merge(profile, product_override)

    profile.setdefault("version", 1)
    profile.setdefault("packaging_profile_id", f"{_normalize_token(domain)}_default")
    profile.setdefault(
        "allowed_learning_unit_types",
        ["video_session_unit", "reading_material_unit", "mcq_practice_unit"],
    )
    profile.setdefault("preferred_learning_unit_mix", profile["allowed_learning_unit_types"][:3])
    profile.setdefault(
        "module_count_per_course",
        {"default": 3, "min": 2, "max": 5, "target_hours_per_module": 8},
    )
    profile.setdefault("topic_count_per_module", {"default": 4, "min": 2, "max": 6})
    profile.setdefault("learning_units_per_topic", 3)
    profile.setdefault("classroom_quiz_every_minutes", 20)
    profile.setdefault("module_quiz_required", True)
    profile.setdefault("skill_assessment_every_n_topics", 8)
    profile.setdefault("skill_assessment_question_types", ["mcq", "coding", "fib", "project"])
    profile.setdefault("skill_assessment_difficulty_levels", ["easy", "medium", "hard"])
    profile["allowed_learning_unit_types"] = [
        "video_session_unit" if item == "ppt_video_unit" else item
        for item in profile.get("allowed_learning_unit_types", [])
    ]
    profile["preferred_learning_unit_mix"] = [
        "video_session_unit" if item == "ppt_video_unit" else item
        for item in profile.get("preferred_learning_unit_mix", [])
    ]
    profile["resolved_for"] = {
        "domain": domain,
        "content_type": content_type,
        "product_family": product_context.get("product_family"),
        "product_version": product_context.get("product_version"),
    }
    profile["product_feature_flags"] = product_context.get("feature_flags", {})
    return profile
