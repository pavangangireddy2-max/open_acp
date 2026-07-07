"""Echo corpus registry.

Enumerates the intelligence sources Echo can read and answer from. Each ``Source``
is a whole file (Echo does document-selection, not chunk search — see the design doc
§2). The registry is built by scanning known directories at call time, so newly-added
handoff docs / manifests / analyses appear automatically without editing this file.

Scope (confirmed 2026-07-08): handoff docs + manifests + pedagogy YAML +
docs/architecture + raw sources (extracted deck text + corpora CSVs). Raw PDF binaries
are NOT included — Echo reads the ``extracted_text/*.txt`` versions instead.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from open_acp.config.curriculum_context import find_project_root

# Roughly 4 chars per token; used only for budgeting/telemetry, not correctness.
_CHARS_PER_TOKEN = 4

# File extensions Echo can read as text. PDFs/binaries are deliberately excluded.
_TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".txt", ".csv"}


@dataclass(frozen=True)
class Source:
    """One readable intelligence file."""

    key: str  # repo-relative path, the stable citation id
    path: Path
    category: str  # handoff | pedagogy | manifest | architecture | raw
    description: str  # one line, shown to the selection step

    @property
    def approx_tokens(self) -> int:
        try:
            return self.path.stat().st_size // _CHARS_PER_TOKEN
        except OSError:
            return 0


# (repo-relative dir, category, recursive, one-line description of the group).
# Order sets rough priority when presenting the manifest to the selector.
_SCAN_SPECS: tuple[tuple[str, str, bool, str], ...] = (
    ("docs/handoff", "handoff", True, "Handoff intelligence docs (products, pedagogy, question intelligence, platform, agent-family architecture, proposals, reviews, specs)"),
    ("knowledge/analyses/pedagogy", "pedagogy", True, "Universal pedagogy principles (mined from brand decks)"),
    ("knowledge/analyses/style", "pedagogy", True, "Per-deck style analyses (cpp/genai/react)"),
    ("knowledge/manifests", "manifest", True, "Domain / stack / track / product / channel / source-family manifests"),
    ("docs/architecture", "architecture", True, "Internal architecture design docs"),
    ("knowledge/raw/brand/extracted_text", "raw", True, "Raw extracted text from brand session decks"),
    ("knowledge/raw/corpora", "raw", True, "Raw corpora (Central Stack Catalogue, course inputs)"),
)

# Files that add noise without answering questions.
_EXCLUDE_NAMES = {"__init__.py"}


def _describe(path: Path, group_description: str, root: Path) -> str:
    """Best-effort one-line description: a doc's first heading, else the group blurb."""
    if path.suffix.lower() == ".md":
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                stripped = line.strip()
                if stripped.startswith("#"):
                    return stripped.lstrip("# ").strip() or group_description
                if stripped:
                    break
        except OSError:
            pass
    return group_description


def list_sources(root: Path | None = None) -> list[Source]:
    """Scan the registered directories and return all readable sources."""
    root = root or find_project_root()
    sources: list[Source] = []
    seen: set[str] = set()

    for rel_dir, category, recursive, group_desc in _SCAN_SPECS:
        base = root / rel_dir
        if not base.exists():
            continue
        paths = base.rglob("*") if recursive else base.glob("*")
        for path in sorted(paths):
            if not path.is_file():
                continue
            if path.suffix.lower() not in _TEXT_SUFFIXES:
                continue
            if path.name in _EXCLUDE_NAMES:
                continue
            key = str(path.relative_to(root))
            if key in seen:
                continue
            seen.add(key)
            sources.append(
                Source(
                    key=key,
                    path=path,
                    category=category,
                    description=_describe(path, group_desc, root),
                )
            )
    return sources


def load_source(source: Source, max_chars: int = 400_000) -> str:
    """Read a source's text, truncating pathologically large files with a marker."""
    try:
        text = source.path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return f"[Echo could not read {source.key}: {exc}]"
    if len(text) > max_chars:
        text = text[:max_chars] + f"\n\n[... truncated at {max_chars} chars for {source.key} ...]"
    return text


def manifest_lines(sources: list[Source]) -> str:
    """Render the source list as a compact manifest for the selection step."""
    return "\n".join(f"- [{s.category}] {s.key} — {s.description}" for s in sources)
