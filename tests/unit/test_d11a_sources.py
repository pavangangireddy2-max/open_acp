"""Unit tests for the D11a curated source manifest loader."""

from open_acp.channels.d11a import (
    CuratedSourceManifest,
    SourceEntry,
    load_curated_market_manifest,
)
from open_acp.channels.d11a.sources import curated_market_manifest_path


def test_curated_market_manifest_loads():
    manifest = load_curated_market_manifest()

    assert isinstance(manifest, CuratedSourceManifest)
    assert manifest.manifest_id == "dimension_11a_curated_market_genai"
    assert manifest.manifest_path == str(curated_market_manifest_path())
    # Every source family declared in the channel contract should appear here.
    expected_families = {
        "org_blogs",
        "curated_x_accounts",
        "youtube_channels",
        "podcasts",
        "newsletters",
        "leaderboards_benchmarks",
        "competitor_courses",
        "product_launches",
        "longform_blogs",
    }
    assert expected_families.issubset(set(manifest.family_ids()))


def test_cadence_policy_defaults_match_yaml():
    manifest = load_curated_market_manifest()
    assert manifest.cadence_policy.rss == "daily"
    assert manifest.cadence_policy.x == "every_3_days"
    assert manifest.cadence_policy.youtube == "every_3_days"
    assert manifest.cadence_policy.leaderboards == "weekly"


def test_rss_entries_have_feed_urls():
    manifest = load_curated_market_manifest()
    rss_entries = manifest.rss_entries()

    assert len(rss_entries) >= 4, "Expected at least the 4 declared RSS feeds"
    for entry in rss_entries:
        assert entry.rss, f"{entry.label} flagged as RSS but has no feed url"
        assert entry.ingestion == "rss"


def test_x_entries_carry_signal_types():
    manifest = load_curated_market_manifest()
    x_entries = manifest.entries_with_ingestion("x")

    assert any(e.handle == "karpathy" for e in x_entries), "Expected karpathy in curated X accounts"
    karpathy = next(e for e in x_entries if e.handle == "karpathy")
    assert "Founders" in karpathy.x_signal_types


def test_source_entry_label_prefers_name_then_handle():
    name_entry = SourceEntry(name="OpenAI Academy", url="https://example.com", ingestion="scrape")
    handle_entry = SourceEntry(handle="karpathy", url="https://x.com/karpathy", ingestion="x")

    assert name_entry.label == "OpenAI Academy"
    assert handle_entry.label == "@karpathy"


def test_huggingface_blog_is_rss_target():
    manifest = load_curated_market_manifest()
    org_blogs = manifest.entries_for_family("org_blogs")
    hf = next((e for e in org_blogs if e.name == "Hugging Face Blog"), None)

    assert hf is not None
    assert hf.ingestion == "rss"
    assert hf.rss and hf.rss.startswith("https://")
