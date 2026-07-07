"""Loop B nodes — curriculum design using wiki intelligence."""
import json
from pathlib import Path
import re
from typing import Any

import yaml

from open_acp.knowledge.wiki_engine import WikiEngine
from open_acp.styles.pedagogy_resolver import PedagogyResolver
from open_acp.utils.claude import ClaudeClient
from open_acp.config.curriculum_context import (
    find_project_root,
    load_stack_manifest,
    load_yaml,
    resolve_packaging_profile as resolve_packaging_manifest_profile,
    resolve_product_context as resolve_product_manifest_context,
    resolve_structure_profile as resolve_structure_profile_context,
)


def _find_project_root() -> Path:
    return find_project_root()


def _design_artifact_dir(state: dict) -> Path:
    project_root = _find_project_root()
    domain = state.get("domain", "unknown")
    cycle_id = state.get("cycle_id", "cycle_1")
    return project_root / "storage" / "design" / domain / cycle_id


def _persist_design_artifact(state: dict, artifact_key: str, filename: str, payload: dict) -> tuple[str, dict[str, str]]:
    artifact_dir = _design_artifact_dir(state)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    path = artifact_dir / filename
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")
    artifact_paths = dict(state.get("design_artifact_paths", {}) or {})
    artifact_paths[artifact_key] = str(path)
    return str(path), artifact_paths


def _persist_design_collection_artifacts(
    state: dict,
    artifact_key: str,
    subdir: str,
    item_prefix: str,
    item_key: str,
    item_id_key: str,
    payload: dict,
) -> tuple[str, dict[str, str]]:
    artifact_dir = _design_artifact_dir(state) / subdir
    artifact_dir.mkdir(parents=True, exist_ok=True)

    index_path = artifact_dir / "index.yaml"
    index_path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")

    for item in payload.get(item_key, []) or []:
        item_id = item.get(item_id_key)
        if not item_id:
            continue
        item_path = artifact_dir / f"{item_prefix}.{item_id}.yaml"
        item_path.write_text(yaml.safe_dump(item, sort_keys=False, allow_unicode=False), encoding="utf-8")

    artifact_paths = dict(state.get("design_artifact_paths", {}) or {})
    artifact_paths[artifact_key] = str(index_path)
    return str(index_path), artifact_paths


def _load_design_artifact(state: dict, artifact_key: str, state_key: str, filename: str) -> dict:
    in_state = state.get(state_key, {}) or {}
    if in_state:
        return in_state

    artifact_paths = state.get("design_artifact_paths", {}) or {}
    path_value = artifact_paths.get(artifact_key)
    if not path_value:
        candidate = _design_artifact_dir(state) / filename
        if candidate.exists():
            path_value = str(candidate)

    if not path_value:
        return {}

    path = Path(path_value)
    if not path.exists():
        return {}

    loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(loaded, dict):
        return {}
    return loaded


def _validate_curriculum_hours(curriculum: dict, packaging_profile: dict, time_budget_context: dict) -> dict:
    target_total = float(
        time_budget_context.get("target_total_hours")
        or packaging_profile.get("total_hours")
        or 0
    )
    curriculum_total = float(curriculum.get("total_hours", 0) or 0)
    courses = curriculum.get("courses", []) or []
    course_hours_sum = round(sum(float(course.get("estimated_hours", 0) or 0) for course in courses), 2)
    capstone_hours = round(float((curriculum.get("capstone_project") or {}).get("estimated_hours", 0) or 0), 2)
    grand_quiz_hours = round(float((curriculum.get("grand_quiz") or {}).get("estimated_hours", 0) or 0), 2)
    accounted_total = round(course_hours_sum + capstone_hours + grand_quiz_hours, 2)
    time_tolerance = packaging_profile.get("time_tolerance")
    if time_tolerance is not None:
        tolerance_hours = round(float(time_tolerance) * max(target_total, curriculum_total, 1.0), 2)
    else:
        tolerance_hours = float(packaging_profile.get("curriculum_hours_tolerance", 0.5) or 0.5)

    issues: list[str] = []
    if abs(accounted_total - curriculum_total) > tolerance_hours:
        issues.append(
            "Sum of course hours plus capstone and grand quiz "
            f"({accounted_total}) does not match curriculum total ({curriculum_total}) within tolerance {tolerance_hours}."
        )
    if target_total and abs(curriculum_total - target_total) > tolerance_hours:
        issues.append(
            f"Curriculum total ({curriculum_total}) does not match resolved target total ({target_total}) within tolerance {tolerance_hours}."
        )

    return {
        "target_total_hours": target_total,
        "curriculum_total_hours": curriculum_total,
        "course_hours_sum": course_hours_sum,
        "capstone_hours": capstone_hours,
        "grand_quiz_hours": grand_quiz_hours,
        "accounted_total_hours": accounted_total,
        "tolerance_hours": tolerance_hours,
        "within_tolerance": not issues,
        "issues": issues,
    }


def _normalize_curriculum_payload(data: dict) -> dict:
    """Ensure optional Stage 1 curriculum keys exist before validation/persistence."""
    data.setdefault("courses", [])
    data.setdefault("capstone_project", {})
    data.setdefault("grand_quiz", {})
    data.setdefault("hours_check", {})
    return data


def _parse_json_object_response(response: str) -> dict:
    """Parse a JSON object from a model response with light cleanup."""
    cleaned = response.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned[cleaned.index("\n") + 1:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(cleaned[start:end + 1])
        raise


def _looks_like_truncated_json(response: str) -> bool:
    cleaned = response.strip()
    if not cleaned:
        return False
    if cleaned.startswith("```"):
        cleaned = cleaned[cleaned.index("\n") + 1:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()
    if cleaned.startswith("{") and not cleaned.endswith("}"):
        return True
    return cleaned.count("{") > cleaned.count("}")


def _load_curriculum_sources(domain: str) -> str:
    """Load optional stack curriculum source docs from the stack manifest."""
    project_root = _find_project_root()
    manifest_path = project_root / "knowledge" / "manifests" / "stacks" / f"{domain}.yaml"
    if not manifest_path.exists():
        return ""

    with open(manifest_path, encoding="utf-8") as f:
        manifest = yaml.safe_load(f) or {}

    parts: list[str] = []
    for source_path in manifest.get("curriculum_sources", []):
        resolved = project_root / source_path
        if not resolved.exists():
            continue
        parts.append(f"### Source: {source_path}\n{resolved.read_text(encoding='utf-8')[:12000]}")

    return "\n\n".join(parts)


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "item"


def _unique_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            ordered.append(value)
    return ordered


def _resolve_configured_count(estimated_hours: float, rule: dict) -> int:
    default = int(rule.get("default", 4))
    min_count = int(rule.get("min", default))
    max_count = int(rule.get("max", default))
    target_hours = float(rule.get("target_hours_per_module", 0) or 0)

    if target_hours > 0 and estimated_hours > 0:
        count = max(1, round(estimated_hours / target_hours))
    else:
        count = default

    return max(min_count, min(max_count, count))


def _course_skill_ids(course_seed: dict) -> list[str]:
    return _unique_preserve_order(
        skill_id
        for objective in course_seed.get("objectives", [])
        for skill_id in objective.get("skill_ids", [])
    )


def _course_objective_statements(course_seed: dict) -> list[str]:
    return [
        objective.get("statement", "")
        for objective in course_seed.get("objectives", [])
        if objective.get("statement")
    ]


def _module_phase_labels(packaging_profile: dict) -> list[str]:
    return packaging_profile.get(
        "module_phase_labels",
        ["Foundations", "Core workflow", "Practice and integration", "Assessment readiness"],
    )


def _topic_phase_labels(packaging_profile: dict, pedagogy_profile: str) -> list[str]:
    if pedagogy_profile == "project_build_along":
        return packaging_profile.get(
            "topic_phase_labels",
            ["Problem framing", "Architecture and concepts", "Guided build", "Checkpoint and quiz"],
        )
    return packaging_profile.get(
        "topic_phase_labels",
        ["Motivation and framing", "Core concepts", "Worked practice", "Checkpoint and recap"],
    )


def _learning_unit_label(unit_type: str) -> str:
    mapping = {
        "video_session_unit": "Video session",
        "reading_material_unit": "Reading material",
        "mcq_practice_unit": "MCQ practice",
        "coding_practice_unit": "Coding practice",
    }
    return mapping.get(unit_type, unit_type.replace("_", " ").title())


def _assessment_question_types_for_topic(topic: dict, units_for_topic: list[dict]) -> list[str]:
    question_types = ["mcq", "fib"]
    if any(unit.get("unit_type") == "coding_practice_unit" for unit in units_for_topic):
        question_types.append("coding")
    if "checkpoint" in topic.get("title", "").lower() or "quiz" in topic.get("title", "").lower():
        question_types.append("short_answer")
    return _unique_preserve_order(question_types)


def _assessment_difficulty(topic_sequence: int, topic_count: int, tags: list[str] | None = None) -> str:
    """Determine assessment difficulty from sequence position and C/L tags."""
    # v9: L-tag overrides when available
    if tags:
        for tag in tags:
            if tag == "L3":
                return "hard"
            if tag == "L1" and topic_sequence == 1:
                return "easy"

    if topic_count <= 1:
        return "medium"
    if topic_sequence == 1:
        return "easy"
    if topic_sequence >= topic_count:
        return "hard"
    return "medium"


def _extract_keywords(texts: list[str]) -> list[str]:
    stopwords = {
        "and", "for", "with", "that", "this", "from", "into", "over", "under", "course",
        "module", "topic", "level", "using", "build", "guided", "core", "concepts", "practice",
    }
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9_+-]*", " ".join(texts).lower())
    return _unique_preserve_order([word for word in words if len(word) >= 4 and word not in stopwords])


def _product_summary(product_context: dict) -> str:
    return "\n".join(
        [
            f"- Product label: {product_context.get('product_label', 'Stack-only default')}",
            f"- Product category: {product_context.get('product_category', 'standard_product')}",
            f"- Curriculum container kind: {product_context.get('curriculum_container_kind', 'standard_curriculum')}",
            f"- Delivery mode: {product_context.get('delivery_mode', 'unspecified')}",
            f"- Focus priority: {product_context.get('focus_priority', 'default')}",
        ]
    )


def _structure_summary(structure_profile: dict) -> str:
    return "\n".join(
        [
            f"- Structure profile: {structure_profile.get('structure_profile_id', 'standard_product_structure')}",
            (
                f"- Hierarchy: {' -> '.join(structure_profile.get('hierarchy', [])) or 'curriculum_container -> courses -> modules -> topics -> learning_units'}"
            ),
            (
                f"- Design priorities: {', '.join(structure_profile.get('design_priority_dimensions', [])) or 'default'}"
            ),
        ]
    )


def _packaging_summary(packaging_profile: dict) -> str:
    return "\n".join(
        [
            f"- Packaging profile: {packaging_profile.get('packaging_profile_id', 'default_learning_packaging')}",
            f"- Modules per course default: {packaging_profile.get('module_count_per_course', {}).get('default', 'unknown')}",
            f"- Topics per module default: {packaging_profile.get('topic_count_per_module', {}).get('default', 'unknown')}",
            f"- Learning unit types: {', '.join(packaging_profile.get('allowed_learning_unit_types', [])) or 'none'}",
        ]
    )


def _stack_course_abstract_summary(domain: str) -> str:
    stack_manifest = load_stack_manifest(domain)
    abstract_ref = stack_manifest.get("stack_curriculum_abstract_ref")
    if abstract_ref:
        abstract_path = _find_project_root() / abstract_ref
        if abstract_path.exists():
            payload = yaml.safe_load(abstract_path.read_text(encoding="utf-8")) or {}
            return yaml.safe_dump(payload, sort_keys=False, allow_unicode=False)

    canonical_titles = stack_manifest.get("canonical_course_titles", []) or []
    course_variants = stack_manifest.get("course_variants", []) or []

    sections = [
        f"- Catalog label: {stack_manifest.get('catalog_label', domain.title())}",
        f"- Canonical course titles: {', '.join(canonical_titles) or 'none'}",
    ]
    if course_variants:
        sections.append("### Canonical Course Variants")
        for variant in course_variants[:8]:
            if isinstance(variant, dict):
                variant_id = variant.get("course_variant_id") or variant.get("variant_id") or "unknown_variant"
                base_course = variant.get("canonical_course_id") or variant.get("base_course_id") or "unknown_course"
                audience = variant.get("audience") or variant.get("product_family") or "unspecified"
                sections.append(f"- {variant_id}: base={base_course}, audience={audience}")
            else:
                sections.append(f"- {variant}")
    else:
        sections.append("### Canonical Course Variants\n- none declared")

    return "\n".join(sections)


def _product_course_overlay_summary(product_context: dict) -> str:
    product_only_courses = product_context.get("product_only_courses", []) or []
    course_variant_overrides = product_context.get("course_variant_overrides", {}) or {}

    sections = [
        f"- Product label: {product_context.get('product_label', 'Stack-only default')}",
        f"- Variant strategy: {product_context.get('variant_strategy', 'none') or 'none'}",
        "### Product-only Courses",
    ]
    if product_only_courses:
        for course in product_only_courses[:8]:
            course_id = course.get("course_id", "unknown_course")
            title = course.get("title", course_id)
            placement = course.get("insertion", course.get("placement", "append"))
            hours = course.get("estimated_hours", course.get("default_hours", "unknown"))
            sections.append(f"- {course_id}: {title} (placement={placement}, hours={hours})")
    else:
        sections.append("- none declared")

    sections.append("### Course Variant Overrides")
    if course_variant_overrides:
        for canonical_course_id, override in list(course_variant_overrides.items())[:12]:
            if isinstance(override, dict):
                variant_id = override.get("course_variant_id", "unspecified_variant")
                reason = override.get("reason", "not provided")
                sections.append(f"- {canonical_course_id}: {variant_id} ({reason})")
            else:
                sections.append(f"- {canonical_course_id}: {override}")
    else:
        sections.append("- none declared")

    return "\n".join(sections)


def _extract_total_hours_from_curriculum_source(curriculum_source_context: str) -> float | None:
    if not curriculum_source_context:
        return None
    patterns = [
        r"(\d+(?:\.\d+)?)\s*(?:hour|hours|hr|hrs)\b",
        r"(\d+(?:\.\d+)?)h\b",
    ]
    for pattern in patterns:
        matches = re.findall(pattern, curriculum_source_context, flags=re.IGNORECASE)
        if matches:
            try:
                return float(matches[0])
            except ValueError:
                continue
    return None


def _design_priority_label(dimension_id: str) -> str:
    labels = {
        "job_placement_outcomes": "job_placement_outcomes",
        "student_learning_outcomes": "student_learning_outcomes",
        "degree_and_higher_ed_outcomes": "degree_and_higher_ed_outcomes",
        "regulatory_compliance": "regulatory_compliance",
        "university_policy_and_infra_constraints": "university_policy_and_infra_constraints",
        "operational_efficiency": "operational_efficiency",
        "cross_product_alignment": "cross_product_alignment",
        "industry_partnerships_and_certifications": "industry_partnerships_and_certifications",
        "market_and_community_signals": "market_and_community_signals",
        "customer_and_sales_intelligence": "customer_and_sales_intelligence",
        "internal_expertise": "internal_expertise",
    }
    return labels.get(dimension_id, dimension_id)


def _build_design_priority_summary(profile: dict) -> str:
    dimensions = profile.get("ordered_dimensions") or profile.get("dimension_ids") or []
    return "\n".join(
        [
            f"- Design priority profile: {profile.get('profile_id', 'default_design_priorities')}",
            f"- Ordered dimensions: {', '.join(dimensions) or 'none'}",
            f"- Focus priority: {profile.get('focus_priority', 'default')}",
            f"- Resolution reason: {profile.get('resolution_reason', 'not provided')}",
        ]
    )


def _build_time_budget_summary(context: dict) -> str:
    return "\n".join(
        [
            f"- Time budget context: {context.get('context_id', 'unknown')}",
            f"- Source total hours: {context.get('source_total_hours', 'unknown')}",
            f"- Packaging total hours: {context.get('packaging_total_hours', 'unknown')}",
            f"- Target total hours: {context.get('target_total_hours', 'unknown')}",
            f"- Slot budget hours: {context.get('slot_budget_hours', 'unknown')}",
            f"- Reserved hours: {context.get('reserved_hours', 'unknown')}",
            f"- Available design hours: {context.get('available_design_hours', 'unknown')}",
            f"- Resolution reason: {context.get('resolution_reason', 'not provided')}",
        ]
    )


def _build_skill_outcomes_digest_summary(digest: dict) -> str:
    if not digest:
        return "- No skill-outcomes digest available."

    target_roles = digest.get("target_roles", []) or []
    role_lines = []
    for role in target_roles[:5]:
        if isinstance(role, dict):
            role_id = role.get("role_id") or role.get("title") or "unknown_role"
            priority = role.get("priority") or role.get("evidence_strength")
            if priority is not None:
                role_lines.append(f"- {role_id} ({priority})")
            else:
                role_lines.append(f"- {role_id}")
        else:
            role_lines.append(f"- {role}")

    clusters = digest.get("skill_priority_clusters", []) or []
    cluster_lines = []
    for cluster in clusters[:5]:
        if isinstance(cluster, dict):
            cluster_id = cluster.get("cluster_id") or cluster.get("title") or "unknown_cluster"
            skill_ids = ", ".join(cluster.get("skill_ids", [])[:5]) or "none"
            cluster_lines.append(f"- {cluster_id}: {skill_ids}")
        else:
            cluster_lines.append(f"- {cluster}")

    pattern_highlights = digest.get("pattern_highlights", []) or []
    unresolved_inputs = digest.get("unresolved_inputs", []) or []
    source_refs = digest.get("source_refs", []) or []

    sections = [
        "## Skill Outcomes Digest",
        f"- Digest id: {digest.get('digest_id', 'unknown')}",
        f"- Source refs: {', '.join(source_refs) or 'none'}",
        "### Target Roles",
        "\n".join(role_lines) if role_lines else "- none",
        "### Skill Priority Clusters",
        "\n".join(cluster_lines) if cluster_lines else "- none",
        "### Pattern Highlights",
        "\n".join(f"- {highlight}" for highlight in pattern_highlights[:5]) if pattern_highlights else "- none",
        "### Unresolved Inputs",
        "\n".join(f"- {item}" for item in unresolved_inputs[:5]) if unresolved_inputs else "- none",
    ]
    return "\n".join(sections)


def _build_market_and_community_digest_summary(digest: dict) -> str:
    if not digest:
        return "- No market-and-community digest available."

    source_refs = digest.get("source_refs", []) or []
    competitor_refs = digest.get("competitor_signal_refs", []) or []
    market_refs = digest.get("market_signal_refs", []) or []
    pressures = digest.get("competitive_pressures", []) or digest.get("market_pressures", []) or []
    pattern_highlights = digest.get("pattern_highlights", []) or []
    unresolved_inputs = digest.get("unresolved_inputs", []) or []

    pressure_lines = []
    for pressure in pressures[:5]:
        if isinstance(pressure, dict):
            label = pressure.get("pressure_id") or pressure.get("title") or "unknown_pressure"
            summary = pressure.get("summary") or pressure.get("notes") or ""
            pressure_lines.append(f"- {label}: {summary}".rstrip(": "))
        else:
            pressure_lines.append(f"- {pressure}")

    sections = [
        "## Market And Community Digest",
        f"- Digest id: {digest.get('digest_id', 'unknown')}",
        f"- Source refs: {', '.join(source_refs) or 'none'}",
        f"- Competitor refs: {', '.join(competitor_refs) or 'none'}",
        f"- Market refs: {', '.join(market_refs) or 'none'}",
        "### Competitive And Market Pressures",
        "\n".join(pressure_lines) if pressure_lines else "- none",
        "### Pattern Highlights",
        "\n".join(f"- {highlight}" for highlight in pattern_highlights[:5]) if pattern_highlights else "- none",
        "### Unresolved Inputs",
        "\n".join(f"- {item}" for item in unresolved_inputs[:5]) if unresolved_inputs else "- none",
    ]
    return "\n".join(sections)


def _extract_source_refs(curriculum_source_context: str) -> list[str]:
    refs = re.findall(r"^### Source: (.+)$", curriculum_source_context or "", flags=re.MULTILINE)
    return _unique_preserve_order([ref.strip() for ref in refs if ref.strip()])


def _default_stack_name(domain: str, curriculum_source_context: str) -> str:
    heading_match = re.search(r"^#\s+(.+)$", curriculum_source_context or "", flags=re.MULTILINE)
    if heading_match:
        heading = heading_match.group(1).strip()
        heading = re.sub(r"\s+(Seed|Reference|Source)$", "", heading, flags=re.IGNORECASE).strip()
        if heading:
            return heading

    stack_manifest = load_stack_manifest(domain)
    catalog_label = stack_manifest.get("catalog_label")
    if catalog_label:
        return f"{catalog_label} Stack Curriculum"

    return f"{domain.title()} Stack Curriculum"


def _extract_markdown_bullets(section_text: str, limit: int = 8) -> list[str]:
    bullets: list[str] = []
    for line in (section_text or "").splitlines():
        stripped = line.strip()
        if stripped.startswith("- **") and "**" in stripped[4:]:
            title = stripped[4:]
            title = title.split("**", 1)[0].strip()
            if title:
                bullets.append(_slugify(title))
        elif stripped.startswith("- "):
            value = stripped[2:].strip()
            if value:
                bullets.append(_slugify(value))
        if len(bullets) >= limit:
            break
    return _unique_preserve_order(bullets)


def _default_coverage_policy(domain: str, track_abstract: dict | None) -> dict:
    """Build default coverage_policy_per_stack from track abstract or sensible defaults."""
    if track_abstract:
        policy = {}
        for cs in track_abstract.get("contributing_stacks", []):
            if isinstance(cs, dict):
                stack_id = cs.get("stack_id", domain)
                policy[stack_id] = {
                    "include_tags": cs.get("include_tags", ["C1", "C2"]),
                    "include_levels": cs.get("include_levels", ["L1", "L2"]),
                }
        if policy:
            return policy
    return {domain: {"include_tags": ["C1", "C2"], "include_levels": ["L1", "L2"]}}


def _default_allowed_local_overrides(profile: str) -> list[str]:
    mapping = {
        "project_build_along": ["concept_progression", "tool_workflow"],
        "concept_progression": ["skill_drill", "case_reasoning"],
        "skill_drill": ["concept_progression"],
        "case_reasoning": ["concept_progression"],
        "tool_workflow": ["concept_progression", "project_build_along"],
    }
    return mapping.get(profile, [])


def _fallback_stack_learning_outcomes(domain: str, pedagogy_profile: str, curriculum_source_context: str) -> list[str]:
    source_text = curriculum_source_context.lower()
    if domain == "genai":
        outcomes = [
            "Build and deploy a document-grounded GenAI application",
            "Implement retrieval, tool use, and evaluation in GenAI systems",
            "Ship a milestone-based AI workflow with production constraints",
        ]
        if "agent" in source_text:
            outcomes.append("Build and evaluate an agent with tool use")
        return outcomes[:5]

    if pedagogy_profile == "skill_drill":
        return [
            f"Demonstrate timed proficiency in core {domain} problem patterns",
            f"Apply {domain} concepts under assessment-style constraints",
        ]

    return [
        f"Apply core {domain} concepts in realistic scenarios",
        f"Demonstrate observable {domain} skills through guided outputs",
    ]


def load_stack_abstracts(state: dict) -> dict:
    """Load stack curriculum abstracts, track abstract, and domain definition into state.

    Sources (in priority order):
    1. Loop A artifacts from storage/intelligence/{domain}/{cycle_id}/
    2. Seed manifests from knowledge/manifests/
    """
    domain = state.get("domain", "unknown")
    cycle_id = state.get("cycle_id", "cycle_1")
    project_root = _find_project_root()

    # --- Domain definition ---
    domain_def = None
    # Try Loop A artifact first
    artifact_path = project_root / "storage" / "intelligence" / domain / cycle_id / "domain_definition.yaml"
    if artifact_path.exists():
        domain_def = yaml.safe_load(artifact_path.read_text(encoding="utf-8"))
    if not domain_def:
        # Fall back to seed manifest
        seed_path = project_root / "knowledge" / "manifests" / "domains" / f"{domain}.yaml"
        if seed_path.exists():
            domain_def = yaml.safe_load(seed_path.read_text(encoding="utf-8"))

    # --- Stack curriculum abstract ---
    stack_abstracts = {}
    # Try Loop A artifact
    abstract_artifact = project_root / "storage" / "intelligence" / domain / cycle_id / "stack_curriculum_abstract.yaml"
    if abstract_artifact.exists():
        abstract = yaml.safe_load(abstract_artifact.read_text(encoding="utf-8"))
        if abstract:
            stack_id = abstract.get("stack_id", domain)
            stack_abstracts[stack_id] = abstract
    if not stack_abstracts:
        # Fall back to seed abstract
        seed_abstract = project_root / "knowledge" / "manifests" / "stacks" / f"{domain}_curriculum_abstract.yaml"
        if seed_abstract.exists():
            abstract = yaml.safe_load(seed_abstract.read_text(encoding="utf-8"))
            if abstract:
                stack_abstracts[abstract.get("stack_id", domain)] = abstract

    # --- Track abstract ---
    track_abstract = None
    # Check if domain definition points to tracks, try to load matching track
    if domain_def:
        stacks = domain_def.get("stacks", [])
        # Search for any track that lists these stacks as contributing
        tracks_dir = project_root / "knowledge" / "manifests" / "tracks"
        if tracks_dir.exists():
            for track_file in sorted(tracks_dir.glob("*.yaml")):
                track_data = yaml.safe_load(track_file.read_text(encoding="utf-8")) or {}
                contributing_stacks = [
                    cs.get("stack_id") if isinstance(cs, dict) else cs
                    for cs in track_data.get("contributing_stacks", [])
                ]
                if domain in contributing_stacks or any(s in contributing_stacks for s in stacks):
                    track_abstract = track_data
                    break  # Take the first matching track

    abstract_count = sum(len(a.get("modules", [])) for a in stack_abstracts.values())
    print(
        f"  Stack abstracts loaded: {len(stack_abstracts)} stack(s), "
        f"{abstract_count} total module(s), "
        f"track={'yes' if track_abstract else 'none'}"
    )
    return {
        "domain_definition": domain_def,
        "stack_abstracts": stack_abstracts if stack_abstracts else None,
        "track_abstract": track_abstract,
    }


def resolve_design_priority_profile(state: dict) -> dict:
    """Resolve the active design-priority dimensions from structure and product context."""
    structure_profile = state.get("structure_profile", {}) or {}
    product_context = state.get("product_context", {}) or {}
    dimension_ids = [
        _design_priority_label(dimension_id)
        for dimension_id in structure_profile.get("design_priority_dimensions", [])
    ]
    ordered_dimensions = _unique_preserve_order(dimension_ids)
    profile = {
        "profile_id": f"{structure_profile.get('structure_profile_id', 'standard_product_structure')}_design_priorities",
        "dimension_ids": ordered_dimensions,
        "ordered_dimensions": ordered_dimensions,
        "dimensions": [{"dimension_id": dimension_id} for dimension_id in ordered_dimensions],
        "focus_priority": product_context.get("focus_priority", "default"),
        "resolution_reason": (
            f"structure profile {structure_profile.get('structure_profile_id', 'standard_product_structure')} "
            "defines the active design-priority dimensions"
        ),
    }
    print(f"  Design priorities: {len(ordered_dimensions)} dimensions resolved")
    return {"design_priority_profile": profile}


def resolve_time_budget_context(state: dict) -> dict:
    """Resolve a structured time-budget object for the current curriculum-design run."""
    curriculum_source_context = state.get("curriculum_source_context", "") or ""
    packaging_profile = state.get("packaging_profile", {}) or {}
    domain = state.get("domain", "unknown")

    source_total_hours = _extract_total_hours_from_curriculum_source(curriculum_source_context)
    packaging_total_hours = packaging_profile.get("total_hours")
    target_total_hours = (
        float(packaging_total_hours)
        if packaging_total_hours is not None
        else (source_total_hours if source_total_hours is not None else 20.0)
    )
    slot_budget_hours = target_total_hours
    reserved_hours = float(packaging_profile.get("reserved_hours", 0.0) or 0.0)
    available_design_hours = max(0.0, round(slot_budget_hours - reserved_hours, 2))

    if packaging_total_hours is not None and source_total_hours is not None:
        reason = "packaging-owned total hours resolved and cross-checked against the source curriculum"
    elif packaging_total_hours is not None:
        reason = "packaging-owned total hours resolved from canonical packaging profile"
    elif source_total_hours is not None:
        reason = "source-defined total hours used because packaging profile does not declare total hours"
    else:
        reason = "no explicit source total hours found; using default planning budget"

    context = {
        "context_id": f"time_budget_{_slugify(domain)}",
        "source_total_hours": source_total_hours,
        "packaging_total_hours": float(packaging_total_hours) if packaging_total_hours is not None else None,
        "target_total_hours": target_total_hours,
        "slot_budget_hours": slot_budget_hours,
        "reserved_hours": reserved_hours,
        "available_design_hours": available_design_hours,
        "source_vs_packaging_conflict": (
            packaging_total_hours is not None
            and source_total_hours is not None
            and abs(float(packaging_total_hours) - float(source_total_hours)) > 0.01
        ),
        "resolution_reason": reason,
    }

    print(f"  Time budget: target {target_total_hours} hours")
    return {"time_budget_context": context}


def load_wiki_context(state: dict) -> dict:
    """Load skill graph and learner model from wiki entities."""
    wiki = WikiEngine()
    domain = state.get("domain", "ml-engineering")
    skill_outcomes_digest = state.get("skill_outcomes_signal_digest", {}) or {}
    market_and_community_digest = state.get("market_and_community_digest", {}) or {}

    # Gather skill entities
    skills = wiki.list_entities(entity_type="skill")
    skill_context = "## Skills in Wiki\n"
    for s in skills:
        entity = wiki.get_entity("skill", s["entity_id"])
        if entity:
            skill_context += f"- **{s['title']}** (confidence={s['confidence']:.2f}, durability={s.get('durability', '?')})\n"

    stack_skill_profiles = wiki.list_stack_profiles(stack_id=domain, entity_type="skill")
    if stack_skill_profiles:
        skill_context += "\n## Stack Skill Profiles\n"
        for profile in stack_skill_profiles[:20]:
            skill_context += (
                f"- **{profile['title']}** "
                f"(relevance={profile.get('relevance_score', 0.0):.2f}, "
                f"role={profile.get('role_in_stack', 'unknown')})\n"
            )

    # Gather learner entities
    learners = wiki.list_entities(entity_type="audience_segment")
    learner_context = "## Learner Segments\n"
    for l in learners:
        entity = wiki.get_entity("audience_segment", l["entity_id"])
        if entity:
            learner_context += f"- **{l['title']}**: {entity['content'][:300]}\n"

    curriculum_source_context = _load_curriculum_sources(domain)
    skill_outcomes_context = _build_skill_outcomes_digest_summary(skill_outcomes_digest)
    market_and_community_context = _build_market_and_community_digest_summary(market_and_community_digest)

    print(f"  Wiki context loaded: {len(skills)} skills, {len(learners)} learner segments")
    return {
        "skill_graph_context": skill_context,
        "learner_context": learner_context,
        "skill_outcomes_context": skill_outcomes_context,
        "market_and_community_context": market_and_community_context,
        "curriculum_source_context": curriculum_source_context,
    }


def resolve_product_context(state: dict) -> dict:
    """Resolve explicit product context or fall back to stack-only defaults."""
    domain = state.get("domain", "ml-engineering")
    existing_context = state.get("product_context", {}) or {}
    product_family = state.get("product_family") or existing_context.get("product_family")
    product_version = state.get("product_version") or existing_context.get("product_version")
    require_product_context = bool(state.get("require_product_context", False))

    context = resolve_product_manifest_context(
        domain=domain,
        product_family=product_family,
        product_version=product_version,
    )
    if require_product_context and not context.get("is_explicit_product"):
        raise ValueError(
            "Explicit product context is required for this run. "
            "Provide product_family and product_version instead of relying on stack-only defaults."
        )

    print(f"  Product context: {context.get('product_label', 'Stack-only default')}")
    return {
        "product_family": context.get("product_family"),
        "product_version": context.get("product_version"),
        "product_context": context,
    }


def resolve_structure_profile(state: dict) -> dict:
    """Resolve the structure profile that should shape curriculum containers."""
    context = state.get("product_context") or resolve_product_manifest_context(
        domain=state.get("domain", "ml-engineering"),
        product_family=state.get("product_family"),
        product_version=state.get("product_version"),
    )
    profile = resolve_structure_profile_context(context)

    print(f"  Structure profile: {profile.get('structure_profile_id', 'standard_product_structure')}")
    return {"structure_profile": profile}


def generate_brief(state: dict) -> dict:
    """Generate a Stage 0 curriculum brief artifact from resolved context."""
    domain = state.get("domain", "ml-engineering")
    product_context = state.get("product_context", {}) or {}
    structure_profile = state.get("structure_profile", {}) or {}
    packaging_profile = state.get("packaging_profile", {}) or {}
    design_priority_profile = state.get("design_priority_profile", {}) or {}
    time_budget_context = state.get("time_budget_context", {}) or {}
    pedagogy_profile = state.get("pedagogy_profile", "concept_progression")
    pedagogy_rationale = state.get("pedagogy_rationale", "content-type default")
    skill_context = state.get("skill_graph_context", "")
    learner_context = state.get("learner_context", "")
    skill_outcomes_context = state.get("skill_outcomes_context", "")
    market_and_community_context = state.get("market_and_community_context", "")
    curriculum_source_context = state.get("curriculum_source_context") or state.get("program_context", "")

    # v9: stack abstract context for coverage policy
    stack_abstracts = state.get("stack_abstracts", {}) or {}
    track_abstract = state.get("track_abstract")

    product_summary = _product_summary(product_context)
    structure_summary = _structure_summary(structure_profile)
    packaging_summary = _packaging_summary(packaging_profile)
    design_priority_summary = _build_design_priority_summary(design_priority_profile)
    time_budget_summary = _build_time_budget_summary(time_budget_context)
    source_refs = _extract_source_refs(curriculum_source_context)
    source_hours_declared = time_budget_context.get("source_total_hours")
    source_vs_packaging_conflict = bool(time_budget_context.get("source_vs_packaging_conflict", False))
    default_stack_name = _default_stack_name(domain, curriculum_source_context)

    # Build abstract module catalog summary for the prompt
    abstract_summary_lines: list[str] = []
    for stack_id, abstract in stack_abstracts.items():
        modules = abstract.get("modules", []) or []
        if not modules:
            continue
        abstract_summary_lines.append(f"\n### Stack: {stack_id} ({len(modules)} modules)")
        for mod in modules[:15]:
            tags = mod.get("tags", [])
            hours = mod.get("estimated_hours_range", {})
            hr_str = f"{hours.get('min', '?')}-{hours.get('max', '?')}h" if isinstance(hours, dict) else str(hours)
            abstract_summary_lines.append(
                f"- {mod.get('module_id', '?')}: {mod.get('title', '?')} "
                f"[{', '.join(tags)}] {hr_str} freq={mod.get('interview_frequency', '?')}"
            )
        if len(modules) > 15:
            abstract_summary_lines.append(f"  ... and {len(modules) - 15} more")
    abstract_context = "\n".join(abstract_summary_lines) if abstract_summary_lines else "No stack curriculum abstracts available."

    # Track abstract context
    track_context = ""
    if track_abstract:
        track_context = f"\n## Track Abstract: {track_abstract.get('display_name', track_abstract.get('track_id', '?'))}"
        for cs in track_abstract.get("contributing_stacks", []):
            if isinstance(cs, dict):
                track_context += f"\n- {cs.get('stack_id', '?')}: tags={cs.get('include_tags', [])}, levels={cs.get('include_levels', [])}"

    claude = ClaudeClient()
    prompt = f"""Create a Stage 0 curriculum brief for the "{domain}" stack.

## Curriculum Source Context
{curriculum_source_context or "No explicit curriculum source provided."}

## Product Context
{product_summary}

## Structure Profile
{structure_summary}

## Packaging Context
{packaging_summary}

## Design Priority Profile
{design_priority_summary}

## Time Budget Context
{time_budget_summary}

## Skill Outcomes Digest
{skill_outcomes_context or "No explicit skill-outcomes digest provided."}

## Market And Community Digest
{market_and_community_context or "No explicit market/community digest provided."}

## Skill Context
{skill_context or "No explicit skill context provided."}

## Learner Context
{learner_context or "No explicit learner context provided."}

## Stack Curriculum Abstract (C/L Tagged Module Catalog)
{abstract_context}
{track_context}

Decide only the Stage 0 brief:
1. Stack name
2. Primary target learner segments (maximum 2)
3. Default pedagogy profile and allowed local overrides
4. Stack learning outcomes (maximum 5, observable verbs only)
5. Minimum product context downstream stages need
6. Cross-check the declared source hours against the packaging profile target hours and mark the conflict flag

Return JSON:
{{
  "brief_id": "brief_{domain}",
  "stack_name": "Stack name",
  "packaging_profile_ref": "{packaging_profile.get('packaging_profile_id', 'default_learning_packaging')}",
  "product_context": {{
    "product_label": "{product_context.get('product_label', 'Stack-only default')}",
    "delivery_mode": "{product_context.get('delivery_mode', 'unspecified')}",
    "curriculum_container_kind": "{product_context.get('curriculum_container_kind', 'standard_curriculum')}"
  }},
  "audience": {{
    "primary": ["audience_segment_id"],
    "english_level": 8
  }},
  "pedagogy": {{
    "default_profile": "{pedagogy_profile}",
    "allowed_local_overrides": ["concept_progression"]
  }},
  "stack_learning_outcomes": [
    "Observable stack learning outcome"
  ],
  "source_refs": {json.dumps(source_refs)},
  "source_hours_declared": {json.dumps(source_hours_declared)},
  "source_vs_packaging_conflict": {json.dumps(source_vs_packaging_conflict)},
  "coverage_policy_per_stack": {{
    "{domain}": {{
      "include_tags": ["C1", "C2"],
      "include_levels": ["L1", "L2"]
    }}
  }}
}}

Important constraints:
- Stack learning outcomes must use observable verbs, not vague verbs like understand or know.
- Keep primary audience to at most 2 segments.
- Use the resolved pedagogy profile unless the sources clearly justify a different default.
- Do not design courses, modules, topics, or content yet.
- Do not introduce success metrics, differentiation strategy, or hour allocation into this artifact.
- If stack curriculum abstracts are available, decide which C-tags (C1/C2/C3) and L-tags (L1/L2/L3) to include per stack in `coverage_policy_per_stack`. Default: C1+C2, L1+L2.
- If a track abstract specifies coverage scope, prefer its tags/levels unless overridden by product context.
- Keep this brief compact and structural.

Return ONLY the JSON object."""

    response = claude.generate(
        prompt=prompt,
        system="You are a curriculum architect preparing a Stage 0 brief artifact before curriculum structuring.",
        model_tier="strong",
        max_tokens=6000,
    )

    audience_candidates = _extract_markdown_bullets(learner_context, limit=2)
    brief_generation_status = "parsed"
    brief_generation_note = None
    brief_generation_raw_response = None
    try:
        brief = _parse_json_object_response(response)
    except (json.JSONDecodeError, ValueError):
        brief_generation_status = "fallback_non_json"
        brief_generation_note = (
            "Brief generation response could not be parsed as JSON. "
            "Using a deterministic fallback brief."
        )
        brief_generation_raw_response = response[:4000]
        brief = {
            "brief_id": f"brief_{_slugify(domain)}",
            "stack_name": default_stack_name,
            "packaging_profile_ref": packaging_profile.get("packaging_profile_id"),
            "product_context": {
                "product_label": product_context.get("product_label", "Stack-only default"),
                "delivery_mode": product_context.get("delivery_mode", "unspecified"),
                "curriculum_container_kind": product_context.get("curriculum_container_kind", "standard_curriculum"),
            },
            "audience": {
                "primary": audience_candidates[:2],
                "english_level": 8,
            },
            "pedagogy": {
                "default_profile": pedagogy_profile,
                "allowed_local_overrides": _default_allowed_local_overrides(pedagogy_profile),
            },
            "stack_learning_outcomes": _fallback_stack_learning_outcomes(domain, pedagogy_profile, curriculum_source_context),
            "source_refs": source_refs,
            "source_hours_declared": source_hours_declared,
            "source_vs_packaging_conflict": source_vs_packaging_conflict,
            "coverage_policy_per_stack": _default_coverage_policy(domain, track_abstract),
        }

    brief.setdefault("brief_id", f"brief_{_slugify(domain)}")
    brief.setdefault("stack_name", default_stack_name)
    brief.setdefault("packaging_profile_ref", packaging_profile.get("packaging_profile_id"))
    brief.setdefault(
        "product_context",
        {
            "product_label": product_context.get("product_label", "Stack-only default"),
            "delivery_mode": product_context.get("delivery_mode", "unspecified"),
            "curriculum_container_kind": product_context.get("curriculum_container_kind", "standard_curriculum"),
        },
    )
    brief.setdefault(
        "audience",
        {"primary": audience_candidates[:2], "english_level": 8},
    )
    brief.setdefault(
        "pedagogy",
        {
            "default_profile": pedagogy_profile,
            "allowed_local_overrides": _default_allowed_local_overrides(pedagogy_profile),
        },
    )
    brief.setdefault(
        "stack_learning_outcomes",
        _fallback_stack_learning_outcomes(domain, pedagogy_profile, curriculum_source_context),
    )
    brief.setdefault("source_refs", source_refs)
    brief.setdefault("source_hours_declared", source_hours_declared)
    brief.setdefault("source_vs_packaging_conflict", source_vs_packaging_conflict)
    brief.setdefault("coverage_policy_per_stack", _default_coverage_policy(domain, track_abstract))
    brief["pedagogy"].setdefault("default_profile", pedagogy_profile)
    brief["pedagogy"].setdefault("allowed_local_overrides", _default_allowed_local_overrides(pedagogy_profile))

    if brief_generation_status == "fallback_non_json":
        print("  Brief generation parse failed; using deterministic fallback brief.")
    else:
        print(
            "  Brief: "
            f"{brief.get('stack_name', domain)} "
            f"({len(brief.get('stack_learning_outcomes', []))} stack learning outcomes)"
        )

    artifact_path, artifact_paths = _persist_design_artifact(
        state=state,
        artifact_key="brief",
        filename="brief.yaml",
        payload=brief,
    )

    return {
        "brief_generation_status": brief_generation_status,
        "brief_generation_note": brief_generation_note,
        "brief_generation_raw_response": brief_generation_raw_response,
        "brief": brief,
        "brief_artifact_path": artifact_path,
        "design_artifact_paths": artifact_paths,
        "coverage_policy": brief.get("coverage_policy_per_stack"),
    }


def resolve_pedagogy_profile(state: dict) -> dict:
    """Resolve and justify a pedagogy profile from config."""
    domain = state.get("domain", "ml-engineering")
    content_type = state.get("content_type", "concept_explainer")
    product_context = state.get("product_context", {}) or {}
    if state.get("product_family") and not product_context.get("pedagogy_layers"):
        product_context = resolve_product_manifest_context(
            domain=domain,
            product_family=state.get("product_family"),
            product_version=state.get("product_version"),
        )

    resolver = PedagogyResolver()
    resolution = resolver.resolve_domain_profile(
        domain=domain,
        content_type=content_type,
        product_context=product_context,
    )

    print(
        "  Pedagogy profile: "
        f"{resolution['profile']} "
        f"(source: {resolution.get('source', resolution.get('reason', 'unknown'))})"
    )
    return {
        "product_context": product_context,
        "pedagogy_profile": resolution["profile"],
        "pedagogy_rationale": resolution.get("rationale", resolution["reason"]),
        "pedagogy_source": resolution.get("source", resolution["reason"]),
        "pedagogy_resolution_layers": resolution.get("resolution_layers", []),
    }


def compose_product_specific_curriculum_container(state: dict) -> dict:
    """Compose the product-specific curriculum container from brief, stack abstract, and overlays."""
    from open_acp.loops.loop_b.coverage import apply_coverage_policy, verify_cross_stack_prerequisites

    domain = state.get("domain", "ml-engineering")
    brief = _load_design_artifact(state, artifact_key="brief", state_key="brief", filename="brief.yaml")
    if not brief:
        raise ValueError(
            "Missing brief artifact. Run generate_brief successfully before compose_product_specific_curriculum_container."
        )
    curriculum_source_context = state.get("curriculum_source_context") or state.get("program_context", "")
    content_type = state.get("content_type", "concept_explainer")
    structure_profile = state.get("structure_profile", {}) or {}
    packaging_profile = state.get("packaging_profile", {}) or {}
    time_budget_context = state.get("time_budget_context", {}) or {}
    skill_outcomes_context = state.get("skill_outcomes_context", "")
    market_and_community_context = state.get("market_and_community_context", "")
    structure_summary = _structure_summary(structure_profile)
    packaging_summary = _packaging_summary(packaging_profile)
    stack_course_abstract_summary = _stack_course_abstract_summary(domain)
    product_course_overlay_summary = _product_course_overlay_summary(state.get("product_context", {}) or {})
    brief_json = json.dumps(brief, indent=2)
    pedagogy_profile = ((brief.get("pedagogy") or {}).get("default_profile")) or state.get("pedagogy_profile", "concept_progression")
    total_hours = time_budget_context.get("target_total_hours", packaging_profile.get("total_hours", 20.0))
    stack_name = brief.get("stack_name", _default_stack_name(domain, curriculum_source_context))
    packaging_profile_ref = brief.get("packaging_profile_ref", packaging_profile.get("packaging_profile_id"))

    # v9: Apply coverage policy to stack abstracts when available
    stack_abstracts = state.get("stack_abstracts", {}) or {}
    coverage_policy = state.get("coverage_policy") or brief.get("coverage_policy_per_stack", {}) or {}
    all_selected_modules: list[dict] = []
    composition_trace_data: dict = {
        "contributing_stacks": [],
        "modules_selected_per_stack": {},
        "modules_dropped": [],
        "coverage_cells_selected_per_stack": {},
        "refreshers_added": [],
        "addons_injected": [],
        "cross_stack_prereq_verification": {},
        "abstract_versions_pinned": {},
    }
    coverage_context_lines: list[str] = []

    if stack_abstracts:
        for stack_id, abstract in stack_abstracts.items():
            policy = coverage_policy.get(stack_id, {})
            include_tags = policy.get("include_tags")
            include_levels = policy.get("include_levels")

            result = apply_coverage_policy(abstract, include_tags, include_levels)
            selected = result["selected"]
            dropped = result["dropped"]
            selected_cells = result["selected_cells"]

            all_selected_modules.extend(selected)
            composition_trace_data["contributing_stacks"].append(stack_id)
            composition_trace_data["modules_selected_per_stack"][stack_id] = [
                m.get("module_id", "?") for m in selected
            ]
            composition_trace_data["modules_dropped"].extend(dropped)
            composition_trace_data["coverage_cells_selected_per_stack"][stack_id] = selected_cells
            composition_trace_data["abstract_versions_pinned"][stack_id] = abstract.get("version", 1)

            coverage_context_lines.append(
                f"\n### {stack_id}: {len(selected)} modules selected, {len(dropped)} dropped"
            )
            for mod in selected[:10]:
                tags = mod.get("tags", [])
                coverage_context_lines.append(
                    f"- {mod.get('module_id', '?')}: {mod.get('title', '?')} [{', '.join(tags)}]"
                )
            if len(selected) > 10:
                coverage_context_lines.append(f"  ... and {len(selected) - 10} more")

        # Verify cross-stack prerequisites
        prereq_report = verify_cross_stack_prerequisites(all_selected_modules, stack_abstracts)
        composition_trace_data["cross_stack_prereq_verification"] = {
            "verified": prereq_report["verified"],
            "checks": prereq_report["checks"][:20],
        }

    coverage_context = "\n".join(coverage_context_lines) if coverage_context_lines else ""

    claude = ClaudeClient()
    prompt = f"""Design a curriculum structure for "{domain}" using the approved brief artifact.

## Brief Artifact
{brief_json}

## Curriculum Source Context
{curriculum_source_context or "No explicit curriculum source provided."}

## Structure Profile
{structure_summary}

## Packaging Context
{packaging_summary}

## Canonical Stack Course Abstract
{stack_course_abstract_summary}

## Product Course Overlay
{product_course_overlay_summary}

## Coverage-Policy Selected Modules (from Stack Curriculum Abstracts)
{coverage_context or "No stack curriculum abstracts available — design courses from scratch."}

## Skill Outcomes Digest
{skill_outcomes_context or "No explicit skill-outcomes digest provided."}

## Market And Community Digest
{market_and_community_context or "No explicit market/community digest provided."}

Use backward design and keep this stage structural:
1. Start with terminal outcomes (what can learners DO after?)
2. Select which packaged courses belong in this curriculum based on:
   - time budget
   - priority skill requirements
   - product-linked skill-assessment expectations
   - canonical stack course titles and any declared canonical course variants
   - product-only course additions and any declared product course-variant overrides
3. Map prerequisites between packaged courses.
4. Estimate duration per course.
5. Use source-defined levels, phases, or tracks only as ordering cues or title hints; do not emit explicit level output at this stage.
6. Use the packaging profile to decide how coarse or fine the packaged course boundaries should be.
7. If breadth/depth packaging scope is known, reflect it in course scope or course title rather than inventing a separate level object.
8. Do not decide topic allocation here. Topic-to-course assignment belongs to later design stages and should eventually be informed by channel-analysis inputs.
9. If a course must be designed differently for a different audience or product, prefer a declared `course_variant_id` over silently reusing the base course.
10. Product-only additions such as induction should be emitted as `course_kind: "product_only_course"` when canonically declared.
11. Keep this stage structural and compact rather than fully expanded.
12. If coverage-policy selected modules are available, group them into courses. Each course's modules trace back via `source_modules` entries with `stack`, `abstract_ref` (module_id), and `tags`.

Return JSON:
{{
  "curriculum_id": "cur_{domain}",
  "brief_ref": "{brief.get('brief_id', f'brief_{domain}')}",
  "packaging_profile_ref": "{packaging_profile_ref}",
  "stack_name": "{stack_name}",
  "domain": "{domain}",
  "courses": [
    {{
      "course_id": "c1",
      "title": "Course Title",
      "sequence": 1,
      "pedagogy_profile": "{pedagogy_profile}",
      "objectives": [
        {{"id": "obj_1", "statement": "...", "bloom_level": "understand", "skill_ids": ["skill_id"]}}
      ],
      "estimated_hours": 1.5,
      "prerequisite_courses": [],
      "content_types": ["{content_type}"],
      "skill_ids": ["skill_id"],
      "canonical_course_id": "canonical_course_id",
      "course_variant_id": null,
      "course_kind": "stack_course",
      "course_variant_reason": null,
      "source_modules": [{{"stack": "{domain}", "abstract_ref": "module_id", "tags": ["C1", "L1"]}}]
    }}
  ],
  "capstone_project": {{}},
  "grand_quiz": {{}},
  "total_hours": {total_hours},
  "hours_check": {{
    "courses_sum": {total_hours},
    "capstone": 0.0,
    "grand_quiz": 0.0
  }}
}}

Important constraints:
- Respect the resolved target total hours unless the source curriculum clearly forces a human-reviewed conflict.
- `total_hours` is the full Stage 1 budget for packaged courses + capstone_project + grand_quiz combined.
- `hours_check.courses_sum + hours_check.capstone + hours_check.grand_quiz` must equal `total_hours`.
- If capstone_project or grand_quiz are not explicitly required by the product/source, return them as empty objects and keep their hours at 0.
- If capstone_project or grand_quiz are present, their estimated hours must fit inside the same `total_hours`; reduce packaged course hours accordingly.
- Preserve source-defined progression when it exists, but encode it through course sequence and course scope rather than explicit level output.
- Represent each major phase or specialization as its own packaged course only when time budget and product requirements justify it.
- Do not collapse a detailed long-form curriculum into 4-6 generic courses unless the source clearly justifies it.
- Limit to 2-3 concise objectives per course.
- Keep each objective statement under 18 words.
- Use stable snake_case wiki skill IDs when referencing skills, not display titles.
- Prefer 4-8 packaged courses total for this stage unless the source clearly requires more.
- `course_kind` must be either `stack_course` or `product_only_course`.
- Use `canonical_course_id` whenever the course maps to a known canonical stack course.
- Use `course_variant_id` only when a declared canonical course variant or product override applies.

Return ONLY the JSON object."""

    response = claude.generate(
        prompt=prompt,
        system="You are a curriculum architect using backward design.",
        model_tier="strong",
        max_tokens=12000,
    )

    curriculum_generation_status = "parsed"
    curriculum_generation_note = None
    curriculum_generation_raw_response = None
    try:
        data = _parse_json_object_response(response)
    except (json.JSONDecodeError, ValueError):
        curriculum_generation_status = "fallback_non_json"
        if _looks_like_truncated_json(response):
            curriculum_generation_note = (
                "Curriculum container composition response could not be parsed as JSON and appears to have been cut off mid-output. "
                "Using an empty fallback curriculum draft."
            )
        else:
            curriculum_generation_note = (
                "Curriculum container composition response could not be parsed as JSON. "
                "Using an empty fallback curriculum draft."
            )
        curriculum_generation_raw_response = response[:4000]
        data = {
            "curriculum_id": f"cur_{domain}",
            "brief_ref": brief.get("brief_id", f"brief_{domain}"),
            "packaging_profile_ref": packaging_profile_ref,
            "stack_name": stack_name,
            "domain": domain,
            "courses": [],
            "capstone_project": {},
            "grand_quiz": {},
            "total_hours": total_hours,
            "hours_check": {"courses_sum": 0, "capstone": 0, "grand_quiz": 0},
        }

    data = _normalize_curriculum_payload(data)
    courses = data.get("courses", [])
    validation_report = _validate_curriculum_hours(
        curriculum=data,
        packaging_profile=packaging_profile,
        time_budget_context=time_budget_context,
    )
    if curriculum_generation_status != "fallback_non_json" and not validation_report["within_tolerance"]:
        repair_prompt = f"""Repair this Stage 1 product-specific curriculum container JSON so its hours accounting is valid.

## Brief Artifact
{brief_json}

## Packaging Context
{packaging_summary}

## Time Budget Context
{_build_time_budget_summary(time_budget_context)}

## Current Curriculum JSON
{json.dumps(data, indent=2)}

## Validation Issues
{json.dumps(validation_report.get("issues", []), indent=2)}

Return a corrected JSON object only.

Hard requirements:
- Keep the same curriculum_id, brief_ref, packaging_profile_ref, stack_name, and domain.
- Preserve course intent and sequence where possible.
- `total_hours` is the full budget for courses + capstone_project + grand_quiz combined.
- `hours_check.courses_sum + hours_check.capstone + hours_check.grand_quiz` must equal `total_hours`.
- If capstone_project or grand_quiz are not required, return them as empty objects and keep their hours at 0.
- Keep packaged course count within the same rough scale unless a small reduction is needed to satisfy the budget.
- Return ONLY the corrected JSON object."""
        repair_response = claude.generate(
            prompt=repair_prompt,
            system="You are repairing a Stage 1 curriculum-container artifact to satisfy strict time-budget validation.",
            model_tier="strong",
            max_tokens=8000,
        )
        try:
            repaired = _normalize_curriculum_payload(_parse_json_object_response(repair_response))
            repair_validation_report = _validate_curriculum_hours(
                curriculum=repaired,
                packaging_profile=packaging_profile,
                time_budget_context=time_budget_context,
            )
            if repair_validation_report["within_tolerance"]:
                data = repaired
                validation_report = repair_validation_report
                curriculum_generation_status = "validated_after_repair"
                curriculum_generation_note = (
                    "Initial curriculum draft failed hours validation; a single structured repair pass produced a valid artifact."
                )
                curriculum_generation_raw_response = repair_response[:4000]
            else:
                raise ValueError(
                    "Curriculum hours validation failed: " + " ".join(repair_validation_report["issues"])
                )
        except (json.JSONDecodeError, ValueError) as exc:
            raise ValueError(
                "Curriculum hours validation failed: " + " ".join(validation_report["issues"])
            ) from exc

    courses = data.get("courses", [])
    data["hours_check"] = {
        "courses_sum": validation_report["course_hours_sum"],
        "capstone": float((data.get("capstone_project") or {}).get("estimated_hours", 0) or 0),
        "grand_quiz": float((data.get("grand_quiz") or {}).get("estimated_hours", 0) or 0),
    }
    # v9: Attach composition_trace when abstracts were used
    if stack_abstracts and composition_trace_data.get("contributing_stacks"):
        data["composition_trace"] = composition_trace_data
        data.setdefault("composition_mode", "multi_stack" if len(stack_abstracts) > 1 else "single_stack")

    if curriculum_generation_status == "fallback_non_json":
        print("  Curriculum generation parse failed; using empty fallback curriculum draft.")
    elif curriculum_generation_status == "validated_after_repair":
        print("  Curriculum validated after one repair pass.")
    else:
        trace_msg = ""
        if data.get("composition_trace"):
            trace = data["composition_trace"]
            total_selected = sum(len(v) for v in trace.get("modules_selected_per_stack", {}).values())
            total_dropped = len(trace.get("modules_dropped", []))
            trace_msg = f" (from abstracts: {total_selected} selected, {total_dropped} dropped)"
        print(f"  Curriculum: {len(courses)} courses, {data.get('total_hours', 0)} hours{trace_msg}")

    artifact_path, artifact_paths = _persist_design_artifact(
        state=state,
        artifact_key="curriculum",
        filename="curriculum.yaml",
        payload=data,
    )

    # v9: Persist abstract version registry when abstracts were consumed
    if composition_trace_data.get("abstract_versions_pinned"):
        version_registry = {
            "curriculum_id": data.get("curriculum_id"),
            "cycle_id": state.get("cycle_id", "cycle_1"),
            "abstract_versions": composition_trace_data["abstract_versions_pinned"],
            "domain_definition_version": (state.get("domain_definition") or {}).get("version"),
            "track_abstract_version": (state.get("track_abstract") or {}).get("version"),
        }
        _, artifact_paths = _persist_design_artifact(
            state=state,
            artifact_key="abstract_versions",
            filename="abstract_versions.yaml",
            payload=version_registry,
        )

    return {
        "curriculum_generation_status": curriculum_generation_status,
        "curriculum_generation_note": curriculum_generation_note,
        "curriculum_generation_raw_response": curriculum_generation_raw_response,
        "previous_curriculum_map": state.get("curriculum_map"),
        "curriculum_map": data,
        "curriculum_validation_report": validation_report,
        "curriculum_artifact_path": artifact_path,
        "design_artifact_paths": artifact_paths,
    }


def compare_curriculum_changes(state: dict) -> dict:
    """Compare the current curriculum draft to the previous saved version, if any."""
    current = _load_design_artifact(state, artifact_key="curriculum", state_key="curriculum_map", filename="curriculum.yaml")
    previous = state.get("previous_curriculum_map", {}) or {}

    current_courses = current.get("courses", []) or []
    previous_courses = previous.get("courses", []) or []

    current_by_id = {
        course.get("course_id", f"course_{index + 1}"): course
        for index, course in enumerate(current_courses)
    }
    previous_by_id = {
        course.get("course_id", f"course_{index + 1}"): course
        for index, course in enumerate(previous_courses)
    }

    added_courses = [
        course.get("title", course_id)
        for course_id, course in current_by_id.items()
        if course_id not in previous_by_id
    ]
    removed_courses = [
        course.get("title", course_id)
        for course_id, course in previous_by_id.items()
        if course_id not in current_by_id
    ]
    renamed_courses = []
    for course_id, course in current_by_id.items():
        if course_id in previous_by_id:
            previous_title = previous_by_id[course_id].get("title", course_id)
            current_title = course.get("title", course_id)
            if previous_title != current_title:
                renamed_courses.append({"course_id": course_id, "from": previous_title, "to": current_title})

    report = {
        "status": "baseline" if not previous_courses else "changed",
        "previous_course_count": len(previous_courses),
        "current_course_count": len(current_courses),
        "added_courses": added_courses,
        "removed_courses": removed_courses,
        "renamed_courses": renamed_courses,
        "hours_change": round(float(current.get("total_hours", 0) or 0) - float(previous.get("total_hours", 0) or 0), 2),
        "current_titles": [course.get("title", "Untitled") for course in current_courses],
    }

    status = "baseline snapshot" if report["status"] == "baseline" else "change report"
    print(f"  Curriculum changes: {status}, {len(added_courses)} added, {len(removed_courses)} removed")
    return {"curriculum_change_report": report}


def resolve_packaging_profile(state: dict) -> dict:
    """Resolve packaging defaults that shape courses, modules, topics, and learning units."""
    domain = state.get("domain", "ml-engineering")
    product_context = state.get("product_context", {}) or {}
    if state.get("product_family") and not product_context.get("packaging_layers"):
        product_context = resolve_product_manifest_context(
            domain=domain,
            product_family=state.get("product_family"),
            product_version=state.get("product_version"),
        )
    profile = resolve_packaging_manifest_profile(
        domain=domain,
        content_type=state.get("content_type", "concept_explainer"),
        product_context=product_context,
    )

    print(
        "  Packaging profile: "
        f"{profile.get('packaging_profile_id', 'default')} "
        f"({len(profile.get('allowed_learning_unit_types', []))} unit types)"
    )
    return {"product_context": product_context, "packaging_profile": profile}


def design_courses(state: dict) -> dict:
    """Treat the current curriculum draft courses as explicit course seeds for downstream design."""
    curriculum = _load_design_artifact(state, artifact_key="curriculum", state_key="curriculum_map", filename="curriculum.yaml")
    course_seeds = curriculum.get("courses", []) or []

    courses = []
    for index, seed in enumerate(course_seeds, start=1):
        course_id = seed.get("course_id") or f"course_{_slugify(seed.get('title', f'course_{index}'))}"
        courses.append(
            {
                "course_id": course_id,
                "source_course_id": seed.get("course_id", course_id),
                "title": seed.get("title", f"Course {index}"),
                "sequence": seed.get("sequence", index),
                "estimated_hours": seed.get("estimated_hours", 0),
                "content_types": seed.get("content_types", []),
                "objective_ids": [
                    objective.get("id") or objective.get("objective_id", f"obj_{obj_index + 1}")
                    for obj_index, objective in enumerate(seed.get("objectives", []))
                ],
                "outcomes": _course_objective_statements(seed),
                "skill_ids": seed.get("skill_ids", []) or _course_skill_ids(seed),
                "canonical_course_id": seed.get("canonical_course_id"),
                "course_variant_id": seed.get("course_variant_id"),
                "course_kind": seed.get("course_kind", "stack_course"),
                "course_variant_reason": seed.get("course_variant_reason"),
                "source_modules": seed.get("source_modules", []),
                "domain_rollup": seed.get("domain_rollup", []),
                "origin": seed.get("origin"),
            }
        )

    course_design = {
        "curriculum_id": curriculum.get("curriculum_id", "unknown_curriculum"),
        "course_count": len(courses),
        "courses": courses,
    }
    print(f"  Course design: {len(courses)} course seeds prepared")
    artifact_path, artifact_paths = _persist_design_collection_artifacts(
        state=state,
        artifact_key="course_design",
        subdir="courses",
        item_prefix="course",
        item_key="courses",
        item_id_key="course_id",
        payload=course_design,
    )
    return {"course_design": course_design, "design_artifact_paths": artifact_paths, "course_design_artifact_path": artifact_path}


def _build_abstract_module_index(state: dict) -> dict[str, dict]:
    """Build a lookup from abstract module_id to its full dict across all stack abstracts."""
    index: dict[str, dict] = {}
    for abstract in (state.get("stack_abstracts") or {}).values():
        for mod in abstract.get("modules", []) or []:
            mid = mod.get("module_id")
            if mid:
                index[mid] = mod
    return index


def design_modules(state: dict) -> dict:
    """Expand each course into packaging-shaped modules, inheriting C/L tags from abstract modules."""
    course_design = _load_design_artifact(state, artifact_key="course_design", state_key="course_design", filename="courses/index.yaml")
    courses = (course_design or {}).get("courses", [])
    packaging_profile = state.get("packaging_profile", {}) or {}
    phase_labels = _module_phase_labels(packaging_profile)
    module_rule = packaging_profile.get("module_count_per_course", {})

    # Build abstract module index for C/L tag inheritance
    abstract_index = _build_abstract_module_index(state)

    modules = []
    for course in courses:
        source_modules = course.get("source_modules", []) or []

        if source_modules and abstract_index:
            # v9 path: one design module per source abstract module
            for index, sm in enumerate(source_modules):
                abstract_ref = sm.get("abstract_ref", "")
                abstract_mod = abstract_index.get(abstract_ref, {})
                tags = sm.get("tags", []) or abstract_mod.get("tags", [])
                hours_range = abstract_mod.get("estimated_hours_range", {})
                est_hours = (float(hours_range.get("min", 0)) + float(hours_range.get("max", 0))) / 2 if hours_range else 0
                if not est_hours:
                    est_hours = round(float(course.get("estimated_hours", 0) or 0) / max(len(source_modules), 1), 2)

                modules.append(
                    {
                        "module_id": f"{course['course_id']}_m{index + 1}",
                        "course_id": course["course_id"],
                        "title": abstract_mod.get("title", f"{course['title']} — Module {index + 1}"),
                        "sequence_within_course": index + 1,
                        "estimated_hours": round(est_hours, 2),
                        "skill_ids": abstract_mod.get("skill_ids", course.get("skill_ids", [])),
                        "focus_outcomes": course.get("outcomes", [course["title"]])[:2],
                        "module_quiz_required": packaging_profile.get("module_quiz_required", True),
                        "tags": tags,
                        "concepts": abstract_mod.get("concepts", []),
                        "interview_frequency": abstract_mod.get("interview_frequency"),
                        "abstract_ref": abstract_ref,
                        "pedagogy_profile": abstract_mod.get("default_pedagogy_profile"),
                    }
                )
        else:
            # Legacy path: generate modules from packaging rules
            module_count = _resolve_configured_count(float(course.get("estimated_hours", 0) or 0), module_rule)
            hours_per_module = round(float(course.get("estimated_hours", 0) or 0) / module_count, 2) if module_count else 0

            for index in range(module_count):
                phase_label = phase_labels[index % len(phase_labels)]
                modules.append(
                    {
                        "module_id": f"{course['course_id']}_m{index + 1}",
                        "course_id": course["course_id"],
                        "title": f"{course['title']} — {phase_label}",
                        "sequence_within_course": index + 1,
                        "estimated_hours": hours_per_module,
                        "skill_ids": course.get("skill_ids", []),
                        "focus_outcomes": course.get("outcomes", [course["title"]])[:2],
                        "module_quiz_required": packaging_profile.get("module_quiz_required", True),
                        "tags": [],
                        "concepts": [],
                        "interview_frequency": None,
                        "abstract_ref": None,
                        "pedagogy_profile": None,
                    }
                )

    module_design = {
        "total_module_count": len(modules),
        "modules": modules,
    }
    print(f"  Module design: {len(modules)} modules across {len(courses)} courses")
    artifact_path, artifact_paths = _persist_design_collection_artifacts(
        state=state,
        artifact_key="module_design",
        subdir="modules",
        item_prefix="module",
        item_key="modules",
        item_id_key="module_id",
        payload=module_design,
    )
    return {"module_design": module_design, "design_artifact_paths": artifact_paths, "module_design_artifact_path": artifact_path}


def design_topics(state: dict) -> dict:
    """Design topics inside each module using packaging defaults."""
    module_design = _load_design_artifact(state, artifact_key="module_design", state_key="module_design", filename="modules/index.yaml")
    modules = (module_design or {}).get("modules", [])
    packaging_profile = state.get("packaging_profile", {}) or {}
    pedagogy_profile = state.get("pedagogy_profile", "concept_progression")
    topic_rule = packaging_profile.get("topic_count_per_module", {})
    phase_labels = _topic_phase_labels(packaging_profile, pedagogy_profile)

    topics = []
    for module in modules:
        concepts = module.get("concepts", []) or []
        topic_count = _resolve_configured_count(float(module.get("estimated_hours", 0) or 0), topic_rule)
        minutes_per_topic = round((float(module.get("estimated_hours", 0) or 0) * 60) / topic_count, 1) if topic_count else 0

        for index in range(topic_count):
            phase_label = phase_labels[index % len(phase_labels)]
            # Use abstract concepts for topic titles when available
            if concepts and index < len(concepts):
                concept_title = concepts[index].replace("_", " ").title()
                topic_title = f"{module['title']} — {concept_title}"
            else:
                topic_title = f"{module['title']} — {phase_label}"

            topics.append(
                {
                    "topic_id": f"{module['module_id']}_t{index + 1}",
                    "module_id": module["module_id"],
                    "course_id": module["course_id"],
                    "title": topic_title,
                    "sequence_within_module": index + 1,
                    "estimated_minutes": minutes_per_topic,
                    "skill_ids": module.get("skill_ids", []),
                    "focus_outcomes": module.get("focus_outcomes", []),
                    "tags": module.get("tags", []),
                    "concept": concepts[index] if index < len(concepts) else None,
                }
            )

    topic_design = {
        "total_topic_count": len(topics),
        "topics": topics,
    }
    print(f"  Topic design: {len(topics)} topics prepared")
    artifact_path, artifact_paths = _persist_design_collection_artifacts(
        state=state,
        artifact_key="topic_design",
        subdir="topics",
        item_prefix="topic",
        item_key="topics",
        item_id_key="topic_id",
        payload=topic_design,
    )
    return {"topic_design": topic_design, "design_artifact_paths": artifact_paths, "topic_design_artifact_path": artifact_path}


def design_learning_units(state: dict) -> dict:
    """Assign learning unit types to each topic based on packaging and pedagogy."""
    topic_design = _load_design_artifact(state, artifact_key="topic_design", state_key="topic_design", filename="topics/index.yaml")
    topics = (topic_design or {}).get("topics", [])
    packaging_profile = state.get("packaging_profile", {}) or {}
    pedagogy_profile = state.get("pedagogy_profile", "concept_progression")
    preferred_mix = packaging_profile.get("preferred_learning_unit_mix", [])
    allowed_types = set(packaging_profile.get("allowed_learning_unit_types", []))
    units_per_topic = int(packaging_profile.get("learning_units_per_topic", 3))

    units = []
    for topic in topics:
        unit_types = preferred_mix[:units_per_topic] or list(allowed_types)[:units_per_topic]
        unit_types = list(unit_types)

        if pedagogy_profile == "project_build_along" and "coding_practice_unit" in allowed_types and topic["sequence_within_module"] >= 2:
            if "coding_practice_unit" not in unit_types:
                unit_types[-1] = "coding_practice_unit"

        if topic["sequence_within_module"] == 1 and "reading_material_unit" in allowed_types and "reading_material_unit" not in unit_types:
            unit_types[0] = "reading_material_unit"

        minutes_per_unit = round(float(topic.get("estimated_minutes", 0) or 0) / max(len(unit_types), 1), 1)
        for index, unit_type in enumerate(unit_types, start=1):
            units.append(
                {
                    "learning_unit_id": f"{topic['topic_id']}_u{index}",
                    "topic_id": topic["topic_id"],
                    "module_id": topic["module_id"],
                    "course_id": topic["course_id"],
                    "unit_type": unit_type,
                    "title": f"{topic['title']} — {_learning_unit_label(unit_type)}",
                    "estimated_minutes": minutes_per_unit,
                    "delivery_intent": "build" if unit_type == "coding_practice_unit" else "learn",
                }
            )

    learning_unit_plan = {
        "total_learning_unit_count": len(units),
        "unit_types_present": _unique_preserve_order([unit["unit_type"] for unit in units]),
        "learning_units": units,
    }
    print(f"  Learning units: {len(units)} units across {len(topics)} topics")
    artifact_path, artifact_paths = _persist_design_collection_artifacts(
        state=state,
        artifact_key="learning_unit_plan",
        subdir="units",
        item_prefix="unit",
        item_key="learning_units",
        item_id_key="learning_unit_id",
        payload=learning_unit_plan,
    )
    return {
        "learning_unit_plan": learning_unit_plan,
        "design_artifact_paths": artifact_paths,
        "learning_unit_plan_artifact_path": artifact_path,
    }


def design_practice(state: dict) -> dict:
    """Design practice touchpoints from the planned learning-unit mix."""
    topic_design = _load_design_artifact(
        state,
        artifact_key="topic_design",
        state_key="topic_design",
        filename="topics/index.yaml",
    ) or {}
    learning_unit_plan = _load_design_artifact(
        state,
        artifact_key="learning_unit_plan",
        state_key="learning_unit_plan",
        filename="units/index.yaml",
    ) or {}
    topics = topic_design.get("topics", [])
    learning_units = learning_unit_plan.get("learning_units", [])

    practice_items = []
    for topic in topics:
        topic_units = [unit for unit in learning_units if unit.get("topic_id") == topic["topic_id"]]
        if any(unit.get("unit_type") == "coding_practice_unit" for unit in topic_units):
            practice_type = "coding_practice"
        elif any(unit.get("unit_type") == "mcq_practice_unit" for unit in topic_units):
            practice_type = "mcq_retrieval"
        else:
            practice_type = "guided_reflection"

        # v9: C1 topics get 30% practice time, C2/C3 get 20%
        tags = topic.get("tags", []) or []
        practice_ratio = 0.30 if "C1" in tags else 0.20 if tags else 0.25
        practice_items.append(
            {
                "topic_id": topic["topic_id"],
                "module_id": topic["module_id"],
                "practice_type": practice_type,
                "estimated_minutes": max(10, round(float(topic.get("estimated_minutes", 0) or 0) * practice_ratio)),
                "goal": f"Reinforce {topic['title']}",
                "tags": tags,
                "interview_frequency": topic.get("interview_frequency"),
            }
        )

    practice_design = {
        "practice_touchpoint_count": len(practice_items),
        "practice_types": _unique_preserve_order([item["practice_type"] for item in practice_items]),
        "items": practice_items,
    }
    artifact_path, artifact_paths = _persist_design_artifact(
        state=state,
        artifact_key="practice_design",
        filename="practice.yaml",
        payload=practice_design,
    )
    print(f"  Practice design: {len(practice_items)} touchpoints")
    return {
        "practice_design": practice_design,
        "design_artifact_paths": artifact_paths,
        "practice_design_artifact_path": artifact_path,
    }


def design_learning_assessments(state: dict) -> dict:
    """Design internal learning assessments before external skill-assessment alignment."""
    module_design = _load_design_artifact(
        state,
        artifact_key="module_design",
        state_key="module_design",
        filename="modules/index.yaml",
    ) or {}
    topic_design = _load_design_artifact(
        state,
        artifact_key="topic_design",
        state_key="topic_design",
        filename="topics/index.yaml",
    ) or {}
    learning_unit_plan = _load_design_artifact(
        state,
        artifact_key="learning_unit_plan",
        state_key="learning_unit_plan",
        filename="units/index.yaml",
    ) or {}
    modules = module_design.get("modules", [])
    topics = topic_design.get("topics", [])
    learning_units = learning_unit_plan.get("learning_units", [])
    packaging_profile = state.get("packaging_profile", {}) or {}

    classroom_quizzes = []
    module_quizzes = []

    for topic in topics:
        topic_units = [unit for unit in learning_units if unit.get("topic_id") == topic["topic_id"]]
        classroom_quizzes.append(
            {
                "assessment_id": f"{topic['topic_id']}_classroom_quiz",
                "topic_id": topic["topic_id"],
                "module_id": topic["module_id"],
                "cadence_minutes": packaging_profile.get("classroom_quiz_every_minutes", 20),
                "question_types": _assessment_question_types_for_topic(topic, topic_units),
                "difficulty": _assessment_difficulty(
                    topic["sequence_within_module"],
                    max(1, len([candidate for candidate in topics if candidate.get("module_id") == topic["module_id"]])),
                    tags=topic.get("tags"),
                ),
                "concept_tags": topic.get("skill_ids", []),
                "tags": topic.get("tags", []),
            }
        )

    for module in modules:
        module_topics = [topic for topic in topics if topic.get("module_id") == module["module_id"]]
        module_question_types = _unique_preserve_order(
            question_type
            for topic in module_topics
            for question_type in _assessment_question_types_for_topic(
                topic,
                [unit for unit in learning_units if unit.get("topic_id") == topic["topic_id"]],
            )
        )
        if "coding_practice_unit" in {unit.get("unit_type") for unit in learning_units if unit.get("module_id") == module["module_id"]}:
            module_question_types = _unique_preserve_order(module_question_types + ["coding"])

        module_quizzes.append(
            {
                "assessment_id": f"{module['module_id']}_module_quiz",
                "module_id": module["module_id"],
                "question_types": module_question_types,
                "difficulty": "medium" if module["sequence_within_course"] == 1 else "hard",
                "concept_tags": module.get("skill_ids", []),
                "required": module.get("module_quiz_required", True),
            }
        )

    learning_assessment_plan = {
        "classroom_quizzes": classroom_quizzes,
        "module_quizzes": module_quizzes,
        "question_types_covered": _unique_preserve_order(
            question_type
            for assessment in classroom_quizzes + module_quizzes
            for question_type in assessment.get("question_types", [])
        ),
        "difficulty_levels_covered": _unique_preserve_order(
            assessment.get("difficulty", "")
            for assessment in classroom_quizzes + module_quizzes
            if assessment.get("difficulty")
        ),
        "assessment_schedule": {
            "classroom_quizzes": f"Every {packaging_profile.get('classroom_quiz_every_minutes', 20)} minutes within topics",
            "module_quizzes": "At the end of each module",
        },
    }
    artifact_path, artifact_paths = _persist_design_artifact(
        state=state,
        artifact_key="learning_assessment_plan",
        filename="learning_assessments.yaml",
        payload=learning_assessment_plan,
    )

    print(
        "  Learning assessments: "
        f"{len(classroom_quizzes)} classroom quizzes, {len(module_quizzes)} module quizzes"
    )
    return {
        "learning_assessment_plan": learning_assessment_plan,
        "design_artifact_paths": artifact_paths,
        "learning_assessment_plan_artifact_path": artifact_path,
    }


def resolve_skill_assessment_requirements(state: dict) -> dict:
    """Resolve external skill-assessment expectations from packaging plus shared signal context."""
    packaging_profile = state.get("packaging_profile", {}) or {}
    course_design = _load_design_artifact(
        state,
        artifact_key="course_design",
        state_key="course_design",
        filename="courses/index.yaml",
    ) or {}
    course_design = course_design.get("courses", [])
    detected_patterns = state.get("detected_patterns", []) or []

    concept_targets = _unique_preserve_order(
        skill_id
        for course in course_design
        for skill_id in course.get("skill_ids", [])
    )

    requirements = {
        "external_owner": "skill_assessments_team",
        "placement_eligibility": "product-packaging-defined",
        "skill_assessment_every_n_topics": packaging_profile.get("skill_assessment_every_n_topics", 8),
        "question_types": packaging_profile.get("skill_assessment_question_types", []),
        "difficulty_levels": packaging_profile.get("skill_assessment_difficulty_levels", []),
        "concept_targets": concept_targets,
        "industry_patterns": [pattern.get("description", "pattern") for pattern in detected_patterns[:5]],
        "signal_sync_status": "shared_loop_a_patterns" if detected_patterns else "no_explicit_signal_digest",
    }
    artifact_path, artifact_paths = _persist_design_artifact(
        state=state,
        artifact_key="skill_assessment_requirements",
        filename="skill_assessment_requirements.yaml",
        payload=requirements,
    )

    print(
        "  Skill assessment requirements: "
        f"{len(requirements['question_types'])} question types, cadence every "
        f"{requirements['skill_assessment_every_n_topics']} topics"
    )
    return {
        "skill_assessment_requirements": requirements,
        "design_artifact_paths": artifact_paths,
        "skill_assessment_requirements_artifact_path": artifact_path,
    }


def align_learning_with_skill_assessments(state: dict) -> dict:
    """Check whether internal learning assessments prepare learners for external skill assessments."""
    learning_plan = _load_design_artifact(
        state,
        artifact_key="learning_assessment_plan",
        state_key="learning_assessment_plan",
        filename="learning_assessments.yaml",
    ) or {}
    requirements = _load_design_artifact(
        state,
        artifact_key="skill_assessment_requirements",
        state_key="skill_assessment_requirements",
        filename="skill_assessment_requirements.yaml",
    ) or {}
    course_design = _load_design_artifact(
        state,
        artifact_key="course_design",
        state_key="course_design",
        filename="courses/index.yaml",
    ) or {}
    module_design = _load_design_artifact(
        state,
        artifact_key="module_design",
        state_key="module_design",
        filename="modules/index.yaml",
    ) or {}
    topic_design = _load_design_artifact(
        state,
        artifact_key="topic_design",
        state_key="topic_design",
        filename="topics/index.yaml",
    ) or {}
    courses = course_design.get("courses", [])
    modules = module_design.get("modules", [])
    topics = topic_design.get("topics", [])
    detected_patterns = state.get("detected_patterns", []) or []

    covered_question_types = set(learning_plan.get("question_types_covered", []))
    required_question_types = set(requirements.get("question_types", []))
    covered_difficulties = set(learning_plan.get("difficulty_levels_covered", []))
    required_difficulties = set(requirements.get("difficulty_levels", []))

    learning_concepts = set(
        skill_id
        for course in courses
        for skill_id in course.get("skill_ids", [])
    )
    required_concepts = set(requirements.get("concept_targets", []))

    learning_keywords = _extract_keywords(
        [course.get("title", "") for course in courses]
        + [module.get("title", "") for module in modules]
        + [topic.get("title", "") for topic in topics]
        + [pattern.get("description", "") for pattern in detected_patterns]
    )
    required_pattern_keywords = _extract_keywords(requirements.get("industry_patterns", []))
    shared_pattern_keywords = sorted(set(learning_keywords) & set(required_pattern_keywords))

    topics_per_module = {}
    for topic in topics:
        topics_per_module[topic["module_id"]] = topics_per_module.get(topic["module_id"], 0) + 1
    max_topics_before_module_quiz = max(topics_per_module.values()) if topics_per_module else 0
    required_cadence = int(requirements.get("skill_assessment_every_n_topics", 8) or 8)

    question_type_missing = sorted(required_question_types - covered_question_types)
    difficulty_missing = sorted(required_difficulties - covered_difficulties)
    concept_missing = sorted(required_concepts - learning_concepts)

    question_type_status = "aligned" if not question_type_missing else "gap"
    difficulty_status = "aligned" if not difficulty_missing else "gap"
    concept_status = "aligned" if not concept_missing else "gap"
    if not required_pattern_keywords:
        pattern_status = "not_applicable"
    elif shared_pattern_keywords:
        pattern_status = "aligned"
    else:
        pattern_status = "gap"

    cadence_status = "aligned" if max_topics_before_module_quiz <= required_cadence else "gap"

    status_values = [question_type_status, difficulty_status, concept_status, pattern_status, cadence_status]
    overall_status = "aligned" if all(status in {"aligned", "not_applicable"} for status in status_values) else "needs_review"

    alignment_report = {
        "overall_status": overall_status,
        "question_type_alignment": {
            "status": question_type_status,
            "covered": sorted(covered_question_types),
            "required": sorted(required_question_types),
            "missing": question_type_missing,
        },
        "difficulty_alignment": {
            "status": difficulty_status,
            "covered": sorted(covered_difficulties),
            "required": sorted(required_difficulties),
            "missing": difficulty_missing,
        },
        "concept_coverage_alignment": {
            "status": concept_status,
            "covered_count": len(learning_concepts),
            "required_count": len(required_concepts),
            "missing": concept_missing,
        },
        "pattern_alignment": {
            "status": pattern_status,
            "shared_keywords": shared_pattern_keywords,
            "required_patterns": requirements.get("industry_patterns", []),
        },
        "cadence_alignment": {
            "status": cadence_status,
            "max_topics_before_module_quiz": max_topics_before_module_quiz,
            "skill_assessment_every_n_topics": required_cadence,
        },
    }
    artifact_path, artifact_paths = _persist_design_artifact(
        state=state,
        artifact_key="assessment_alignment_report",
        filename="assessment_alignment.yaml",
        payload=alignment_report,
    )

    print(f"  Skill-assessment alignment: {overall_status}")
    return {
        "assessment_alignment_report": alignment_report,
        "design_artifact_paths": artifact_paths,
        "assessment_alignment_report_artifact_path": artifact_path,
    }
