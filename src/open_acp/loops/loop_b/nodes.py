"""Loop B nodes — curriculum design using wiki intelligence."""
import json
from pathlib import Path
import re

import yaml

from open_acp.knowledge.wiki_engine import WikiEngine
from open_acp.styles.pedagogy_resolver import PedagogyResolver
from open_acp.utils.claude import ClaudeClient
from open_acp.config.curriculum_context import (
    find_project_root,
    load_yaml,
    resolve_packaging_profile as resolve_packaging_manifest_profile,
    resolve_product_context as resolve_product_manifest_context,
    resolve_structure_profile as resolve_structure_profile_context,
)


def _find_project_root() -> Path:
    return find_project_root()


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


def _assessment_difficulty(topic_sequence: int, topic_count: int) -> str:
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
            f"- Target total hours: {context.get('target_total_hours', 'unknown')}",
            f"- Slot budget hours: {context.get('slot_budget_hours', 'unknown')}",
            f"- Reserved hours: {context.get('reserved_hours', 'unknown')}",
            f"- Available design hours: {context.get('available_design_hours', 'unknown')}",
            f"- Resolution reason: {context.get('resolution_reason', 'not provided')}",
        ]
    )


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


def _default_allowed_local_overrides(profile: str) -> list[str]:
    mapping = {
        "project_build_along": ["concept_progression", "tool_workflow"],
        "concept_progression": ["skill_drill", "case_reasoning"],
        "skill_drill": ["concept_progression"],
        "case_reasoning": ["concept_progression"],
        "tool_workflow": ["concept_progression", "project_build_along"],
    }
    return mapping.get(profile, [])


def _fallback_terminal_outcomes(domain: str, pedagogy_profile: str, curriculum_source_context: str) -> list[str]:
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
    target_total_hours = source_total_hours if source_total_hours is not None else 20.0
    slot_budget_hours = target_total_hours
    reserved_hours = float(packaging_profile.get("reserved_hours", 0.0) or 0.0)
    available_design_hours = max(0.0, round(slot_budget_hours - reserved_hours, 2))

    if source_total_hours is not None:
        reason = "source-defined total hours preserved from curriculum source context"
    else:
        reason = "no explicit source total hours found; using default planning budget"

    context = {
        "context_id": f"time_budget_{_slugify(domain)}",
        "source_total_hours": source_total_hours,
        "target_total_hours": target_total_hours,
        "slot_budget_hours": slot_budget_hours,
        "reserved_hours": reserved_hours,
        "available_design_hours": available_design_hours,
        "resolution_reason": reason,
    }

    print(f"  Time budget: target {target_total_hours} hours")
    return {"time_budget_context": context}


def load_wiki_context(state: dict) -> dict:
    """Load skill graph and learner model from wiki entities."""
    wiki = WikiEngine()
    domain = state.get("domain", "ml-engineering")

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

    # Gather competitor entities
    competitors = wiki.list_entities(entity_type="competitor")
    competitor_context = "## Competitors\n"
    for c in competitors:
        entity = wiki.get_entity("competitor", c["entity_id"])
        if entity:
            competitor_context += f"- **{c['title']}**: {entity['content'][:300]}\n"

    curriculum_source_context = _load_curriculum_sources(domain)

    print(f"  Wiki context loaded: {len(skills)} skills, {len(learners)} learner segments, {len(competitors)} competitors")
    return {
        "skill_graph_context": skill_context + "\n" + competitor_context,
        "learner_context": learner_context,
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
    curriculum_source_context = state.get("curriculum_source_context") or state.get("program_context", "")

    product_summary = _product_summary(product_context)
    structure_summary = _structure_summary(structure_profile)
    packaging_summary = _packaging_summary(packaging_profile)
    design_priority_summary = _build_design_priority_summary(design_priority_profile)
    time_budget_summary = _build_time_budget_summary(time_budget_context)

    claude = ClaudeClient()
    prompt = f"""Create a curriculum brief for the "{domain}" stack.

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

## Skill Context
{skill_context or "No explicit skill context provided."}

## Learner Context
{learner_context or "No explicit learner context provided."}

Decide only the Stage 0 brief:
1. Program name
2. Primary target learner segments (maximum 2)
3. Differentiation angle
4. Default pedagogy profile and allowed local overrides
5. Total hours
6. Terminal outcomes (maximum 5, observable verbs only)
7. Success metrics

Do not design modules, topics, or content yet.

Return JSON:
{{
  "brief_id": "brief_{domain}",
  "program_name": "Program name",
  "audience": {{
    "primary": ["audience_segment_id"],
    "english_level": 8
  }},
  "pedagogy": {{
    "default_profile": "{pedagogy_profile}",
    "allowed_local_overrides": ["concept_progression"]
  }},
  "total_hours": {time_budget_context.get("target_total_hours", 20.0)},
  "terminal_outcomes": [
    "Observable terminal outcome"
  ],
  "success_metrics": {{
    "completion_rate_target": 0.75,
    "median_assessment_score_target": 0.70
  }},
  "differentiation": "One-line differentiation angle",
  "design_priority_dimensions": {json.dumps(design_priority_profile.get("ordered_dimensions", []))}
}}

Important constraints:
- Terminal outcomes must use observable verbs, not vague verbs like understand or know.
- Keep primary audience to at most 2 segments.
- Use the resolved pedagogy profile unless the sources clearly justify a different default.
- Respect source-defined total hours when provided.
- Keep this brief compact and structural.

Return ONLY the JSON object."""

    response = claude.generate(
        prompt=prompt,
        system="You are a curriculum architect preparing a brief artifact before curriculum structuring.",
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
            "program_name": product_context.get("product_label") or f"{domain.title()} Curriculum",
            "audience": {
                "primary": audience_candidates[:2],
                "english_level": 8,
            },
            "pedagogy": {
                "default_profile": pedagogy_profile,
                "allowed_local_overrides": _default_allowed_local_overrides(pedagogy_profile),
            },
            "total_hours": time_budget_context.get("target_total_hours", 20.0),
            "terminal_outcomes": _fallback_terminal_outcomes(domain, pedagogy_profile, curriculum_source_context),
            "success_metrics": {
                "completion_rate_target": 0.75,
                "median_assessment_score_target": 0.70,
            },
            "differentiation": (
                "Milestone-driven, implementation-first curriculum shaped by product and structure constraints."
            ),
            "design_priority_dimensions": design_priority_profile.get("ordered_dimensions", []),
        }

    brief.setdefault("brief_id", f"brief_{_slugify(domain)}")
    brief.setdefault("program_name", product_context.get("product_label") or f"{domain.title()} Curriculum")
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
    brief.setdefault("total_hours", time_budget_context.get("target_total_hours", 20.0))
    brief.setdefault(
        "terminal_outcomes",
        _fallback_terminal_outcomes(domain, pedagogy_profile, curriculum_source_context),
    )
    brief.setdefault(
        "success_metrics",
        {
            "completion_rate_target": 0.75,
            "median_assessment_score_target": 0.70,
        },
    )
    brief.setdefault("differentiation", "Curriculum shaped by product, structure, and skill-outcome priorities.")
    brief.setdefault("design_priority_dimensions", design_priority_profile.get("ordered_dimensions", []))
    brief["pedagogy"].setdefault("default_profile", pedagogy_profile)
    brief["pedagogy"].setdefault("allowed_local_overrides", _default_allowed_local_overrides(pedagogy_profile))
    brief["pedagogy"].setdefault("rationale", pedagogy_rationale)
    brief["time_budget"] = time_budget_context
    brief["product_ref"] = product_context.get("product_label")
    brief["structure_profile_id"] = structure_profile.get("structure_profile_id")
    brief["packaging_profile_id"] = packaging_profile.get("packaging_profile_id")

    if brief_generation_status == "fallback_non_json":
        print("  Brief generation parse failed; using deterministic fallback brief.")
    else:
        print(
            "  Brief: "
            f"{brief.get('program_name', domain)} "
            f"({len(brief.get('terminal_outcomes', []))} terminal outcomes)"
        )

    return {
        "brief_generation_status": brief_generation_status,
        "brief_generation_note": brief_generation_note,
        "brief_generation_raw_response": brief_generation_raw_response,
        "brief": brief,
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


def generate_curriculum(state: dict) -> dict:
    """Generate packaged course structure from the approved brief and source curriculum."""
    domain = state.get("domain", "ml-engineering")
    brief = state.get("brief", {}) or {}
    curriculum_source_context = state.get("curriculum_source_context") or state.get("program_context", "")
    content_type = state.get("content_type", "concept_explainer")
    structure_profile = state.get("structure_profile", {}) or {}
    packaging_profile = state.get("packaging_profile", {}) or {}
    structure_summary = _structure_summary(structure_profile)
    packaging_summary = _packaging_summary(packaging_profile)
    brief_json = json.dumps(brief, indent=2)
    pedagogy_profile = ((brief.get("pedagogy") or {}).get("default_profile")) or state.get("pedagogy_profile", "concept_progression")
    pedagogy_rationale = ((brief.get("pedagogy") or {}).get("rationale")) or state.get("pedagogy_rationale", "content-type default")
    total_hours = brief.get("total_hours", 20.0)
    program_name = brief.get("program_name", f"{domain.title()} Curriculum")

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

Use backward design and keep this stage structural:
1. Start with terminal outcomes (what can learners DO after?)
2. Select which packaged courses belong in this curriculum based on:
   - time budget
   - priority skill requirements
   - product-linked skill-assessment expectations
3. Map prerequisites between packaged courses.
4. Estimate duration per course.
5. Use source-defined levels, phases, or tracks only as ordering cues or title hints; do not emit explicit level output at this stage.
6. Use the packaging profile to decide how coarse or fine the packaged course boundaries should be.
7. If breadth/depth packaging scope is known, reflect it in course scope or course title rather than inventing a separate level object.
8. Do not decide topic allocation here. Topic-to-course assignment belongs to later design stages and should eventually be informed by channel-analysis inputs.
9. Keep this stage structural and compact rather than fully expanded.

Return JSON:
{{
  "curriculum_id": "cur_{domain}",
  "brief_ref": "{brief.get('brief_id', f'brief_{domain}')}",
  "program_name": "{program_name}",
  "domain": "{domain}",
  "pedagogy_profile": "{pedagogy_profile}",
  "pedagogy_rationale": "{pedagogy_rationale}",
  "courses": [
    {{
      "course_id": "c1",
      "title": "Module Title",
      "sequence": 1,
      "objectives": [
        {{"id": "obj_1", "statement": "...", "bloom_level": "understand", "skill_ids": ["skill_id"]}}
      ],
      "estimated_hours": 1.5,
      "prerequisite_courses": [],
      "content_types": ["{content_type}"]
    }}
  ],
  "total_hours": {total_hours}
}}

Important constraints:
- Respect the total hours from the brief unless the source curriculum clearly forces a different total.
- Preserve source-defined progression when it exists, but encode it through course sequence and course scope rather than explicit level output.
- Represent each major phase or specialization as its own packaged course only when time budget and product requirements justify it.
- Do not collapse a detailed long-form curriculum into 4-6 generic courses unless the source clearly justifies it.
- Limit to 2-3 concise objectives per course.
- Keep each objective statement under 18 words.
- Use stable snake_case wiki skill IDs when referencing skills, not display titles.
- Prefer 4-8 packaged courses total for this stage unless the source clearly requires more.

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
                "Curriculum generation response could not be parsed as JSON and appears to have been cut off mid-output. "
                "Using an empty fallback curriculum draft."
            )
        else:
            curriculum_generation_note = (
                "Curriculum generation response could not be parsed as JSON. "
                "Using an empty fallback curriculum draft."
            )
        curriculum_generation_raw_response = response[:4000]
        data = {
            "curriculum_id": f"cur_{domain}",
            "brief_ref": brief.get("brief_id", f"brief_{domain}"),
            "program_name": program_name,
            "domain": domain,
            "pedagogy_profile": pedagogy_profile,
            "pedagogy_rationale": pedagogy_rationale,
            "courses": [],
            "total_hours": total_hours,
        }

    courses = data.get("courses", [])
    if curriculum_generation_status == "fallback_non_json":
        print("  Curriculum generation parse failed; using empty fallback curriculum draft.")
    else:
        print(f"  Curriculum: {len(courses)} courses, {data.get('total_hours', 0)} hours")
    return {
        "curriculum_generation_status": curriculum_generation_status,
        "curriculum_generation_note": curriculum_generation_note,
        "curriculum_generation_raw_response": curriculum_generation_raw_response,
        "previous_curriculum_map": state.get("curriculum_map"),
        "curriculum_map": data,
    }


def compare_curriculum_changes(state: dict) -> dict:
    """Compare the current curriculum draft to the previous saved version, if any."""
    current = state.get("curriculum_map", {}) or {}
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
    curriculum = state.get("curriculum_map", {}) or {}
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
            }
        )

    course_design = {
        "curriculum_id": curriculum.get("curriculum_id", "unknown_curriculum"),
        "course_count": len(courses),
        "courses": courses,
    }
    print(f"  Course design: {len(courses)} course seeds prepared")
    return {"course_design": course_design}


def design_modules(state: dict) -> dict:
    """Expand each course into packaging-shaped modules."""
    courses = (state.get("course_design", {}) or {}).get("courses", [])
    packaging_profile = state.get("packaging_profile", {}) or {}
    phase_labels = _module_phase_labels(packaging_profile)
    module_rule = packaging_profile.get("module_count_per_course", {})

    modules = []
    for course in courses:
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
                }
            )

    module_design = {
        "total_module_count": len(modules),
        "modules": modules,
    }
    print(f"  Module design: {len(modules)} modules across {len(courses)} courses")
    return {"module_design": module_design}


def design_topics(state: dict) -> dict:
    """Design topics inside each module using packaging defaults."""
    modules = (state.get("module_design", {}) or {}).get("modules", [])
    packaging_profile = state.get("packaging_profile", {}) or {}
    pedagogy_profile = state.get("pedagogy_profile", "concept_progression")
    topic_rule = packaging_profile.get("topic_count_per_module", {})
    phase_labels = _topic_phase_labels(packaging_profile, pedagogy_profile)

    topics = []
    for module in modules:
        topic_count = _resolve_configured_count(float(module.get("estimated_hours", 0) or 0), topic_rule)
        minutes_per_topic = round((float(module.get("estimated_hours", 0) or 0) * 60) / topic_count, 1) if topic_count else 0

        for index in range(topic_count):
            phase_label = phase_labels[index % len(phase_labels)]
            topics.append(
                {
                    "topic_id": f"{module['module_id']}_t{index + 1}",
                    "module_id": module["module_id"],
                    "course_id": module["course_id"],
                    "title": f"{module['title']} — {phase_label}",
                    "sequence_within_module": index + 1,
                    "estimated_minutes": minutes_per_topic,
                    "skill_ids": module.get("skill_ids", []),
                    "focus_outcomes": module.get("focus_outcomes", []),
                }
            )

    topic_design = {
        "total_topic_count": len(topics),
        "topics": topics,
    }
    print(f"  Topic design: {len(topics)} topics prepared")
    return {"topic_design": topic_design}


def design_learning_units(state: dict) -> dict:
    """Assign learning unit types to each topic based on packaging and pedagogy."""
    topics = (state.get("topic_design", {}) or {}).get("topics", [])
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
    return {"learning_unit_plan": learning_unit_plan}


def design_practice(state: dict) -> dict:
    """Design practice touchpoints from the planned learning-unit mix."""
    topics = (state.get("topic_design", {}) or {}).get("topics", [])
    learning_units = (state.get("learning_unit_plan", {}) or {}).get("learning_units", [])

    practice_items = []
    for topic in topics:
        topic_units = [unit for unit in learning_units if unit.get("topic_id") == topic["topic_id"]]
        if any(unit.get("unit_type") == "coding_practice_unit" for unit in topic_units):
            practice_type = "coding_practice"
        elif any(unit.get("unit_type") == "mcq_practice_unit" for unit in topic_units):
            practice_type = "mcq_retrieval"
        else:
            practice_type = "guided_reflection"

        practice_items.append(
            {
                "topic_id": topic["topic_id"],
                "module_id": topic["module_id"],
                "practice_type": practice_type,
                "estimated_minutes": max(10, round(float(topic.get("estimated_minutes", 0) or 0) * 0.25)),
                "goal": f"Reinforce {topic['title']}",
            }
        )

    practice_design = {
        "practice_touchpoint_count": len(practice_items),
        "practice_types": _unique_preserve_order([item["practice_type"] for item in practice_items]),
        "items": practice_items,
    }
    print(f"  Practice design: {len(practice_items)} touchpoints")
    return {"practice_design": practice_design}


def design_learning_assessments(state: dict) -> dict:
    """Design internal learning assessments before external skill-assessment alignment."""
    modules = (state.get("module_design", {}) or {}).get("modules", [])
    topics = (state.get("topic_design", {}) or {}).get("topics", [])
    learning_units = (state.get("learning_unit_plan", {}) or {}).get("learning_units", [])
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
                ),
                "concept_tags": topic.get("skill_ids", []),
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

    print(
        "  Learning assessments: "
        f"{len(classroom_quizzes)} classroom quizzes, {len(module_quizzes)} module quizzes"
    )
    return {"learning_assessment_plan": learning_assessment_plan}


def resolve_skill_assessment_requirements(state: dict) -> dict:
    """Resolve external skill-assessment expectations from packaging plus shared signal context."""
    packaging_profile = state.get("packaging_profile", {}) or {}
    course_design = (state.get("course_design", {}) or {}).get("courses", [])
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

    print(
        "  Skill assessment requirements: "
        f"{len(requirements['question_types'])} question types, cadence every "
        f"{requirements['skill_assessment_every_n_topics']} topics"
    )
    return {"skill_assessment_requirements": requirements}


def align_learning_with_skill_assessments(state: dict) -> dict:
    """Check whether internal learning assessments prepare learners for external skill assessments."""
    learning_plan = state.get("learning_assessment_plan", {}) or {}
    requirements = state.get("skill_assessment_requirements", {}) or {}
    courses = (state.get("course_design", {}) or {}).get("courses", [])
    modules = (state.get("module_design", {}) or {}).get("modules", [])
    topics = (state.get("topic_design", {}) or {}).get("topics", [])
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

    print(f"  Skill-assessment alignment: {overall_status}")
    return {"assessment_alignment_report": alignment_report}


# Compatibility alias for older call sites.
select_pedagogy = resolve_pedagogy_profile
