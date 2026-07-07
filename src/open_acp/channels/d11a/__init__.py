"""D11a — Curated Market & Tech Intelligence (GenAI stack) ingestion package.

This package collects ingestors for the curated source list defined in
`knowledge/manifests/source_families/dimension_11a_curated_market_genai.yaml`.

Slice 1 covers the manifest loader, the RawItem model, and the RSS/Atom ingestor.
Later slices add YouTube/leaderboard/Product Hunt scrapers, an X ingestor, and
the trend aggregator that emits Loop D signals.
"""

from open_acp.channels.d11a.raw_item import RawItem
from open_acp.channels.d11a.rss_ingestor import RSSFetchError, fetch_rss_entries, ingest_rss_sources
from open_acp.channels.d11a.sources import (
    CadencePolicy,
    CuratedSourceManifest,
    IngestionMode,
    SourceEntry,
    XSignalType,
    load_curated_market_manifest,
)

__all__ = [
    "CadencePolicy",
    "CuratedSourceManifest",
    "IngestionMode",
    "RSSFetchError",
    "RawItem",
    "SourceEntry",
    "XSignalType",
    "fetch_rss_entries",
    "ingest_rss_sources",
    "load_curated_market_manifest",
]
