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

from open_acp.models.state import LoopAState
from open_acp.models.signals import RawSignal, SignalBatch, ChannelCategory, ChannelType
from open_acp.knowledge.wiki_engine import WikiEngine
from open_acp.utils.claude import ClaudeClient
from open_acp.config.constants import STRONG_MODEL, CHEAP_MODEL, DRIFT_THRESHOLD


def _get_raw_sources_dir() -> Path:
    """Get the knowledge/raw/ directory path."""
    return Path(__file__).parent.parent.parent / "knowledge" / "raw"


def _load_raw_sources(domain: str) -> list[dict]:
    """Load all markdown files from knowledge/raw/ subdirectories."""
    raw_dir = _get_raw_sources_dir()
    sources = []
    for subdir in ["sources", "job_postings", "competitors", "learner"]:
        src_dir = raw_dir / subdir
        if src_dir.exists():
            for f in sorted(src_dir.glob("*.md")):
                sources.append({
                    "filename": f.name,
                    "category": subdir,
                    "content": f.read_text(encoding="utf-8"),
                })
    return sources


def ingest_signals(state: dict) -> dict:
    """Load raw sources and convert them into a SignalBatch."""
    domain = state.get("domain", "ml-engineering")
    cycle_id = state.get("cycle_id", "unknown")

    raw_sources = _load_raw_sources(domain)

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
            metadata={"filename": src["filename"]},
        ))

    batch = SignalBatch(
        batch_id=f"batch_{cycle_id}",
        signals=signals,
        ingested_at=datetime.now(UTC).isoformat(),
        source_domain=domain,
    )

    print(f"  Ingested {len(signals)} signals from {len(raw_sources)} sources")
    return {"signal_batch": batch}


def detect_patterns(state: dict) -> dict:
    """Analyze signals against existing wiki knowledge to detect new patterns."""
    signal_batch: SignalBatch = state.get("signal_batch")
    domain = state.get("domain", "ml-engineering")

    if not signal_batch or not signal_batch.signals:
        return {"detected_patterns": [], "drift_score": 0.0}

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
        patterns = [{"pattern_id": "p_raw", "description": "Pattern detection returned non-JSON", "evidence": response[:500], "affected_areas": [], "confidence": 0.3, "is_new": True}]
        drift_score = 0.5

    print(f"  Detected {len(patterns)} patterns, drift_score={drift_score:.2f}")
    return {"detected_patterns": patterns, "drift_score": drift_score}


def update_skill_graph(state: dict) -> dict:
    """Create or update skill entities in the wiki based on detected patterns."""
    patterns = state.get("detected_patterns", [])
    signal_batch = state.get("signal_batch")
    domain = state.get("domain", "ml-engineering")

    wiki = WikiEngine()
    created = []  # Only NEW entries this node creates (reducer will merge)
    updated = []

    # Ask Claude to extract skills from signals
    signal_content = ""
    if signal_batch:
        for sig in signal_batch.signals:
            if sig.channel_name in ("sources", "job_postings"):
                signal_content += sig.content[:1500] + "\n\n"

    if not signal_content:
        return {"wiki_entries_created": [], "wiki_entries_updated": []}

    claude = ClaudeClient()
    prompt = f"""From these signals about "{domain}", extract a list of technical skills with demand scores.

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
    "related_skills": ["pytorch", "pandas"]
  }}
]

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
                cross_references=cross_refs,
            )
            created.append(f"skill_{skill_id}")

    print(f"  Skills — created: {len(created) - len(state.get('wiki_entries_created', []))}, updated: {len(updated) - len(state.get('wiki_entries_updated', []))}")
    return {"wiki_entries_created": created, "wiki_entries_updated": updated}


def update_learner_model(state: dict) -> dict:
    """Create or update audience segment entities in the wiki."""
    signal_batch: SignalBatch = state.get("signal_batch")
    domain = state.get("domain", "ml-engineering")

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

    print(f"  Learner segments — created: {len(created) - len(state.get('wiki_entries_created', []))}, updated: {len(updated) - len(state.get('wiki_entries_updated', []))}")
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

    print(f"  Competitors — created: {len(created) - len(state.get('wiki_entries_created', []))}, updated: {len(updated) - len(state.get('wiki_entries_updated', []))}")
    return {"wiki_entries_created": created, "wiki_entries_updated": updated}


def update_wiki_index(state: dict) -> dict:
    """Rebuild index.md and log summary."""
    wiki = WikiEngine()
    wiki.rebuild_index()

    created = state.get("wiki_entries_created", [])
    updated = state.get("wiki_entries_updated", [])
    print(f"  Wiki index rebuilt. Total: {len(created)} created, {len(updated)} updated")

    return {}
