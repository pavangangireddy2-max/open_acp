from open_acp.styles.style_loader import StyleLoader


def test_style_loader_composes_first_wave_layers():
    loader = StyleLoader()
    composed = loader.load_for_pipeline(content_type="concept_explainer", domain="cpp")

    assert "pedagogy_core" in composed
    assert "pedagogy_profile" in composed
    assert "format" in composed
    assert "brand" in composed
    assert "domain" in composed
    assert composed["pedagogy_profile"]["profile_id"] == "worked_example_scaffold"


def test_project_building_uses_project_session_format():
    loader = StyleLoader()
    composed = loader.load_for_pipeline(content_type="project_building", domain="genai")

    assert composed["format"]["format"] == "project_session"
    assert composed["pedagogy_profile"]["profile_id"] == "project_build_along"


def test_style_loader_text_includes_profile_and_brand_sections():
    loader = StyleLoader()
    text = loader.load_for_pipeline_as_text(content_type="concept_explainer", domain="genai")

    assert "Resolved Pedagogy Profile" in text
    assert "Brand Guidelines" in text
    assert "Format Guidelines" in text
