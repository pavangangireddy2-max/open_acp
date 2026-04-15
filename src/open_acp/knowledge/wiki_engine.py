"""WikiEngine — LLM-maintained markdown wiki with confidence scoring.

Tracked canonical knowledge lives in manifests and raw inputs.
Generated wiki state is a runtime artifact and defaults to storage/wiki.
"""
from datetime import datetime, UTC
from pathlib import Path
from typing import Optional


def _find_project_root() -> Path:
    current = Path(__file__).resolve()
    for ancestor in current.parents:
        if (ancestor / "pyproject.toml").exists():
            return ancestor
    return current.parents[3]


class WikiEngine:
    """Manages a persistent, LLM-curated intelligence wiki."""

    ENTITY_TYPES = ["skill", "competitor", "audience_segment", "concept", "domain"]

    def __init__(self, wiki_dir: Optional[str] = None):
        if wiki_dir:
            self.wiki_dir = Path(wiki_dir)
        else:
            self.wiki_dir = _find_project_root() / "storage" / "wiki"
        self.entities_dir = self.wiki_dir / "entities"
        self.concepts_dir = self.wiki_dir / "concepts"
        self.synthesis_dir = self.wiki_dir / "synthesis"

        # Ensure directories exist
        for d in [self.entities_dir, self.concepts_dir, self.synthesis_dir]:
            d.mkdir(parents=True, exist_ok=True)

    # ── CRUD Operations ────────────────────────────────────────────────

    def create_entity(
        self,
        entity_type: str,
        entity_id: str,
        title: str,
        content: str,
        confidence: float = 0.5,
        sources: list[str] = None,
        cross_references: list[str] = None,
        durability: str = "unknown",
    ) -> str:
        """Create a new wiki entity page. Returns the file path."""
        if entity_type not in self.ENTITY_TYPES:
            raise ValueError(f"Invalid entity_type: {entity_type}. Must be one of {self.ENTITY_TYPES}")

        filepath = self.entities_dir / f"{entity_type}_{entity_id}.md"

        # Build frontmatter
        frontmatter = {
            "entity_id": entity_id,
            "entity_type": entity_type,
            "title": title,
            "confidence": confidence,
            "durability": durability,
            "sources": sources or [],
            "cross_references": cross_references or [],
            "created_at": datetime.now(UTC).isoformat(),
            "updated_at": datetime.now(UTC).isoformat(),
        }

        # Write markdown with YAML frontmatter
        md_content = self._format_entity_page(frontmatter, content)
        filepath.write_text(md_content, encoding="utf-8")

        # Log the creation
        self._append_log(f"create | {entity_type}/{entity_id} | {title} | confidence={confidence}")

        return str(filepath)

    def update_entity(
        self,
        entity_id: str,
        entity_type: str,
        content_delta: str,
        reason: str,
        new_confidence: Optional[float] = None,
        new_sources: Optional[list[str]] = None,
    ) -> bool:
        """Update an existing entity with new information. Returns True if found and updated."""
        filepath = self.entities_dir / f"{entity_type}_{entity_id}.md"
        if not filepath.exists():
            return False

        existing = filepath.read_text(encoding="utf-8")
        frontmatter, body = self._parse_entity_page(existing)

        # Update content
        updated_body = body + f"\n\n---\n\n### Update ({datetime.now(UTC).strftime('%Y-%m-%d')})\n\n{content_delta}\n\n*Reason: {reason}*"

        # Update frontmatter
        frontmatter["updated_at"] = datetime.now(UTC).isoformat()
        if new_confidence is not None:
            frontmatter["confidence"] = new_confidence
        if new_sources:
            existing_sources = frontmatter.get("sources", [])
            frontmatter["sources"] = list(set(existing_sources + new_sources))

        filepath.write_text(self._format_entity_page(frontmatter, updated_body), encoding="utf-8")
        self._append_log(f"update | {entity_type}/{entity_id} | {reason} | confidence={frontmatter['confidence']}")

        return True

    def supersede(
        self,
        old_entity_id: str,
        old_entity_type: str,
        new_entity_id: str,
        new_entity_type: str,
        reason: str,
    ) -> bool:
        """Mark an entity as superseded by a new one."""
        old_path = self.entities_dir / f"{old_entity_type}_{old_entity_id}.md"
        if not old_path.exists():
            return False

        existing = old_path.read_text(encoding="utf-8")
        frontmatter, body = self._parse_entity_page(existing)

        frontmatter["superseded_by"] = f"{new_entity_type}_{new_entity_id}"
        frontmatter["superseded_at"] = datetime.now(UTC).isoformat()
        frontmatter["confidence"] = 0.0  # Superseded entities have zero confidence

        updated_body = body + f"\n\n---\n\n> **SUPERSEDED** by [{new_entity_type}/{new_entity_id}](entities/{new_entity_type}_{new_entity_id}.md) — {reason}"

        old_path.write_text(self._format_entity_page(frontmatter, updated_body), encoding="utf-8")
        self._append_log(f"supersede | {old_entity_type}/{old_entity_id} → {new_entity_type}/{new_entity_id} | {reason}")

        return True

    def get_entity(self, entity_type: str, entity_id: str) -> Optional[dict]:
        """Read an entity and return its frontmatter + content."""
        filepath = self.entities_dir / f"{entity_type}_{entity_id}.md"
        if not filepath.exists():
            return None

        text = filepath.read_text(encoding="utf-8")
        frontmatter, body = self._parse_entity_page(text)
        return {"frontmatter": frontmatter, "content": body, "path": str(filepath)}

    def list_entities(self, entity_type: Optional[str] = None) -> list[dict]:
        """List all entities, optionally filtered by type."""
        entities = []
        for filepath in sorted(self.entities_dir.glob("*.md")):
            text = filepath.read_text(encoding="utf-8")
            frontmatter, _ = self._parse_entity_page(text)
            if entity_type and frontmatter.get("entity_type") != entity_type:
                continue
            entities.append({
                "entity_id": frontmatter.get("entity_id", filepath.stem),
                "entity_type": frontmatter.get("entity_type", "unknown"),
                "title": frontmatter.get("title", filepath.stem),
                "confidence": frontmatter.get("confidence", 0.0),
                "durability": frontmatter.get("durability", "unknown"),
                "path": str(filepath),
            })
        return entities

    # ── Search ─────────────────────────────────────────────────────────

    def search(self, query: str, entity_type: Optional[str] = None) -> list[dict]:
        """BM25-style keyword search across wiki entities.

        Simple implementation: scores entities by keyword match frequency.
        """
        query_terms = query.lower().split()
        results = []

        glob_pattern = f"{entity_type}_*.md" if entity_type else "*.md"

        for filepath in self.entities_dir.glob(glob_pattern):
            text = filepath.read_text(encoding="utf-8").lower()
            frontmatter, body = self._parse_entity_page(filepath.read_text(encoding="utf-8"))

            # Simple scoring: count query term occurrences
            score = sum(text.count(term) for term in query_terms)
            if score > 0:
                results.append({
                    "entity_id": frontmatter.get("entity_id", filepath.stem),
                    "entity_type": frontmatter.get("entity_type", "unknown"),
                    "title": frontmatter.get("title", filepath.stem),
                    "score": score,
                    "confidence": frontmatter.get("confidence", 0.0),
                    "path": str(filepath),
                })

        return sorted(results, key=lambda x: x["score"], reverse=True)

    # ── Index & Log ────────────────────────────────────────────────────

    def rebuild_index(self) -> str:
        """Regenerate index.md from all entities."""
        entities = self.list_entities()

        lines = ["# Wiki Index\n"]
        lines.append(f"*Last rebuilt: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')}*\n")
        lines.append(f"**Total entities: {len(entities)}**\n")

        # Group by type
        by_type: dict[str, list] = {}
        for e in entities:
            by_type.setdefault(e["entity_type"], []).append(e)

        for etype, ents in sorted(by_type.items()):
            lines.append(f"\n## {etype.replace('_', ' ').title()} ({len(ents)})\n")
            for e in sorted(ents, key=lambda x: x.get("confidence", 0), reverse=True):
                conf = e.get("confidence", 0)
                durability = e.get("durability", "?")
                lines.append(f"- [{e['title']}](entities/{e['entity_type']}_{e['entity_id']}.md) — confidence: {conf:.2f}, durability: {durability}")

        index_content = "\n".join(lines) + "\n"
        index_path = self.wiki_dir / "index.md"
        index_path.write_text(index_content, encoding="utf-8")

        return index_content

    def get_index(self) -> str:
        """Read the current index.md."""
        index_path = self.wiki_dir / "index.md"
        if index_path.exists():
            return index_path.read_text(encoding="utf-8")
        return ""

    def get_log(self, last_n: int = 50) -> str:
        """Read the last N entries from log.md."""
        log_path = self.wiki_dir / "log.md"
        if not log_path.exists():
            return ""
        lines = log_path.read_text(encoding="utf-8").strip().split("\n")
        return "\n".join(lines[-last_n:])

    # ── Lint ───────────────────────────────────────────────────────────

    def lint(self) -> list[dict]:
        """Health-check the wiki. Returns a list of issues found."""
        issues = []
        entities = self.list_entities()

        for e in entities:
            # Low confidence
            if e["confidence"] < 0.3:
                issues.append({
                    "type": "low_confidence",
                    "entity_id": e["entity_id"],
                    "entity_type": e["entity_type"],
                    "detail": f"Confidence {e['confidence']:.2f} is below 0.3 threshold",
                    "severity": "warning",
                })

            # Check for broken cross-references
            entity_data = self.get_entity(e["entity_type"], e["entity_id"])
            if entity_data:
                fm = entity_data["frontmatter"]
                for ref in fm.get("cross_references", []):
                    # Check if referenced entity exists
                    ref_parts = ref.split("_", 1)
                    if len(ref_parts) == 2:
                        ref_path = self.entities_dir / f"{ref}.md"
                        if not ref_path.exists():
                            issues.append({
                                "type": "broken_cross_reference",
                                "entity_id": e["entity_id"],
                                "detail": f"Cross-reference to '{ref}' not found",
                                "severity": "error",
                            })

        # Check for orphan entities (no cross-references from others)
        all_refs = set()
        for e in entities:
            entity_data = self.get_entity(e["entity_type"], e["entity_id"])
            if entity_data:
                for ref in entity_data["frontmatter"].get("cross_references", []):
                    all_refs.add(ref)

        for e in entities:
            full_id = f"{e['entity_type']}_{e['entity_id']}"
            if full_id not in all_refs and len(entities) > 1:
                issues.append({
                    "type": "orphan_entity",
                    "entity_id": e["entity_id"],
                    "entity_type": e["entity_type"],
                    "detail": "No other entity references this one",
                    "severity": "info",
                })

        return issues

    # ── Crystallization ────────────────────────────────────────────────

    def crystallize(self, cycle_id: str, report: dict) -> str:
        """Convert a Loop D cycle report into a wiki synthesis entry."""
        filepath = self.synthesis_dir / f"cycle_{cycle_id}.md"

        lines = [f"# Cycle Report: {cycle_id}\n"]
        lines.append(f"*Generated: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')}*\n")

        if "health_scores" in report:
            lines.append("## Health Scores\n")
            for score in report["health_scores"]:
                lines.append(f"- {score}")

        if "fix_routes" in report:
            lines.append("\n## Fixes Applied\n")
            for fix in report["fix_routes"]:
                lines.append(f"- {fix}")

        if "insights" in report:
            lines.append("\n## Key Insights\n")
            for insight in report["insights"]:
                lines.append(f"- {insight}")

        if "lessons_learned" in report:
            lines.append("\n## Lessons Learned\n")
            for lesson in report["lessons_learned"]:
                lines.append(f"- {lesson}")

        content = "\n".join(lines) + "\n"
        filepath.write_text(content, encoding="utf-8")
        self._append_log(f"crystallize | cycle_{cycle_id} | synthesis entry created")

        return str(filepath)

    # ── Internal Helpers ───────────────────────────────────────────────

    def _append_log(self, entry: str) -> None:
        """Append an entry to log.md."""
        log_path = self.wiki_dir / "log.md"
        timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M")

        # Create log file with header if it doesn't exist
        if not log_path.exists():
            log_path.write_text("# Wiki Change Log\n\n", encoding="utf-8")

        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {entry}\n")

    def _format_entity_page(self, frontmatter: dict, body: str) -> str:
        """Format an entity page with YAML-like frontmatter."""
        fm_lines = ["---"]
        for key, value in frontmatter.items():
            if isinstance(value, list):
                fm_lines.append(f"{key}:")
                for item in value:
                    fm_lines.append(f"  - {item}")
            elif isinstance(value, (int, float)):
                fm_lines.append(f"{key}: {value}")
            else:
                fm_lines.append(f'{key}: "{value}"')
        fm_lines.append("---\n")
        return "\n".join(fm_lines) + "\n" + body

    def _parse_entity_page(self, text: str) -> tuple[dict, str]:
        """Parse YAML-like frontmatter from a markdown page."""
        if not text.startswith("---"):
            return {}, text

        # Find the closing ---
        end_idx = text.index("---", 3)
        fm_text = text[4:end_idx].strip()
        body = text[end_idx + 4:].strip()

        # Simple YAML-like parsing
        frontmatter = {}
        current_key = None
        current_list = None

        for line in fm_text.split("\n"):
            line = line.strip()
            if not line:
                continue

            if line.startswith("- ") and current_key:
                # List item
                if current_list is None:
                    current_list = []
                current_list.append(line[2:].strip().strip('"'))
                frontmatter[current_key] = current_list
            elif ":" in line:
                # Save previous list
                if current_list is not None:
                    current_list = None

                key, _, value = line.partition(":")
                key = key.strip()
                value = value.strip().strip('"')
                current_key = key

                if value:
                    # Try to parse as number
                    try:
                        if "." in value:
                            frontmatter[key] = float(value)
                        else:
                            frontmatter[key] = int(value)
                    except ValueError:
                        frontmatter[key] = value
                else:
                    # Empty value — might be a list header
                    frontmatter[key] = []
                    current_list = frontmatter[key]

        return frontmatter, body
