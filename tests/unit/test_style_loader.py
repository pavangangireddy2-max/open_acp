from open_acp.styles.style_loader import StyleLoader


def test_style_loader_defaults_to_root_guidance_dir():
    loader = StyleLoader()
    assert loader.base_dir.name == "guidance"
    assert loader.base_dir.exists()


def test_style_loader_composes_first_wave_layers():
    loader = StyleLoader()
    composed = loader.load_for_pipeline(content_type="concept_explainer", domain="cpp")

    assert "pedagogy_core" in composed
    assert "pedagogy_profile" in composed
    assert "guidance_contract" in composed
    assert "learning_unit_type" in composed
    assert "presentation_surface" in composed
    assert "instructional_pattern" in composed
    assert "teaching_mode_contract" in composed
    assert "brand" in composed
    assert "stack" in composed
    assert composed["pedagogy_profile"]["profile_id"] == "worked_example_scaffold"
    assert composed["guidance_contract"]["learning_unit_type"] == "video_session_unit"
    assert composed["guidance_contract"]["presentation_surface"] == "slide_backed_session"
    assert composed["guidance_contract"]["instructional_pattern"] == "concept_explainer"
    assert composed["teaching_mode_contract"]["resolved_sequence"] == [
        "prior_knowledge_bridge",
        "concept_explain",
        "worked_example",
        "guided_practice",
        "reflection_summary",
    ]


def test_project_building_uses_project_guidance_contract():
    loader = StyleLoader()
    composed = loader.load_for_pipeline(content_type="project_building", domain="genai")

    assert composed["instructional_pattern"]["instructional_pattern"] == "project_building"
    assert composed["presentation_surface"]["presentation_surface"] == "slide_backed_session"
    assert composed["pedagogy_profile"]["profile_id"] == "project_build_along"


def test_platform_walkthrough_prefers_screen_demo_surface():
    loader = StyleLoader()
    composed = loader.load_for_pipeline(content_type="platform_walkthrough", domain="genai")

    assert composed["guidance_contract"]["learning_unit_type"] == "video_session_unit"
    assert composed["guidance_contract"]["presentation_surface"] == "screen_demo_session"
    assert composed["guidance_contract"]["instructional_pattern"] == "platform_walkthrough"


def test_skill_assessment_aliases_resolve_to_shared_assessment_guidance():
    loader = StyleLoader()

    skill = loader.resolve_guidance_contract(content_type="skill_assessment")
    legacy_skill = loader.resolve_guidance_contract(content_type="fortnight_quiz")
    graded = loader.resolve_guidance_contract(content_type="graded_assessment")

    assert skill["learning_unit_type"] == "skill_assessment_unit"
    assert skill["presentation_surface"] == "assessment_portal_surface"
    assert legacy_skill["learning_unit_type"] == "skill_assessment_unit"
    assert graded["learning_unit_type"] == "graded_assessment_unit"


def test_style_loader_text_includes_profile_and_brand_sections():
    loader = StyleLoader()
    text = loader.load_for_pipeline_as_text(content_type="concept_explainer", domain="genai")

    assert "Guidance Contract" in text
    assert "Resolved Pedagogy Profile" in text
    assert "Teaching Mode Contract" in text
    assert "Learning Unit Type Guidance" in text
    assert "Presentation Surface Guidance" in text
    assert "Instructional Pattern Guidance" in text
    assert "Stack Guidance" in text
    assert "Brand Guidelines" in text
