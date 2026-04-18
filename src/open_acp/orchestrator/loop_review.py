"""Loop review runner — execute Loop A or Loop B one node at a time."""
from __future__ import annotations

import importlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel

from open_acp.models.signals import SignalBatch


_LOOP_STAGE_ORDER = {
    "loop_a": [
        "ingest_signals",
        "detect_patterns",
        "update_skill_graph",
        "update_learner_model",
        "update_competitor_map",
        "update_product_context",
        "update_wiki_index",
    ],
    "loop_b": [
        "load_wiki_context",
        "resolve_product_context",
        "resolve_structure_profile",
        "resolve_packaging_profile",
        "resolve_design_priority_profile",
        "resolve_time_budget_context",
        "resolve_pedagogy_profile",
        "generate_brief",
        "generate_curriculum",
        "compare_curriculum_changes",
        "design_courses",
        "design_modules",
        "design_topics",
        "design_learning_units",
        "design_practice",
        "design_learning_assessments",
        "resolve_skill_assessment_requirements",
        "align_learning_with_skill_assessments",
    ],
}

_LOOP_MODULES = {
    "loop_a": "open_acp.loops.loop_a.nodes",
    "loop_b": "open_acp.loops.loop_b.nodes",
}


def _find_project_root() -> Path:
    current = Path(__file__).resolve()
    for ancestor in current.parents:
        if (ancestor / "pyproject.toml").exists():
            return ancestor
    return current.parents[3]


class LoopReviewRunner:
    """Persist and review Loop A / Loop B state one node at a time."""

    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir = Path(output_dir) if output_dir else _find_project_root() / "outputs" / "loop_reviews"

    def execute_review_stage(
        self,
        loop_id: str,
        base_state: dict[str, Any],
        stage_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Execute one loop node, persist state, and return a review packet."""
        normalized_loop = self._normalize_loop_id(loop_id)
        state = self._load_state(normalized_loop, base_state)
        selected_stage = self._select_stage(normalized_loop, state, stage_id)

        if selected_stage is None:
            return {
                "status": "complete",
                "loop_id": normalized_loop,
                "state_path": str(self._state_path(normalized_loop, state)),
            }

        hydrated_state = self._rehydrate_state(normalized_loop, state.copy())
        stage_fn = self._load_stage_callable(normalized_loop, selected_stage)
        updates = stage_fn(hydrated_state)

        merged_state = self._merge_state(normalized_loop, state, updates)
        completed = merged_state.setdefault("_completed_stages", [])
        if selected_stage not in completed:
            completed.append(selected_stage)
        merged_state["_updated_at"] = datetime.now(UTC).isoformat()

        self._save_state(normalized_loop, merged_state)
        next_stage_id = self._next_stage_id(normalized_loop, selected_stage)
        review_state = self._rehydrate_state(normalized_loop, merged_state.copy())
        review_packet = self._build_review_packet(
            loop_id=normalized_loop,
            stage_id=selected_stage,
            state=review_state,
            updates=updates,
            next_stage_id=next_stage_id,
        )
        review_packet_paths = self._save_review_packet(review_packet, normalized_loop, merged_state)

        return {
            "status": "awaiting_review",
            "loop_id": normalized_loop,
            "stage_id": selected_stage,
            "next_stage_id": next_stage_id,
            "state_path": str(self._state_path(normalized_loop, merged_state)),
            "review_packet": review_packet,
            "review_packet_paths": review_packet_paths,
        }

    def _normalize_loop_id(self, loop_id: str) -> str:
        normalized = loop_id.strip().lower().replace("-", "_")
        if normalized in {"a", "loopa"}:
            normalized = "loop_a"
        if normalized in {"b", "loopb"}:
            normalized = "loop_b"
        if normalized not in _LOOP_STAGE_ORDER:
            raise ValueError(f"Unsupported loop_id '{loop_id}'. Expected one of: loop_a, loop_b.")
        return normalized

    def _select_stage(
        self,
        loop_id: str,
        state: dict[str, Any],
        stage_id: Optional[str],
    ) -> Optional[str]:
        stages = _LOOP_STAGE_ORDER[loop_id]
        completed = state.get("_completed_stages", [])

        if stage_id:
            if stage_id not in stages:
                raise ValueError(f"Unknown stage '{stage_id}' for {loop_id}.")
            requested_index = stages.index(stage_id)
            missing_priors = [prior for prior in stages[:requested_index] if prior not in completed]
            if missing_priors:
                raise RuntimeError(
                    f"Cannot execute '{stage_id}' because prior stages are incomplete: {', '.join(missing_priors)}."
                )
            return stage_id

        for stage in stages:
            if stage not in completed:
                return stage
        return None

    def _next_stage_id(self, loop_id: str, stage_id: str) -> Optional[str]:
        stages = _LOOP_STAGE_ORDER[loop_id]
        index = stages.index(stage_id)
        if index + 1 < len(stages):
            return stages[index + 1]
        return None

    def _load_stage_callable(self, loop_id: str, stage_id: str):
        module = importlib.import_module(_LOOP_MODULES[loop_id])
        return getattr(module, stage_id)

    def _state_dir(self, state: dict[str, Any]) -> Path:
        domain = state.get("domain", "unknown")
        cycle_id = state.get("cycle_id", "cycle_1")
        return self.output_dir / domain / cycle_id

    def _state_path(self, loop_id: str, state: dict[str, Any]) -> Path:
        return self._state_dir(state) / f"{loop_id}_state.json"

    def _load_state(self, loop_id: str, base_state: dict[str, Any]) -> dict[str, Any]:
        state = dict(base_state)
        path = self._state_path(loop_id, state)
        if path.exists():
            loaded = json.loads(path.read_text(encoding="utf-8"))
            state.update(loaded)
        if loop_id == "loop_b":
            loop_a_path = self._state_path("loop_a", state)
            if loop_a_path.exists():
                loop_a_state = json.loads(loop_a_path.read_text(encoding="utf-8"))
                for key in (
                    "detected_patterns",
                    "drift_score",
                    "pattern_detection_status",
                    "pattern_detection_note",
                    "product_family",
                    "product_version",
                    "require_product_context",
                    "strict_domain_inputs",
                    "product_context",
                    "structure_profile",
                ):
                    state.setdefault(key, loop_a_state.get(key))
        return state

    def _save_state(self, loop_id: str, state: dict[str, Any]) -> None:
        path = self._state_path(loop_id, state)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self._to_jsonable(state), indent=2), encoding="utf-8")

    def _merge_state(
        self,
        loop_id: str,
        state: dict[str, Any],
        updates: dict[str, Any],
    ) -> dict[str, Any]:
        merged = state.copy()
        list_merge_keys = set()
        if loop_id == "loop_a":
            list_merge_keys = {
                "wiki_entries_created",
                "wiki_entries_updated",
                "stack_profiles_created",
                "stack_profiles_updated",
            }

        for key, value in updates.items():
            if key in list_merge_keys:
                merged[key] = (merged.get(key, []) or []) + (value or [])
            else:
                merged[key] = value
        return merged

    def _rehydrate_state(self, loop_id: str, state: dict[str, Any]) -> dict[str, Any]:
        if loop_id == "loop_a" and isinstance(state.get("signal_batch"), dict):
            state["signal_batch"] = SignalBatch.model_validate(state["signal_batch"])
        return state

    def _build_review_packet(
        self,
        loop_id: str,
        stage_id: str,
        state: dict[str, Any],
        updates: dict[str, Any],
        next_stage_id: Optional[str],
    ) -> dict[str, Any]:
        summary, key_decisions = self._summarize_stage(loop_id, stage_id, state, updates)
        return {
            "loop_id": loop_id,
            "stage_id": stage_id,
            "domain": state.get("domain", "unknown"),
            "cycle_id": state.get("cycle_id", "cycle_1"),
            "summary": summary,
            "key_decisions": key_decisions,
            "next_stage_id": next_stage_id,
            "generated_at": datetime.now(UTC).isoformat(),
        }

    def _save_review_packet(
        self,
        packet: dict[str, Any],
        loop_id: str,
        state: dict[str, Any],
    ) -> dict[str, str]:
        review_dir = self._state_dir(state) / "review_packets"
        review_dir.mkdir(parents=True, exist_ok=True)

        json_path = review_dir / f"{loop_id}_{packet['stage_id']}.json"
        md_path = review_dir / f"{loop_id}_{packet['stage_id']}.md"

        json_path.write_text(json.dumps(packet, indent=2), encoding="utf-8")
        md_path.write_text(self._render_review_packet_markdown(packet), encoding="utf-8")

        return {"json": str(json_path), "markdown": str(md_path)}

    def _summarize_stage(
        self,
        loop_id: str,
        stage_id: str,
        state: dict[str, Any],
        updates: dict[str, Any],
    ) -> tuple[str, list[str]]:
        if loop_id == "loop_a":
            return self._summarize_loop_a(stage_id, state, updates)
        if loop_id == "loop_b":
            return self._summarize_loop_b(stage_id, state, updates)
        return ("Stage complete.", [f"Updated keys: {', '.join(sorted(updates.keys()))}"])

    def _summarize_loop_a(
        self,
        stage_id: str,
        state: dict[str, Any],
        updates: dict[str, Any],
    ) -> tuple[str, list[str]]:
        if stage_id == "ingest_signals":
            signal_batch = state.get("signal_batch")
            signals = getattr(signal_batch, "signals", []) if signal_batch else []
            categories = sorted({getattr(sig, "channel_name", "unknown") for sig in signals})
            signal_sources = [
                f"{sig.metadata.get('filename', 'unknown')} ({getattr(sig, 'channel_name', 'unknown')})"
                for sig in signals[:6]
            ]
            warnings = state.get("bootstrap_warnings", []) or []
            summary = f"Ingested {len(signals)} raw signals for domain '{state.get('domain', 'unknown')}'."
            if warnings:
                summary += f" Bootstrap mode is active with {len(warnings)} coverage warning(s)."

            key_decisions = [
                f"Signal categories discovered: {', '.join(categories) if categories else 'none'}.",
                f"Signals reviewed: {' | '.join(signal_sources) if signal_sources else 'none'}.",
                f"Cycle id: {state.get('cycle_id', 'cycle_1')}.",
            ]
            key_decisions.extend(warnings)
            return (
                summary,
                key_decisions,
            )

        if stage_id == "detect_patterns":
            patterns = state.get("detected_patterns", []) or []
            descriptions = [pattern.get("description", "pattern") for pattern in patterns[:3]]
            signal_batch = state.get("signal_batch")
            signals = getattr(signal_batch, "signals", []) if signal_batch else []
            signal_sources = [
                f"{sig.metadata.get('filename', 'unknown')} ({getattr(sig, 'channel_name', 'unknown')})"
                for sig in signals[:6]
            ]
            status = state.get("pattern_detection_status", "parsed")
            note = state.get("pattern_detection_note")
            if status == "fallback_non_json":
                key_decisions = [
                    f"Signals compared: {' | '.join(signal_sources) if signal_sources else 'none'}.",
                ]
                if note:
                    key_decisions.append(note)
                key_decisions.append(
                    f"Fallback placeholder pattern: {' | '.join(descriptions) if descriptions else 'none'}."
                )
                return (
                    f"Pattern detection parse failed; using fallback placeholder and default drift score {state.get('drift_score', 0.0):.2f}.",
                    key_decisions,
                )
            return (
                f"Detected {len(patterns)} patterns with drift score {state.get('drift_score', 0.0):.2f}.",
                [
                    f"Signals compared: {' | '.join(signal_sources) if signal_sources else 'none'}.",
                    f"Top patterns: {' | '.join(descriptions) if descriptions else 'none'}.",
                ],
            )

        if stage_id == "update_skill_graph":
            created = [item for item in updates.get("wiki_entries_created", []) if item.startswith("skill_")]
            updated = [item for item in updates.get("wiki_entries_updated", []) if item.startswith("skill_")]
            stack_profiles_created = updates.get("stack_profiles_created", []) or []
            stack_profiles_updated = updates.get("stack_profiles_updated", []) or []
            patterns = state.get("detected_patterns", []) or []
            skill_patterns = [
                pattern.get("description", "pattern")
                for pattern in patterns
                if "skill_graph" in (pattern.get("affected_areas", []) or [])
            ][:3]
            status = state.get("pattern_detection_status", "parsed")
            pattern_guidance = (
                f"Patterns used to guide skill extraction: {' | '.join(skill_patterns) if skill_patterns else 'none explicitly tagged for skill_graph'}."
            )
            if status == "fallback_non_json":
                pattern_guidance = (
                "Pattern guidance was limited because detect_patterns fell back after a non-JSON response."
            )
            return (
                f"Skill graph updates complete: {len(created)} created, {len(updated)} updated.",
                [
                    f"Skill entities touched: {', '.join((created + updated)[:6]) or 'none'}.",
                    (
                        f"Stack skill profiles touched: "
                        f"{', '.join((stack_profiles_created + stack_profiles_updated)[:6]) or 'none'}."
                    ),
                    pattern_guidance,
                ],
            )

        if stage_id == "update_learner_model":
            created = [item for item in updates.get("wiki_entries_created", []) if item.startswith("audience_segment_")]
            updated = [item for item in updates.get("wiki_entries_updated", []) if item.startswith("audience_segment_")]
            return (
                f"Learner model updates complete: {len(created)} created, {len(updated)} updated.",
                [f"Audience segments touched: {', '.join((created + updated)[:6]) or 'none'}."],
            )

        if stage_id == "update_competitor_map":
            created = [item for item in updates.get("wiki_entries_created", []) if item.startswith("competitor_")]
            updated = [item for item in updates.get("wiki_entries_updated", []) if item.startswith("competitor_")]
            return (
                f"Competitor map updates complete: {len(created)} created, {len(updated)} updated.",
                [f"Competitor entities touched: {', '.join((created + updated)[:6]) or 'none'}."],
            )

        if stage_id == "update_product_context":
            product_context = state.get("product_context", {}) or {}
            structure_profile = state.get("structure_profile", {}) or {}
            created = [item for item in updates.get("wiki_entries_created", []) if item.startswith("product_")]
            updated = [item for item in updates.get("wiki_entries_updated", []) if item.startswith("product_")]
            return (
                f"Resolved product context: {product_context.get('product_label', 'Stack-only default')}.",
                [
                    f"Structure profile: {structure_profile.get('structure_profile_id', 'standard_product_structure')}.",
                    f"Product wiki entities touched: {', '.join((created + updated)[:4]) or 'none'}.",
                    f"Resolution reason: {product_context.get('resolution_reason', 'not provided')}.",
                ],
            )

        if stage_id == "update_wiki_index":
            return (
                "Wiki index rebuilt after Loop A updates.",
                [
                    f"Total created entries this cycle so far: {len(state.get('wiki_entries_created', []))}.",
                    f"Total updated entries this cycle so far: {len(state.get('wiki_entries_updated', []))}.",
                    f"Total stack profiles created this cycle so far: {len(state.get('stack_profiles_created', []))}.",
                    f"Total stack profiles updated this cycle so far: {len(state.get('stack_profiles_updated', []))}.",
                ],
            )

        return ("Loop A stage complete.", [f"Updated keys: {', '.join(sorted(updates.keys()))}."])

    def _summarize_loop_b(
        self,
        stage_id: str,
        state: dict[str, Any],
        updates: dict[str, Any],
    ) -> tuple[str, list[str]]:
        if stage_id == "load_wiki_context":
            skill_lines = sum(1 for line in (state.get("skill_graph_context", "")).splitlines() if line.startswith("- **"))
            learner_lines = sum(1 for line in (state.get("learner_context", "")).splitlines() if line.startswith("- **"))
            pattern_count = len(state.get("detected_patterns", []) or [])
            return (
                "Loaded wiki-derived context for curriculum design.",
                [
                    f"Skill and competitor bullets loaded: {skill_lines}.",
                    f"Learner segment bullets loaded: {learner_lines}.",
                    f"Loop A patterns available to this stage: {pattern_count}.",
                ],
            )

        if stage_id == "resolve_product_context":
            product_context = state.get("product_context", {}) or {}
            return (
                f"Resolved product context: {product_context.get('product_label', 'Stack-only default')}.",
                [
                    f"Product category: {product_context.get('product_category', 'standard_product')}.",
                    f"Curriculum container kind: {product_context.get('curriculum_container_kind', 'standard_curriculum')}.",
                    f"Resolution reason: {product_context.get('resolution_reason', 'not provided')}.",
                ],
            )

        if stage_id == "resolve_structure_profile":
            structure_profile = state.get("structure_profile", {}) or {}
            return (
                f"Resolved structure profile: {structure_profile.get('structure_profile_id', 'standard_product_structure')}.",
                [
                    f"Curriculum container kind: {structure_profile.get('curriculum_container_kind', 'standard_curriculum')}.",
                    f"Hierarchy: {' | '.join(structure_profile.get('hierarchy', [])) or 'none'}.",
                ],
            )

        if stage_id == "resolve_packaging_profile":
            packaging = state.get("packaging_profile", {}) or {}
            provenance = packaging.get("field_provenance", {}) or {}
            return (
                f"Resolved packaging profile: {packaging.get('packaging_profile_id', 'default')}.",
                [
                    (
                        f"Modules per course default: {packaging.get('module_count_per_course', {}).get('default', 'unknown')}"
                        f" (source: {provenance.get('module_count_per_course.default', 'unknown')})."
                    ),
                    (
                        f"Topics per module default: {packaging.get('topic_count_per_module', {}).get('default', 'unknown')}"
                        f" (source: {provenance.get('topic_count_per_module.default', 'unknown')})."
                    ),
                    (
                        f"Allowed learning unit types: {', '.join(packaging.get('allowed_learning_unit_types', [])) or 'none'}"
                        f" (source: {provenance.get('allowed_learning_unit_types', 'unknown')})."
                    ),
                ],
            )

        if stage_id == "resolve_pedagogy_profile":
            return (
                f"Resolved domain pedagogy profile: {state.get('pedagogy_profile', 'unknown')}.",
                [
                    f"Source: {state.get('pedagogy_source', 'unknown')}.",
                    f"Rationale: {state.get('pedagogy_rationale', 'not provided')}",
                ],
            )

        if stage_id == "resolve_design_priority_profile":
            profile = state.get("design_priority_profile", {}) or {}
            return (
                f"Resolved design-priority profile with {len(profile.get('dimensions', []))} active dimensions.",
                [
                    f"Dimensions: {', '.join(profile.get('dimension_ids', [])) or 'none'}.",
                    f"Priority order: {' | '.join(profile.get('ordered_dimensions', [])) or 'none'}.",
                    f"Resolution reason: {profile.get('resolution_reason', 'not provided')}.",
                ],
            )

        if stage_id == "resolve_time_budget_context":
            budget = state.get("time_budget_context", {}) or {}
            return (
                f"Resolved time budget context targeting {budget.get('target_total_hours', 'unknown')} total hours.",
                [
                    f"Source total hours: {budget.get('source_total_hours', 'unknown')}.",
                    f"Slot budget hours: {budget.get('slot_budget_hours', 'unknown')}.",
                    f"Available design hours: {budget.get('available_design_hours', 'unknown')}.",
                    f"Resolution reason: {budget.get('resolution_reason', 'not provided')}.",
                ],
            )

        if stage_id == "generate_brief":
            brief = state.get("brief", {}) or {}
            outcomes = brief.get("stack_learning_outcomes", []) or []
            audience = ((brief.get("audience") or {}).get("primary", [])) or []
            status = state.get("brief_generation_status", "parsed")
            note = state.get("brief_generation_note")
            raw_response = state.get("brief_generation_raw_response")
            artifact_path = state.get("brief_artifact_path")
            if status == "fallback_non_json":
                decisions = []
                if note:
                    decisions.append(note)
                decisions.append(f"Primary audience: {', '.join(audience) or 'none'}.")
                decisions.append(f"Terminal outcomes: {' | '.join(outcomes[:5]) or 'none'}.")
                if artifact_path:
                    decisions.append(f"Artifact path: {artifact_path}")
                if raw_response:
                    preview = " ".join(raw_response.split())[:300]
                    decisions.append(f"Raw response preview: {preview}")
                return ("Brief generation parse failed; using a deterministic fallback brief.", decisions)
            return (
                f"Generated curriculum brief for {brief.get('stack_name', state.get('domain', 'unknown'))}.",
                [
                    f"Primary audience: {', '.join(audience) or 'none'}.",
                    f"Default pedagogy: {(brief.get('pedagogy') or {}).get('default_profile', 'unknown')}.",
                    f"Packaging profile ref: {brief.get('packaging_profile_ref', 'unknown')}.",
                    f"Stack learning outcomes: {' | '.join(outcomes[:5]) or 'none'}.",
                    f"Artifact path: {artifact_path or 'not saved'}.",
                ],
            )

        if stage_id == "generate_curriculum":
            curriculum = state.get("curriculum_map", {}) or {}
            courses = curriculum.get("courses", []) or []
            course_titles = [course.get("title", "Untitled") for course in courses[:6]]
            status = state.get("curriculum_generation_status", "parsed")
            note = state.get("curriculum_generation_note")
            raw_response = state.get("curriculum_generation_raw_response")
            artifact_path = state.get("curriculum_artifact_path")
            validation = state.get("curriculum_validation_report", {}) or {}
            if status == "fallback_non_json":
                decisions = []
                if note:
                    decisions.append(note)
                decisions.append(f"Course flow: {' | '.join(course_titles) if course_titles else 'none'}.")
                if artifact_path:
                    decisions.append(f"Artifact path: {artifact_path}")
                if raw_response:
                    preview = " ".join(raw_response.split())[:300]
                    decisions.append(f"Raw response preview: {preview}")
                return (
                    "Curriculum generation parse failed; using an empty fallback curriculum draft.",
                    decisions,
                )
            return (
                f"Generated domain curriculum with {len(courses)} course seeds and total hours {curriculum.get('total_hours', 0)}.",
                [
                    f"Brief ref: {(state.get('brief') or {}).get('brief_id', 'none')}.",
                    f"Packaging profile ref: {curriculum.get('packaging_profile_ref', 'unknown')}.",
                    f"Course-seed flow: {' | '.join(course_titles) if course_titles else 'none'}.",
                    (
                        "Hours validation: "
                        f"course_sum={validation.get('course_hours_sum', 'unknown')}, "
                        f"capstone={validation.get('capstone_hours', 'unknown')}, "
                        f"grand_quiz={validation.get('grand_quiz_hours', 'unknown')}, "
                        f"curriculum_total={validation.get('curriculum_total_hours', 'unknown')}, "
                        f"target_total={validation.get('target_total_hours', 'unknown')}."
                    ),
                    f"Artifact path: {artifact_path or 'not saved'}.",
                ],
            )

        if stage_id == "compare_curriculum_changes":
            report = state.get("curriculum_change_report", {}) or {}
            status = report.get("status", "baseline")
            return (
                "Recorded curriculum baseline for future comparisons."
                if status == "baseline"
                else "Compared the latest curriculum draft to the previous saved version.",
                [
                    f"Added courses: {', '.join(report.get('added_courses', [])) or 'none'}.",
                    f"Removed courses: {', '.join(report.get('removed_courses', [])) or 'none'}.",
                    f"Hours change: {report.get('hours_change', 0)}.",
                ],
            )

        if stage_id == "design_courses":
            course_design = state.get("course_design", {}) or {}
            courses = course_design.get("courses", [])
            return (
                f"Derived {len(courses)} courses from the curriculum blueprint.",
                [
                    f"Course flow: {' | '.join(course.get('title', 'Untitled') for course in courses[:6]) or 'none'}.",
                    f"Artifact path: {state.get('course_design_artifact_path', 'not saved')}.",
                ],
            )

        if stage_id == "design_modules":
            module_design = state.get("module_design", {}) or {}
            modules = module_design.get("modules", [])
            return (
                f"Designed {len(modules)} modules across the current course set.",
                [
                    f"Module titles: {' | '.join(module.get('title', 'Untitled') for module in modules[:6]) or 'none'}.",
                    f"Artifact path: {state.get('module_design_artifact_path', 'not saved')}.",
                ],
            )

        if stage_id == "design_topics":
            topic_design = state.get("topic_design", {}) or {}
            topics = topic_design.get("topics", [])
            return (
                f"Designed {len(topics)} topics across the current modules.",
                [
                    f"Topic samples: {' | '.join(topic.get('title', 'Untitled') for topic in topics[:6]) or 'none'}.",
                    f"Artifact path: {state.get('topic_design_artifact_path', 'not saved')}.",
                ],
            )

        if stage_id == "design_learning_units":
            learning_units = (state.get("learning_unit_plan", {}) or {}).get("learning_units", [])
            unit_types = (state.get("learning_unit_plan", {}) or {}).get("unit_types_present", [])
            return (
                f"Planned {len(learning_units)} learning units for topic delivery.",
                [
                    f"Learning unit types present: {', '.join(unit_types) or 'none'}.",
                    f"Artifact path: {state.get('learning_unit_plan_artifact_path', 'not saved')}.",
                ],
            )

        if stage_id == "design_practice":
            practice_design = state.get("practice_design", {}) or {}
            return (
                f"Designed {practice_design.get('practice_touchpoint_count', 0)} practice touchpoints.",
                [
                    f"Practice types: {', '.join(practice_design.get('practice_types', [])) or 'none'}.",
                    f"Artifact path: {state.get('practice_design_artifact_path', 'not saved')}.",
                ],
            )

        if stage_id == "design_learning_assessments":
            plan = state.get("learning_assessment_plan", {}) or {}
            return (
                f"Designed {len(plan.get('classroom_quizzes', []))} classroom quizzes and {len(plan.get('module_quizzes', []))} module quizzes.",
                [
                    f"Question types covered: {', '.join(plan.get('question_types_covered', [])) or 'none'}.",
                    f"Artifact path: {state.get('learning_assessment_plan_artifact_path', 'not saved')}.",
                ],
            )

        if stage_id == "resolve_skill_assessment_requirements":
            requirements = state.get("skill_assessment_requirements", {}) or {}
            return (
                "Resolved external skill-assessment requirements for alignment.",
                [
                    f"Question types required: {', '.join(requirements.get('question_types', [])) or 'none'}.",
                    f"Cadence: every {requirements.get('skill_assessment_every_n_topics', 'unknown')} topics.",
                    f"Signal sync status: {requirements.get('signal_sync_status', 'unknown')}.",
                    f"Artifact path: {state.get('skill_assessment_requirements_artifact_path', 'not saved')}.",
                ],
            )

        if stage_id == "align_learning_with_skill_assessments":
            report = state.get("assessment_alignment_report", {}) or {}
            return (
                f"Computed learning-to-skill assessment alignment: {report.get('overall_status', 'unknown')}.",
                [
                    f"Question type alignment: {report.get('question_type_alignment', {}).get('status', 'unknown')}.",
                    f"Difficulty alignment: {report.get('difficulty_alignment', {}).get('status', 'unknown')}.",
                    f"Concept coverage alignment: {report.get('concept_coverage_alignment', {}).get('status', 'unknown')}.",
                    f"Pattern alignment: {report.get('pattern_alignment', {}).get('status', 'unknown')}.",
                    f"Cadence alignment: {report.get('cadence_alignment', {}).get('status', 'unknown')}.",
                    f"Artifact path: {state.get('assessment_alignment_report_artifact_path', 'not saved')}.",
                ],
            )

        return ("Loop B stage complete.", [f"Updated keys: {', '.join(sorted(updates.keys()))}."])

    @staticmethod
    def _render_review_packet_markdown(packet: dict[str, Any]) -> str:
        lines = [
            f"# Review Packet: {packet['loop_id']} / {packet['stage_id']}",
            "",
            f"- Domain: `{packet['domain']}`",
            f"- Cycle ID: `{packet['cycle_id']}`",
            f"- Next Stage: `{packet['next_stage_id'] or 'complete'}`",
            "",
            "## Summary",
            packet.get("summary", "No summary."),
            "",
            "## Key Decisions",
        ]
        for item in packet.get("key_decisions", []):
            lines.append(f"- {item}")
        return "\n".join(lines) + "\n"

    @classmethod
    def _to_jsonable(cls, value: Any) -> Any:
        if isinstance(value, BaseModel):
            return {key: cls._to_jsonable(item) for key, item in value.model_dump().items()}
        if isinstance(value, dict):
            return {key: cls._to_jsonable(item) for key, item in value.items()}
        if isinstance(value, list):
            return [cls._to_jsonable(item) for item in value]
        return value
