from open_acp.styles.pedagogy_resolver import PedagogyResolver


def test_resolver_defaults_to_root_guidance_dir():
    resolver = PedagogyResolver()
    assert resolver.base_dir.name == "guidance"
    assert resolver.base_dir.exists()


def test_resolve_exact_domain_content_type_match():
    resolver = PedagogyResolver()
    resolution = resolver.resolve_with_reason(content_type="project_building", domain="genai")

    assert resolution["profile"] == "project_build_along"
    assert "exact match" in resolution["reason"]


def test_resolve_content_type_default():
    resolver = PedagogyResolver()
    resolution = resolver.resolve_with_reason(content_type="platform_walkthrough", domain="unknown-domain")

    assert resolution["profile"] == "guided_tool_walkthrough"
    assert "content-type default" in resolution["reason"]


def test_resolve_global_default_when_type_missing():
    resolver = PedagogyResolver()
    resolution = resolver.resolve_with_reason(content_type="nonexistent_pipeline", domain="unknown-domain")

    assert resolution["profile"] == "concept_progression"
    assert "global default" in resolution["reason"]


def test_list_profiles_includes_concept_progression():
    resolver = PedagogyResolver()
    assert "concept_progression" in resolver.list_profiles()


def test_resolve_domain_profile_prefers_stack_manifest_override():
    resolver = PedagogyResolver()
    resolution = resolver.resolve_domain_profile(domain="genai", content_type="concept_explainer")

    assert resolution["profile"] == "project_build_along"
    assert "stack manifest override" in resolution["reason"]
    assert "project-centered" in resolution["rationale"]
