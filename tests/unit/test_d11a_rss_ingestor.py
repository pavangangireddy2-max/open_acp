"""Unit tests for the D11a RSS / Atom parser and fetcher."""

from __future__ import annotations

import httpx
import pytest

from open_acp.channels.d11a.raw_item import RawItem
from open_acp.channels.d11a.rss_ingestor import (
    RSSFetchError,
    fetch_rss_entries,
    parse_feed,
)
from open_acp.channels.d11a.sources import SourceEntry

ATOM_FIXTURE = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Hugging Face Blog</title>
  <updated>2026-04-30T10:00:00Z</updated>
  <entry>
    <title>Open LLMs Quarterly Recap</title>
    <link rel="alternate" href="https://huggingface.co/blog/open-llm-recap" />
    <summary>Roundup of the most-downloaded open models this quarter.</summary>
    <author><name>HF Team</name></author>
    <published>2026-04-29T09:30:00Z</published>
  </entry>
  <entry>
    <title>New Tool: smolagents</title>
    <link href="https://huggingface.co/blog/smolagents" />
    <content type="html">A tiny agent framework for inference endpoints.</content>
    <updated>2026-04-25T12:00:00Z</updated>
  </entry>
</feed>
"""

RSS_FIXTURE = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <channel>
    <title>Microsoft Research Blog</title>
    <link>https://www.microsoft.com/en-us/research/</link>
    <item>
      <title>Phi-5 Released</title>
      <link>https://example.com/phi5</link>
      <description>A new small model from MSR.</description>
      <dc:creator>MSR Team</dc:creator>
      <pubDate>Mon, 28 Apr 2026 14:30:00 GMT</pubDate>
    </item>
  </channel>
</rss>
"""


def test_parse_atom_feed():
    entries = parse_feed(ATOM_FIXTURE)

    assert len(entries) == 2
    first = entries[0]
    assert first["title"] == "Open LLMs Quarterly Recap"
    assert first["link"] == "https://huggingface.co/blog/open-llm-recap"
    assert "most-downloaded" in (first["summary"] or "")
    assert first["author"] == "HF Team"
    assert first["published"] == "2026-04-29T09:30:00Z"

    second = entries[1]
    assert second["title"] == "New Tool: smolagents"
    assert second["link"] == "https://huggingface.co/blog/smolagents"
    # Falls back to <updated> when no <published>
    assert second["published"] == "2026-04-25T12:00:00Z"


def test_parse_rss_feed():
    entries = parse_feed(RSS_FIXTURE)

    assert len(entries) == 1
    item = entries[0]
    assert item["title"] == "Phi-5 Released"
    assert item["link"] == "https://example.com/phi5"
    assert item["author"] == "MSR Team"
    assert item["published"] == "Mon, 28 Apr 2026 14:30:00 GMT"


def test_fetch_rss_entries_uses_mock_transport():
    """fetch_rss_entries should call the supplied client and return RawItems."""

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path.endswith("feed.xml")
        return httpx.Response(200, text=ATOM_FIXTURE)

    transport = httpx.MockTransport(handler)
    with httpx.Client(transport=transport) as client:
        entry = SourceEntry(
            name="Hugging Face Blog",
            url="https://huggingface.co/blog",
            rss="https://huggingface.co/blog/feed.xml",
            ingestion="rss",
        )
        items = fetch_rss_entries(entry, source_family="org_blogs", client=client)

    assert len(items) == 2
    assert all(isinstance(item, RawItem) for item in items)
    first = items[0]
    assert first.source_family == "org_blogs"
    assert first.source_label == "Hugging Face Blog"
    assert first.title == "Open LLMs Quarterly Recap"
    assert first.item_url == "https://huggingface.co/blog/open-llm-recap"
    assert first.ingestion_mode == "rss"
    assert first.published_at == "2026-04-29T09:30:00Z"
    assert first.fetched_at  # always populated

    # item_id is deterministic for stable dedup across runs.
    again_items = []

    def handler2(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text=ATOM_FIXTURE)

    with httpx.Client(transport=httpx.MockTransport(handler2)) as client:
        again_items = fetch_rss_entries(entry, source_family="org_blogs", client=client)
    assert items[0].item_id == again_items[0].item_id


def test_fetch_rss_entries_raises_on_http_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(503, text="upstream down")

    transport = httpx.MockTransport(handler)
    entry = SourceEntry(
        name="Broken Feed",
        url="https://example.com",
        rss="https://example.com/feed.xml",
        ingestion="rss",
    )
    with httpx.Client(transport=transport) as client, pytest.raises(RSSFetchError):
        fetch_rss_entries(entry, source_family="org_blogs", client=client)


def test_fetch_rss_entries_skips_when_no_feed_declared():
    entry = SourceEntry(
        name="Scrape Only",
        url="https://example.com",
        ingestion="scrape",
    )
    assert fetch_rss_entries(entry, source_family="org_blogs") == []


def test_parse_feed_handles_unknown_root_gracefully():
    # Not RSS, not Atom — should return [] rather than raise.
    assert parse_feed("<html><body>not a feed</body></html>") == []
