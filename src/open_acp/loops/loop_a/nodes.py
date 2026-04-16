"""Loop A nodes — wiki-integrated intelligence gathering.

Nodes:
1. ingest_signals — load raw sources and create SignalBatch
2. detect_patterns — compare new signals against existing wiki knowledge
3. update_skill_graph — create/update skill entities in wiki
4. update_learner_model — create/update audience segment entities in wiki
5. update_competitor_map — create/update competitor entities in wiki
6. update_wiki_index — rebuild index.md and append to log.md
"""
import json
import os
from datetime import datetime, UTC
from pathlib import Path
from typing import Any

import yaml

from open_acp.models.state import LoopAState
from open_acp.models.signals import RawSignal, SignalBatch, ChannelCategory, ChannelType
from open_acp.knowledge.wiki_engine import WikiEngine
from open_acp.utils.claude import ClaudeClient
from open_acp.config.constants import STRONG_MODEL, CHEAP_MODEL, DRIFT_THRESHOLD
from open_acp.config.curriculum_context import (
    find_project_root,
    load_stack_manifest,
    resolve_product_context as resolve_product_manifest_context,
    resolve_structure_profile as resolve_structure_profile_context,
)


def _get_sources_root() -> Path:
    """Get the canonical knowledge/sources/ directory path."""
    return _get_project_root() / "knowledge" / "sources"


def _get_project_root() -> Path:
    return find_project_root()


def _infer_category(path: Path) -> str:
    if "competitors" in path.parts:
        return "competitors"
    if "learner" in path.parts:
        return "learner"
    if "job_postings" in path.parts or "hiring" in path.parts:
        return "job_postings"
    if "market" in path.parts:
        return "sources"
    return "sources"


def _normalize_token(value: str) -> str:
    return value.lower().replace("-", "").replace("_", "").replace(" ", "")


def _describe_source(source: dict) -> str:
    filename = source.get("filename", "unknown")
    category = source.get("category", "sources")
    origin = source.get("source_origin", "unknown")
    return f"{filename} ({category}, {origin})"


def _infer_role_in_stack(skill: dict) -> str:
    explicit = (skill.get("role_in_stack") or "").strip().lower().replace(" ", "_")
    if explicit:
        return explicit

    demand_score = float(skill.get("demand_score", 0.5) or 0.5)
    if demand_score >= 0.85:
        return "foundational"
    if demand_score >= 0.7:
        return "core"
    return "supporting"


def _default_pedagogy_notes(skill: dict, role_in_stack: str) -> list[str]:
    notes = skill.get("pedagogy_notes", []) or []
    if notes:
        return notes
    if role_in_stack == "foundational":
        return ["Teach early, revisit often, and connect the skill to downstream build work."]
    if role_in_stack == "core":
        return ["Use worked practice and checkpoint questions to reinforce the skill in context."]
    return ["Treat as supporting knowledge and connect it to its primary upstream or downstream skills."]


def _default_assessment_implications(skill: dict, role_in_stack: str) -> list[str]:
    implications = skill.get("assessment_implications", []) or []
    if implications:
        return implications

    related = ", ".join(skill.get("related_skills", [])[:3]) or "downstream work"
    if role_in_stack == "foundational":
        return [f"Expect repeated checks before learners use this in {related}."]
    if role_in_stack == "core":
        return [f"Assess learners on applying this skill during {related} tasks."]
    return [f"Use lightweight checks and tie the skill to {related} when relevant."]


def _build_stack_profile_summary(domain: str, skill: dict, role_in_stack: str) -> str:
    name = skill.get("name", skill.get("skill_id", "Unknown Skill"))
    description = skill.get("description", "")
    prerequisites = ", ".join(skill.get("prerequisites", []) or []) or "none"
    downstream = ", ".join(skill.get("related_skills", []) or []) or "none"
    pedagogy_notes = "\n".join(f"- {note}" for note in _default_pedagogy_notes(skill, role_in_stack))
    assessment_notes = "\n".join(
        f"- {note}" for note in _default_assessment_implications(skill, role_in_stack)
    )

    return (
        f"# {name} in {domain}\n\n"
        f"{description}\n\n"
        f"**Role in stack:** {role_in_stack}\n\n"
        f"**Prerequisite skills:** {prerequisites}\n\n"
        f"**Downstream skills:** {downstream}\n\n"
        f"## Pedagogy Notes\n{pedagogy_notes}\n\n"
        f"## Assessment Implications\n{assessment_notes}\n"
    )


def _select_relevant_patterns(patterns: list[dict], area: str, limit: int = 4) -> list[dict]:
    relevant = [
        pattern for pattern in patterns
        if area in (pattern.get("affected_areas", []) or [])
    ]
    if relevant:
        return relevant[:limit]
    return patterns[:limit]


def _extract_signal_source_refs(
    signal_batch: SignalBatch | None,
    allowed_channels: tuple[str, ...] | None = None,
) -> list[str]:
    if not signal_batch:
        return []

    refs: list[str] = []
    for signal in signal_batch.signals:
        if allowed_channels and signal.channel_name not in allowed_channels:
            continue
        filename = signal.metadata.get("filename")
        if filename and filename not in refs:
            refs.append(filename)
    return refs


def _is_obviously_domain_specific(domain: str, source: dict) -> bool:
    domain_token = _normalize_token(domain)
    if not domain_token:
        return False

    path_bits = [
        str(source.get("path", "")),
        source.get("filename", ""),
    ]
    return any(domain_token in _normalize_token(bit) for bit in path_bits if bit)


def _build_bootstrap_warnings(domain: str, raw_sources: list[dict]) -> list[str]:
    if not raw_sources:
        return [
            f"No raw sources were found for domain '{domain}'. "
            "Loop A will continue in bootstrap mode with an empty signal batch."
        ]

    warnings: list[str] = []
    categories_present = {src.get("category", "sources") for src in raw_sources}

    for required in ("job_postings", "competitors"):
        if required not in categories_present:
            warnings.append(
                f"No {required.replace('_', ' ')} sources were found for domain '{domain}'. "
                "Loop A will continue in bootstrap mode, but wiki updates will be thin for that area."
            )

    for category in ("job_postings", "competitors"):
        category_sources = [src for src in raw_sources if src.get("category") == category]
        if category_sources and not any(_is_obviously_domain_specific(domain, src) for src in category_sources):
            filenames = ", ".join(src.get("filename", "unknown") for src in category_sources[:3])
            warnings.append(
                f"No obviously {domain}-specific {category.replace('_', ' ')} sources were found. "
                f"Bootstrap mode will use shared or generic inputs for now ({filenames})."
            )

    return warnings


def _load_manifest_sources(
    domain: str,
    product_family: str | None = None,
    product_version: str | None = None,
) -> list[dict]:
    """Load raw inputs from stack, shared signal, and product manifests when available."""
    project_root = _get_project_root()
    manifest = load_stack_manifest(domain)
    manifest_path_str = manifest.get("_manifest_path")
    if not manifest_path_str:
        return []
    manifest_path = Path(manifest_path_str)

    resolved_paths: list[Path] = []

    shared_signal_manifest = manifest.get("shared_signal_manifest")
    if shared_signal_manifest:
        shared_manifest_path = (manifest_path.parent / shared_signal_manifest).resolve()
        if shared_manifest_path.exists():
            with open(shared_manifest_path, encoding="utf-8") as f:
                shared = yaml.safe_load(f) or {}
            for paths in (shared.get("seed_inputs", {}) or {}).values():
                for path_str in paths or []:
                    resolved_paths.append((project_root / path_str).resolve())

    for key in ["curriculum_sources", "competitor_sources"]:
        for path_str in manifest.get(key, []) or []:
            resolved_paths.append((project_root / path_str).resolve())

    product_context = resolve_product_manifest_context(
        domain=domain,
        product_family=product_family,
        product_version=product_version,
    )
    for path_str in product_context.get("target_audience_sources", []) or []:
        resolved_paths.append((project_root / path_str).resolve())

    seen: set[Path] = set()
    sources: list[dict] = []
    for path in resolved_paths:
        if path in seen or not path.exists():
            continue
        seen.add(path)
        sources.append(
            {
                "filename": path.name,
                "category": _infer_category(path),
                "content": path.read_text(encoding="utf-8"),
                "path": str(path),
                "source_origin": "manifest",
            }
        )

    return sources


def _product_entity_id(product_context: dict) -> str:
    family = _normalize_token(product_context.get("product_family") or "default")
    version = _normalize_token(product_context.get("product_version") or "")
    return f"{family}_{version}" if version else family


def _build_product_context_markdown(
    domain: str,
    product_context: dict,
    structure_profile: dict,
    detected_patterns: list[dict],
) -> str:
    feature_flags = product_context.get("feature_flags", {}) or {}
    notes = product_context.get("notes", []) or []
    lines = [
        f"## Domain",
        f"- `{domain}`",
        "",
        "## Product Context",
        f"- Product label: {product_context.get('product_label', 'unknown')}",
        f"- Product category: {product_context.get('product_category', 'unknown')}",
        f"- Curriculum container kind: {product_context.get('curriculum_container_kind', 'unknown')}",
        f"- Delivery mode: {product_context.get('delivery_mode', 'unspecified')}",
        f"- Focus priority: {product_context.get('focus_priority', 'default')}",
        "",
        "## Structure Profile",
        f"- Structure profile: {structure_profile.get('structure_profile_id', 'unknown')}",
        f"- Hierarchy: {' -> '.join(structure_profile.get('hierarchy', [])) or 'unknown'}",
        "",
        "## Feature Flags",
    ]
    if feature_flags:
        for key, value in sorted(feature_flags.items()):
            lines.append(f"- {key}: {value}")
    else:
        lines.append("- none")

    lines.append("")
    lines.append("## Signal-Aware Notes")
    if detected_patterns:
        for pattern in detected_patterns[:3]:
            lines.append(f"- {pattern.get('description', 'pattern')}")
    else:
        lines.append("- No explicit Loop A patterns were available.")

    if notes:
        lines.append("")
        lines.append("## Manifest Notes")
        for note in notes[:5]:
            lines.append(f"- {note}")

    return "\n".join(lines)


def _load_raw_sources(
    domain: str,
    product_family: str | None = None,
    product_version: str | None = None,
) -> list[dict]:
    """Load all markdown files from canonical knowledge/sources directories.

    Prefer manifest-driven source selection when a stack/domain manifest exists.
    """
    manifest_sources = _load_manifest_sources(
        domain,
        product_family=product_family,
        product_version=product_version,
    )
    if manifest_sources:
        return manifest_sources

    sources_root = _get_sources_root()
    sources = []
    fallback_dirs: list[tuple[Path, str]] = []

    if sources_root.exists():
        domain_root = sources_root / "domains" / domain
        fallback_dirs.extend(
            [
                (sources_root / "shared" / "learner", "learner"),
                (sources_root / "shared" / "hiring", "job_postings"),
                (sources_root / "shared" / "competitors", "competitors"),
                (sources_root / "shared" / "market", "sources"),
                (domain_root, "sources"),
            ]
        )

    seen_paths: set[Path] = set()
    for src_dir, category in fallback_dirs:
        if not src_dir.exists():
            continue
        for f in sorted(src_dir.rglob("*.md")):
            if f in seen_paths:
                continue
            seen_paths.add(f)
            sources.append({
                "filename": f.name,
                "category": category,
                "content": f.read_text(encoding="utf-8"),
                "path": str(f),
                "source_origin": "filesystem_fallback",
            })
    return sources


def ingest_signals(state: dict) -> dict:
    """Load raw sources and convert them into a SignalBatch."""
    domain = state.get("domain", "ml-engineering")
    cycle_id = state.get("cycle_id", "unknown")
    strict_domain_inputs = bool(state.get("strict_domain_inputs", False))
    product_family = state.get("product_family")
    product_version = state.get("product_version")

    stack_manifest = load_stack_manifest(domain)
    if strict_domain_inputs and not stack_manifest:
        raise ValueError(
            f"No stack manifest was found for domain '{domain}'. "
            "Strict domain-input mode does not allow generic filesystem fallback."
        )

    raw_sources = _load_raw_sources(
        domain,
        product_family=product_family,
        product_version=product_version,
    )
    if strict_domain_inputs and not raw_sources:
        raise ValueError(
            f"No canonical source inputs were found for domain '{domain}'. "
            "Strict domain-input mode requires manifest-backed sources."
        )
    bootstrap_warnings = _build_bootstrap_warnings(domain, raw_sources)

    signals = []
    category_map = {
        "sources": ChannelCategory.INDUSTRY_MARKET,
        "job_postings": ChannelCategory.INTERVIEW_INTEL,
        "competitors": ChannelCategory.INDUSTRY_MARKET,
        "learner": ChannelCategory.STUDENT_LEARNING,
    }

    for i, src in enumerate(raw_sources):
        signals.append(RawSignal(
            signal_id=f"sig_{cycle_id}_{i}",
            channel_category=category_map.get(src["category"], ChannelCategory.INDUSTRY_MARKET),
            channel_name=src["category"],
            content=src["content"],
            timestamp=datetime.now(UTC).isoformat(),
            signal_type=ChannelType.PROACTIVE,
            metadata={
                "filename": src["filename"],
                "source_origin": src.get("source_origin", "unknown"),
                "source_path": src.get("path", ""),
            },
        ))

    batch = SignalBatch(
        batch_id=f"batch_{cycle_id}",
        signals=signals,
        ingested_at=datetime.now(UTC).isoformat(),
        source_domain=domain,
    )

    print(f"  Ingested {len(signals)} signals from {len(raw_sources)} sources")
    for source in raw_sources[:6]:
        print(f"  Signal source: {_describe_source(source)}")
    if len(raw_sources) > 6:
        print(f"  Signal source: ... and {len(raw_sources) - 6} more")
    for warning in bootstrap_warnings:
        print(f"  Bootstrap warning: {warning}")

    return {"signal_batch": batch, "bootstrap_warnings": bootstrap_warnings}


def detect_patterns(state: dict) -> dict:
    """Analyze signals against existing wiki knowledge to detect new patterns."""
    signal_batch: SignalBatch = state.get("signal_batch")
    domain = state.get("domain", "ml-engineering")

    if not signal_batch or not signal_batch.signals:
        return {
            "detected_patterns": [],
            "pattern_detection_status": "no_signals",
            "pattern_detection_note": "No signals were available for pattern detection.",
            "drift_score": 0.0,
        }

    # Gather existing wiki knowledge for context
    wiki = WikiEngine()
    existing_entities = wiki.list_entities()
    existing_context = ""
    if existing_entities:
        existing_context = "## Existing Wiki Entities:\n"
        for e in existing_entities:
            existing_context += f"- {e['entity_type']}/{e['entity_id']}: {e['title']} (confidence={e['confidence']})\n"

    # Combine signal content (truncate each to avoid token limits)
    signal_summary = ""
    for sig in signal_batch.signals:
        content_preview = sig.content[:2000]
        signal_summary += f"\n### {sig.metadata.get('filename', 'unknown')} ({sig.channel_name})\n{content_preview}\n"

    # Ask Claude to detect patterns
    claude = ClaudeClient()
    prompt = f"""Analyze these signals for the domain "{domain}" and identify key patterns.

{existing_context}

## New Signals:
{signal_summary}

Return a JSON object with:
{{
  "patterns": [
    {{
      "pattern_id": "p1",
      "description": "Brief description of the pattern",
      "evidence": "What signals support this",
      "affected_areas": ["skill_graph", "learner_model", "competitor_map"],
      "confidence": 0.8,
      "is_new": true
    }}
  ],
  "drift_score": 0.0-1.0 (how much has changed since existing wiki state),
  "summary": "One paragraph summary of intelligence findings"
}}

Return ONLY the JSON object."""

    response = claude.generate(
        prompt=prompt,
        system="You are an intelligence analyst identifying patterns across educational market signals. Be precise and evidence-based.",
        model_tier="strong",
        max_tokens=4096,
    )

    # Parse response
    pattern_detection_status = "parsed"
    pattern_detection_note = None
    try:
        # Strip code fences
        cleaned = response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned[cleaned.index("\n")+1:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        data = json.loads(cleaned)
        patterns = data.get("patterns", [])
        drift_score = float(data.get("drift_score", 0.5))
    except (json.JSONDecodeError, ValueError):
        pattern_detection_status = "fallback_non_json"
        pattern_detection_note = (
            "Pattern detection response could not be parsed as JSON. "
            "Using a fallback placeholder pattern and default drift score 0.50."
        )
        patterns = [{"pattern_id": "p_raw", "description": "Pattern detection returned non-JSON", "evidence": response[:500], "affected_areas": [], "confidence": 0.3, "is_new": True}]
        drift_score = 0.5

    if pattern_detection_status == "fallback_non_json":
        print(
            f"  Pattern detection parse failed; using fallback placeholder and default drift score {drift_score:.2f}."
        )
    elif pattern_detection_status == "no_signals":
        print("  Pattern detection skipped because no signals were available.")
    else:
        print(f"  Detected {len(patterns)} patterns, drift_score={drift_score:.2f}")
    for pattern in patterns[:3]:
        affected_areas = ", ".join(pattern.get("affected_areas", []) or []) or "unspecified"
        print(f"  Detected pattern: {pattern.get('description', 'unknown pattern')} [{affected_areas}]")
    return {
        "detected_patterns": patterns,
        "pattern_detection_status": pattern_detection_status,
        "pattern_detection_note": pattern_detection_note,
        "drift_score": drift_score,
    }


def update_skill_graph(state: dict) -> dict:
    """Create or update skill entities in the wiki based on detected patterns."""
    patterns = state.get("detected_patterns", [])
    signal_batch = state.get("signal_batch")
    domain = state.get("domain", "ml-engineering")

    wiki = WikiEngine()
    created = []  # Only NEW entries this node creates (reducer will merge)
    updated = []
    stack_profiles_created = []
    stack_profiles_updated = []

    # Ask Claude to extract skills from signals
    signal_content = ""
    if signal_batch:
        for sig in signal_batch.signals:
            if sig.channel_name in ("sources", "job_postings"):
                signal_content += sig.content[:1500] + "\n\n"

    if not signal_content:
        return {"wiki_entries_created": [], "wiki_entries_updated": []}

    relevant_patterns = _select_relevant_patterns(patterns, "skill_graph")
    pattern_context = ""
    if relevant_patterns:
        pattern_context = "## Detected Patterns To Honor\n"
        for pattern in relevant_patterns:
            affected_areas = ", ".join(pattern.get("affected_areas", []) or []) or "unspecified"
            pattern_context += (
                f"- {pattern.get('description', 'unknown pattern')} "
                f"(areas: {affected_areas}; evidence: {pattern.get('evidence', 'not provided')})\n"
            )

    existing_skills = wiki.list_entities(entity_type="skill")
    existing_skill_context = ""
    if existing_skills:
        existing_skill_context = "## Existing Canonical Skill IDs\n"
        for skill in existing_skills[:20]:
            existing_skill_context += f"- {skill['entity_id']}: {skill['title']}\n"

    signal_sources = _extract_signal_source_refs(signal_batch, allowed_channels=("sources", "job_postings"))

    claude = ClaudeClient()
    prompt = f"""From these signals about "{domain}", extract a list of technical skills with demand scores.

{pattern_context}
{existing_skill_context}

{signal_content[:6000]}

Return a JSON array of skills:
[
  {{
    "skill_id": "python",
    "name": "Python Programming",
    "demand_score": 0.95,
    "durability": "durable",
    "description": "Brief description of the skill and its relevance",
    "prerequisites": ["programming_basics"],
    "related_skills": ["pytorch", "pandas"],
    "role_in_stack": "foundational",
    "pedagogy_notes": ["Teach early and revisit through build checkpoints."],
    "assessment_implications": ["Expect repeated checks before project-based usage."]
  }}
]

Use the detected patterns to prioritize extraction.
Reuse existing canonical skill IDs when a near-duplicate already exists.
If multiple names refer to the same skill, choose one canonical skill_id instead of creating duplicates.
Extract the top 8-12 most important skills. Return ONLY the JSON array."""

    response = claude.generate(prompt=prompt, system="You are a skills analyst. Extract concrete, specific skills with accurate demand scores.", model_tier="cheap", max_tokens=4096)

    try:
        cleaned = response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned[cleaned.index("\n")+1:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        skills = json.loads(cleaned.strip())
    except (json.JSONDecodeError, ValueError):
        skills = []

    for skill in skills:
        skill_id = skill.get("skill_id", "").replace(" ", "_").lower()
        if not skill_id:
            continue

        existing = wiki.get_entity("skill", skill_id)
        if existing:
            wiki.update_entity(
                entity_id=skill_id,
                entity_type="skill",
                content_delta=f"Demand score updated to {skill.get('demand_score', 0.5)}. {skill.get('description', '')}",
                reason="Signal ingestion update",
                new_confidence=skill.get("demand_score", 0.5),
                new_sources=signal_sources,
            )
            updated.append(f"skill_{skill_id}")
        else:
            cross_refs = [f"skill_{s}" for s in skill.get("related_skills", [])[:5]]
            wiki.create_entity(
                entity_type="skill",
                entity_id=skill_id,
                title=skill.get("name", skill_id),
                content=f"# {skill.get('name', skill_id)}\n\n{skill.get('description', '')}\n\n**Prerequisites:** {', '.join(skill.get('prerequisites', []))}\n\n**Demand Score:** {skill.get('demand_score', 0.5)}",
                confidence=skill.get("demand_score", 0.5),
                durability=skill.get("durability", "unknown"),
                sources=signal_sources,
                cross_references=cross_refs,
            )
            created.append(f"skill_{skill_id}")

        stack_profile_existed = wiki.get_stack_profile(stack_id=domain, entity_type="skill", entity_id=skill_id)
        role_in_stack = _infer_role_in_stack(skill)
        wiki.write_stack_profile(
            stack_id=domain,
            entity_type="skill",
            entity_id=skill_id,
            title=f"{skill.get('name', skill_id)} ({domain})",
            summary=_build_stack_profile_summary(domain=domain, skill=skill, role_in_stack=role_in_stack),
            relevance_score=float(skill.get("demand_score", 0.5) or 0.5),
            role_in_stack=role_in_stack,
            prerequisite_skills=skill.get("prerequisites", []) or [],
            downstream_skills=skill.get("related_skills", []) or [],
            pedagogy_notes=_default_pedagogy_notes(skill, role_in_stack),
            assessment_implications=_default_assessment_implications(skill, role_in_stack),
            sources=signal_sources,
        )
        if stack_profile_existed:
            stack_profiles_updated.append(f"{domain}/skill_{skill_id}")
        else:
            stack_profiles_created.append(f"{domain}/skill_{skill_id}")

    if relevant_patterns:
        print("  Skill graph grounded in detected patterns:")
        for pattern in relevant_patterns[:3]:
            print(f"    - {pattern.get('description', 'unknown pattern')}")
    print(f"  Skills — created: {len(created)}, updated: {len(updated)}")
    print(
        "  Stack skill profiles — created: "
        f"{len(stack_profiles_created)}, updated: {len(stack_profiles_updated)}"
    )
    return {
        "wiki_entries_created": created,
        "wiki_entries_updated": updated,
        "stack_profiles_created": stack_profiles_created,
        "stack_profiles_updated": stack_profiles_updated,
    }


def update_learner_model(state: dict) -> dict:
    """Materialize target-audience context into runtime audience-segment entities."""
    signal_batch: SignalBatch = state.get("signal_batch")
    domain = state.get("domain", "ml-engineering")
    product_family = state.get("product_family")
    product_version = state.get("product_version")

    wiki = WikiEngine()
    created = []  # Only NEW entries this node creates (reducer will merge)
    updated = []

    # Find learner signals
    learner_content = ""
    if signal_batch:
        for sig in signal_batch.signals:
            if sig.channel_name == "learner":
                learner_content += sig.content[:2000] + "\n\n"

    if not learner_content:
        if product_family:
            version_suffix = f" {product_version}" if product_version else ""
            raise ValueError(
                f"Explicit product run '{product_family}{version_suffix}' is missing product-specific target-audience inputs. "
                "Add canonical target_audience_sources to the product manifest before running update_learner_model."
            )
        return {"wiki_entries_created": created, "wiki_entries_updated": updated}

    claude = ClaudeClient()
    prompt = f"""From this learner research for "{domain}", extract audience segments.

{learner_content[:4000]}

Return a JSON array of audience segments:
[
  {{
    "segment_id": "career_switcher",
    "name": "Career Switcher",
    "description": "Profile description",
    "knowledge_gaps": ["statistics", "ml_theory"],
    "misconceptions": ["ML is just calling sklearn.fit()"],
    "motivation_drivers": ["career growth", "salary increase"]
  }}
]

Return ONLY the JSON array."""

    response = claude.generate(prompt=prompt, system="You are a learner analysis specialist.", model_tier="cheap", max_tokens=4096)

    try:
        cleaned = response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned[cleaned.index("\n")+1:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        segments = json.loads(cleaned.strip())
    except (json.JSONDecodeError, ValueError):
        segments = []

    for seg in segments:
        seg_id = seg.get("segment_id", "").replace(" ", "_").lower()
        if not seg_id:
            continue

        existing = wiki.get_entity("audience_segment", seg_id)
        gap_refs = [f"skill_{g}" for g in seg.get("knowledge_gaps", [])[:5]]

        if existing:
            wiki.update_entity(
                entity_id=seg_id, entity_type="audience_segment",
                content_delta=f"Updated profile: {seg.get('description', '')}",
                reason="Learner signal update",
            )
            updated.append(f"audience_segment_{seg_id}")
        else:
            wiki.create_entity(
                entity_type="audience_segment", entity_id=seg_id,
                title=seg.get("name", seg_id),
                content=f"# {seg.get('name', seg_id)}\n\n{seg.get('description', '')}\n\n**Knowledge Gaps:** {', '.join(seg.get('knowledge_gaps', []))}\n\n**Misconceptions:** {', '.join(seg.get('misconceptions', []))}\n\n**Motivation:** {', '.join(seg.get('motivation_drivers', []))}",
                confidence=0.7,
                durability="perishable",
                cross_references=gap_refs,
            )
            created.append(f"audience_segment_{seg_id}")

    print(f"  Learner segments — created: {len(created)}, updated: {len(updated)}")
    return {"wiki_entries_created": created, "wiki_entries_updated": updated}


def update_competitor_map(state: dict) -> dict:
    """Create or update competitor entities in the wiki."""
    signal_batch: SignalBatch = state.get("signal_batch")
    domain = state.get("domain", "ml-engineering")

    wiki = WikiEngine()
    created = []  # Only NEW entries this node creates (reducer will merge)
    updated = []

    competitor_content = ""
    if signal_batch:
        for sig in signal_batch.signals:
            if sig.channel_name == "competitors":
                competitor_content += sig.content[:2000] + "\n\n"

    if not competitor_content:
        return {"wiki_entries_created": created, "wiki_entries_updated": updated}

    claude = ClaudeClient()
    prompt = f"""From this competitor analysis for "{domain}", extract competitor profiles.

{competitor_content[:4000]}

Return a JSON array:
[
  {{
    "competitor_id": "datacamppro",
    "name": "DataCampPro",
    "description": "Profile description",
    "strengths": ["large library"],
    "weaknesses": ["shallow depth"],
    "skills_covered": ["python", "pandas"],
    "skills_missing": ["mlops", "llms"]
  }}
]

Return ONLY the JSON array."""

    response = claude.generate(prompt=prompt, system="You are a competitive intelligence analyst.", model_tier="cheap", max_tokens=4096)

    try:
        cleaned = response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned[cleaned.index("\n")+1:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        competitors = json.loads(cleaned.strip())
    except (json.JSONDecodeError, ValueError):
        competitors = []

    for comp in competitors:
        comp_id = comp.get("competitor_id", "").replace(" ", "_").lower()
        if not comp_id:
            continue

        existing = wiki.get_entity("competitor", comp_id)
        skill_refs = [f"skill_{s}" for s in comp.get("skills_covered", [])[:5]]

        if existing:
            wiki.update_entity(
                entity_id=comp_id, entity_type="competitor",
                content_delta=f"Updated analysis: {comp.get('description', '')}",
                reason="Competitor signal update",
            )
            updated.append(f"competitor_{comp_id}")
        else:
            wiki.create_entity(
                entity_type="competitor", entity_id=comp_id,
                title=comp.get("name", comp_id),
                content=f"# {comp.get('name', comp_id)}\n\n{comp.get('description', '')}\n\n**Strengths:** {', '.join(comp.get('strengths', []))}\n\n**Weaknesses:** {', '.join(comp.get('weaknesses', []))}\n\n**Covers:** {', '.join(comp.get('skills_covered', []))}\n\n**Missing:** {', '.join(comp.get('skills_missing', []))}",
                confidence=0.7,
                durability="perishable",
                cross_references=skill_refs,
            )
            created.append(f"competitor_{comp_id}")

    print(f"  Competitors — created: {len(created)}, updated: {len(updated)}")
    return {"wiki_entries_created": created, "wiki_entries_updated": updated}


def update_product_context(state: dict) -> dict:
    """Resolve product and structure context and persist a derived runtime summary."""
    domain = state.get("domain", "ml-engineering")
    product_family = state.get("product_family")
    product_version = state.get("product_version")
    require_product_context = bool(state.get("require_product_context", False))
    detected_patterns = state.get("detected_patterns", []) or []

    product_context = resolve_product_manifest_context(
        domain=domain,
        product_family=product_family,
        product_version=product_version,
    )
    if require_product_context and not product_context.get("is_explicit_product"):
        raise ValueError(
            "Explicit product context is required for this run. "
            "Provide product_family and product_version instead of relying on stack-only defaults."
        )
    structure_profile = resolve_structure_profile_context(product_context)

    print(
        "  Product context: "
        f"{product_context.get('product_label', 'Stack-only default')} -> "
        f"{structure_profile.get('structure_profile_id', 'standard_product_structure')}"
    )

    if not product_context.get("is_explicit_product"):
        return {
            "product_context": product_context,
            "structure_profile": structure_profile,
        }

    stack_manifest = load_stack_manifest(domain)
    sources = [
        product_context.get("manifest_path", ""),
        stack_manifest.get("_manifest_path", ""),
    ]
    sources = [source for source in sources if source]

    content = _build_product_context_markdown(
        domain=domain,
        product_context=product_context,
        structure_profile=structure_profile,
        detected_patterns=detected_patterns,
    )
    entity_id = _product_entity_id(product_context)
    entity_key = f"product_{entity_id}"
    title = f"{product_context.get('product_label', 'Product')} Context"

    wiki = WikiEngine()
    existing = wiki.get_entity("product", entity_id)
    created: list[str] = []
    updated: list[str] = []

    if existing:
        wiki.update_entity(
            entity_id=entity_id,
            entity_type="product",
            content_delta=content,
            reason="Loop A product context refresh",
            new_confidence=0.9,
            new_sources=sources,
        )
        updated.append(entity_key)
    else:
        wiki.create_entity(
            entity_type="product",
            entity_id=entity_id,
            title=title,
            content=content,
            confidence=0.9,
            sources=sources,
            durability="versioned",
        )
        created.append(entity_key)

    return {
        "product_context": product_context,
        "structure_profile": structure_profile,
        "wiki_entries_created": created,
        "wiki_entries_updated": updated,
    }


def update_wiki_index(state: dict) -> dict:
    """Rebuild index.md and log summary."""
    wiki = WikiEngine()
    wiki.rebuild_index()

    created = state.get("wiki_entries_created", [])
    updated = state.get("wiki_entries_updated", [])
    print(f"  Wiki index rebuilt. Total: {len(created)} created, {len(updated)} updated")

    return {}
