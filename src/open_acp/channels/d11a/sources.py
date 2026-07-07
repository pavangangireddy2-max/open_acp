"""Pydantic models + loader for the D11a curated source manifest.

The manifest lives at:
    knowledge/manifests/source_families/dimension_11a_curated_market_genai.yaml

It groups curated GenAI sources into source families (org_blogs, curated_x_accounts,
youtube_channels, podcasts, newsletters, leaderboards_benchmarks, competitor_courses,
product_launches, longform_blogs, certifications, community_links, instagram).

Each entry declares an ingestion mode:
    - rss      : has a discoverable feed URL (slice 1 target)
    - scrape   : needs bespoke HTML extraction (slice 3 target)
    - x        : requires X API or login flow (slice 4 target)
    - deferred : out of scope for v1 (D11b community chatter etc.)

`x_signal_types` carries the curated tag from the original URL list and feeds
the digest reducer for dimension weighting (Research / News / Tools / etc.).
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Literal, Optional

from pydantic import BaseModel, Field, model_validator

from open_acp.config.curriculum_context import find_project_root, load_yaml

IngestionMode = Literal["rss", "scrape", "x", "deferred"]

XSignalType = Literal[
    "Research",
    "ResearchPapers",
    "News",
    "SystemDesign",
    "Tools",
    "ModelAnalysis",
    "OpenSource",
    "Tips",
    "Prompting",
    "Evaluation",
    "PersonalisedLearning",
    "Founders",
    "LearningResources",
]


class SourceEntry(BaseModel):
    """One curated source. `name` and `handle` are interchangeable shapes from the YAML."""

    name: Optional[str] = None
    handle: Optional[str] = None
    description: Optional[str] = None
    url: str
    rss: Optional[str] = None
    ingestion: IngestionMode
    x_signal_types: list[XSignalType] = Field(default_factory=list)
    note: Optional[str] = None

    @model_validator(mode="after")
    def _ensure_label(self) -> "SourceEntry":
        if not self.name and not self.handle and not self.description:
            raise ValueError("SourceEntry needs at least one of name/handle/description")
        return self

    @property
    def label(self) -> str:
        return self.name or (f"@{self.handle}" if self.handle else self.description or self.url)


class CadencePolicy(BaseModel):
    rss: str = "daily"
    x: str = "every_3_days"
    youtube: str = "every_3_days"
    leaderboards: str = "weekly"
    scraped: str = "weekly"


class CuratedSourceManifest(BaseModel):
    """The full D11a curated source manifest grouped by source family."""

    version: int = 1
    manifest_id: str
    description: Optional[str] = None
    cadence_policy: CadencePolicy = Field(default_factory=CadencePolicy)
    sources: dict[str, list[SourceEntry]] = Field(default_factory=dict)
    notes: list[str] = Field(default_factory=list)
    manifest_path: Optional[str] = None

    def all_entries(self) -> Iterable[SourceEntry]:
        for entries in self.sources.values():
            yield from entries

    def entries_for_family(self, family: str) -> list[SourceEntry]:
        return list(self.sources.get(family, []))

    def entries_with_ingestion(self, mode: IngestionMode) -> list[SourceEntry]:
        return [entry for entry in self.all_entries() if entry.ingestion == mode]

    def rss_entries(self) -> list[SourceEntry]:
        """All entries that declare an RSS feed URL (regardless of ingestion mode)."""
        return [entry for entry in self.all_entries() if entry.rss]

    def family_ids(self) -> list[str]:
        return list(self.sources.keys())


def curated_market_manifest_path() -> Path:
    return (
        find_project_root()
        / "knowledge"
        / "manifests"
        / "source_families"
        / "dimension_11a_curated_market_genai.yaml"
    )


def load_curated_market_manifest(path: Optional[Path] = None) -> CuratedSourceManifest:
    manifest_path = path or curated_market_manifest_path()
    data = load_yaml(manifest_path)
    if not data:
        raise FileNotFoundError(f"Curated market manifest not found at {manifest_path}")
    data["manifest_path"] = str(manifest_path)
    return CuratedSourceManifest.model_validate(data)
