"""Deterministic coverage policy engine for Loop B.

Applies C/L tag-based coverage policies to stack curriculum abstracts,
selecting eligible modules and tracking what was dropped and why.
"""
from __future__ import annotations

from typing import Any


def apply_coverage_policy(
    abstract: dict,
    include_tags: list[str] | None = None,
    include_levels: list[str] | None = None,
) -> dict:
    """Filter an abstract's module catalog by coverage policy.

    Args:
        abstract: A StackCurriculumAbstract dict with a 'modules' list.
        include_tags: C-tags to include (e.g. ["C1", "C2"]). None means all.
        include_levels: L-tags to include (e.g. ["L1", "L2"]). None means all.

    Returns:
        Dict with 'selected', 'dropped', and 'selected_cells' keys.
    """
    modules = abstract.get("modules", []) or []
    selected: list[dict] = []
    dropped: list[dict] = []

    for mod in modules:
        tags = mod.get("tags", []) or []
        c_tag = next((t for t in tags if t.startswith("C")), None)
        l_tag = next((t for t in tags if t.startswith("L")), None)

        c_ok = include_tags is None or c_tag in include_tags
        l_ok = include_levels is None or l_tag in include_levels

        if c_ok and l_ok:
            selected.append(mod)
        else:
            reason_parts = []
            if not c_ok:
                reason_parts.append(f"{c_tag} outside coverage tags {include_tags}")
            if not l_ok:
                reason_parts.append(f"{l_tag} outside coverage levels {include_levels}")
            dropped.append({
                "stack": abstract.get("stack_id", "unknown"),
                "module": mod.get("module_id", "unknown"),
                "reason": "; ".join(reason_parts),
            })

    # Compute which C x L cells were selected
    selected_cells: list[str] = []
    for mod in selected:
        tags = mod.get("tags", []) or []
        c_tag = next((t for t in tags if t.startswith("C")), None)
        l_tag = next((t for t in tags if t.startswith("L")), None)
        if c_tag and l_tag:
            cell = f"{c_tag}_{l_tag}"
            if cell not in selected_cells:
                selected_cells.append(cell)

    return {
        "selected": selected,
        "dropped": dropped,
        "selected_cells": selected_cells,
    }


def verify_cross_stack_prerequisites(
    selected_modules: list[dict],
    available_abstracts: dict[str, dict],
) -> dict:
    """Check that cross-stack prerequisite skills are satisfiable.

    Args:
        selected_modules: Flat list of selected AbstractModule dicts across all stacks.
        available_abstracts: Map of stack_id -> StackCurriculumAbstract dict.

    Returns:
        Dict with 'verified' bool, 'checks' list, and 'unmet' list.
    """
    # Build a set of all skill_ids provided by selected modules
    provided_skills: set[str] = set()
    for mod in selected_modules:
        for skill_id in mod.get("skill_ids", []) or []:
            provided_skills.add(skill_id)

    checks: list[str] = []
    unmet: list[str] = []

    for stack_id, abstract in available_abstracts.items():
        for prereq in abstract.get("external_prerequisites", []) or []:
            from_stack = prereq.get("from_stack", "")
            required_skills = prereq.get("required_skill_ids", []) or []
            kind = prereq.get("kind", "hard_prereq")

            for skill_id in required_skills:
                if skill_id in provided_skills:
                    checks.append(
                        f"{stack_id} needs {skill_id} from {from_stack}: satisfied"
                    )
                else:
                    msg = f"{stack_id} needs {skill_id} from {from_stack}: NOT satisfied ({kind})"
                    checks.append(msg)
                    if kind == "hard_prereq":
                        unmet.append(msg)

    return {
        "verified": len(unmet) == 0,
        "checks": checks,
        "unmet": unmet,
    }
