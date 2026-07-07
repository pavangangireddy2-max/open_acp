"""RSS / Atom ingestor for D11a curated sources.

Parses RSS 2.0 and Atom 1.0 feeds with stdlib `xml.etree.ElementTree` and
fetches over HTTP with `httpx`. Entries are normalized into RawItem.

Why stdlib parser instead of feedparser:
- We only need title/link/summary/published per entry.
- Avoids adding another dep to pyproject.toml.
- xml.etree handles the two namespaces we care about (Atom + RSS dc:date).

The fetcher is split from the parser so unit tests can exercise parsing on
fixture XML without network calls. `ingest_rss_sources` is the public entry
point that walks the manifest and yields RawItem batches.
"""

from __future__ import annotations

import hashlib
import logging
from datetime import datetime, timezone
from typing import Iterable, Optional
from xml.etree import ElementTree as ET

import httpx

from open_acp.channels.d11a.raw_item import RawItem
from open_acp.channels.d11a.sources import (
    CuratedSourceManifest,
    SourceEntry,
    load_curated_market_manifest,
)

logger = logging.getLogger(__name__)

# Atom namespace; RSS 2.0 has no default namespace.
_ATOM_NS = "{http://www.w3.org/2005/Atom}"
_DC_NS = "{http://purl.org/dc/elements/1.1/}"
_CONTENT_NS = "{http://purl.org/rss/1.0/modules/content/}"

DEFAULT_TIMEOUT_SECONDS = 20.0
DEFAULT_USER_AGENT = "open_acp-d11a-rss/0.1 (+https://github.com/nxtwave/open_acp)"


class RSSFetchError(RuntimeError):
    """Raised when an RSS feed cannot be fetched. Parse errors are reported separately."""


def _hash_id(*parts: str) -> str:
    digest = hashlib.sha1("␟".join(p or "" for p in parts).encode("utf-8")).hexdigest()
    return digest[:16]


def _text(node: Optional[ET.Element]) -> Optional[str]:
    if node is None or node.text is None:
        return None
    text = node.text.strip()
    return text or None


def _atom_link_href(entry: ET.Element) -> Optional[str]:
    # Prefer rel="alternate"; fall back to first link.
    alternate: Optional[str] = None
    first: Optional[str] = None
    for link in entry.findall(f"{_ATOM_NS}link"):
        href = link.get("href")
        if not href:
            continue
        if first is None:
            first = href
        if (link.get("rel") or "alternate") == "alternate":
            alternate = href
            break
    return alternate or first


def parse_feed(xml_text: str) -> list[dict[str, Optional[str]]]:
    """Parse an RSS 2.0 or Atom 1.0 feed into a list of normalized entry dicts.

    Returns dicts with keys: title, link, summary, author, published.
    Raises ET.ParseError on malformed XML; callers handle that.
    """
    root = ET.fromstring(xml_text)

    # Atom feeds have <feed> as root with the Atom namespace.
    if root.tag == f"{_ATOM_NS}feed":
        return [_atom_entry(e) for e in root.findall(f"{_ATOM_NS}entry")]

    # RSS 2.0 feeds: <rss><channel><item>...
    channel = root.find("channel")
    if channel is None and root.tag == "channel":
        channel = root
    if channel is None:
        return []
    return [_rss_item(item) for item in channel.findall("item")]


def _atom_entry(entry: ET.Element) -> dict[str, Optional[str]]:
    title = _text(entry.find(f"{_ATOM_NS}title"))
    summary = _text(entry.find(f"{_ATOM_NS}summary")) or _text(entry.find(f"{_ATOM_NS}content"))
    author_node = entry.find(f"{_ATOM_NS}author/{_ATOM_NS}name")
    author = _text(author_node)
    published = _text(entry.find(f"{_ATOM_NS}published")) or _text(entry.find(f"{_ATOM_NS}updated"))
    return {
        "title": title,
        "link": _atom_link_href(entry),
        "summary": summary,
        "author": author,
        "published": published,
    }


def _rss_item(item: ET.Element) -> dict[str, Optional[str]]:
    title = _text(item.find("title"))
    link = _text(item.find("link"))
    summary = _text(item.find("description")) or _text(item.find(f"{_CONTENT_NS}encoded"))
    author = _text(item.find("author")) or _text(item.find(f"{_DC_NS}creator"))
    published = _text(item.find("pubDate")) or _text(item.find(f"{_DC_NS}date"))
    return {
        "title": title,
        "link": link,
        "summary": summary,
        "author": author,
        "published": published,
    }


def fetch_feed_xml(
    url: str,
    *,
    client: Optional[httpx.Client] = None,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    user_agent: str = DEFAULT_USER_AGENT,
) -> str:
    """Fetch an RSS/Atom feed body. Raises RSSFetchError on HTTP/network failure."""
    headers = {"User-Agent": user_agent, "Accept": "application/rss+xml, application/atom+xml, application/xml;q=0.9, */*;q=0.8"}
    try:
        if client is None:
            response = httpx.get(url, headers=headers, timeout=timeout, follow_redirects=True)
        else:
            response = client.get(url, headers=headers, timeout=timeout, follow_redirects=True)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise RSSFetchError(f"Failed to fetch {url}: {exc}") from exc
    return response.text


def fetch_rss_entries(
    entry: SourceEntry,
    *,
    source_family: str,
    client: Optional[httpx.Client] = None,
    fetched_at: Optional[str] = None,
) -> list[RawItem]:
    """Fetch and parse one curated source's feed, returning a list of RawItem.

    Returns an empty list if the entry has no `rss` URL. RSSFetchError is raised
    on transport failure; XML parse errors are caught and logged so a single
    bad feed does not abort an entire ingestion run.
    """
    if not entry.rss:
        return []

    timestamp = fetched_at or datetime.now(timezone.utc).isoformat()
    xml_text = fetch_feed_xml(entry.rss, client=client)
    try:
        parsed_entries = parse_feed(xml_text)
    except ET.ParseError as exc:
        logger.warning("RSS parse failed for %s (%s): %s", entry.label, entry.rss, exc)
        return []

    items: list[RawItem] = []
    for parsed in parsed_entries:
        link = parsed.get("link") or entry.rss
        item_id = _hash_id(source_family, entry.label, link, parsed.get("title") or "")
        items.append(
            RawItem(
                item_id=item_id,
                source_family=source_family,
                source_label=entry.label,
                source_url=entry.url,
                ingestion_mode=entry.ingestion,
                title=parsed.get("title"),
                summary=parsed.get("summary"),
                content=None,
                item_url=link,
                author=parsed.get("author"),
                published_at=parsed.get("published"),
                fetched_at=timestamp,
                x_signal_types=entry.x_signal_types,
                raw_payload={"feed_url": entry.rss, **{k: v for k, v in parsed.items() if v is not None}},
            )
        )
    return items


def ingest_rss_sources(
    manifest: Optional[CuratedSourceManifest] = None,
    *,
    client: Optional[httpx.Client] = None,
    fetched_at: Optional[str] = None,
    skip_on_error: bool = True,
) -> Iterable[RawItem]:
    """Walk every entry with an `rss` URL and yield RawItem instances.

    Caller is responsible for batching/persisting. `skip_on_error=True` lets
    a single broken feed be logged and skipped without aborting the run; set
    to False to surface the first RSSFetchError immediately (useful in tests).
    """
    manifest = manifest or load_curated_market_manifest()
    for family_id, entries in manifest.sources.items():
        for entry in entries:
            if not entry.rss:
                continue
            try:
                yield from fetch_rss_entries(
                    entry,
                    source_family=family_id,
                    client=client,
                    fetched_at=fetched_at,
                )
            except RSSFetchError as exc:
                if not skip_on_error:
                    raise
                logger.warning("Skipping %s/%s: %s", family_id, entry.label, exc)
