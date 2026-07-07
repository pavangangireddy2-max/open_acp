"""Uniform raw-item shape emitted by all D11a ingestors.

Every D11a ingestor (RSS, scrape, X, YouTube) normalizes its source-specific
payload into `RawItem`. The next slice (classifier + signal contract) consumes
RawItem rather than per-source shapes, so adding a new ingestor only requires
producing valid RawItem instances.

Design notes:
- `source_family` matches the keys in the curated source manifest
  (org_blogs, curated_x_accounts, youtube_channels, ...).
- `ingestion_mode` records how this item was fetched (rss/scrape/x).
- `published_at` is ISO-8601 string when the upstream feed provides it; left as
  None when unknown rather than guessed.
- `x_signal_types` is carried through verbatim from the curated tag and used by
  the digest reducer for dimension weighting.
- `raw_payload` keeps the source-specific dict for debugging and re-extraction
  without forcing a wider schema today.
"""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field

from open_acp.channels.d11a.sources import IngestionMode, XSignalType


class RawItem(BaseModel):
    item_id: str
    source_family: str
    source_label: str
    source_url: str
    ingestion_mode: IngestionMode
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    item_url: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[str] = None
    fetched_at: str
    x_signal_types: list[XSignalType] = Field(default_factory=list)
    raw_payload: dict[str, Any] = Field(default_factory=dict)
