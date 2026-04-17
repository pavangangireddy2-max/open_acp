from pathlib import Path

from open_acp.loops.loop_a.nodes import _build_bootstrap_warnings, _load_raw_sources
from open_acp.models.signals import SignalBatch, RawSignal, ChannelCategory, ChannelType
from open_acp.orchestrator.loop_review import LoopReviewRunner


def test_loop_review_runner_executes_first_loop_a_stage(monkeypatch, tmp_path):
    runner = LoopReviewRunner(output_dir=str(tmp_path))

    def fake_stage(state):
        return {
            "signal_batch": SignalBatch(
                batch_id="batch_1",
                signals=[
                    RawSignal(
                        signal_id="sig_1",
                        channel_category=ChannelCategory.INDUSTRY_MARKET,
                        channel_name="sources",
                        content="Python remains important for GenAI.",
                        timestamp="2026-04-16T00:00:00+00:00",
                        signal_type=ChannelType.PROACTIVE,
                        metadata={"filename": "genai_120hr_curriculum.md"},
                    )
                ],
                ingested_at="2026-04-16T00:00:00+00:00",
                source_domain="genai",
            ),
            "bootstrap_warnings": ["Using shared market inputs for now."],
        }

    monkeypatch.setattr(runner, "_load_stage_callable", lambda loop_id, stage_id: fake_stage)

    result = runner.execute_review_stage(
        loop_id="loop_a",
        base_state={"domain": "genai", "cycle_id": "cycle_a"},
    )

    assert result["status"] == "awaiting_review"
    assert result["stage_id"] == "ingest_signals"
    assert result["next_stage_id"] == "detect_patterns"
    assert "Bootstrap mode is active" in result["review_packet"]["summary"]
    assert "genai_120hr_curriculum.md" in result["review_packet"]["key_decisions"][1]
    assert "Using shared market inputs for now." in result["review_packet"]["key_decisions"]
    assert Path(result["review_packet_paths"]["markdown"]).exists()
    assert Path(result["state_path"]).exists()


def test_loop_review_runner_resumes_next_stage(monkeypatch, tmp_path):
    runner = LoopReviewRunner(output_dir=str(tmp_path))

    def fake_callable(loop_id, stage_id):
        if stage_id == "ingest_signals":
            return lambda state: {
                "signal_batch": SignalBatch(
                    batch_id="batch_1",
                    signals=[
                        RawSignal(
                            signal_id="sig_1",
                            channel_category=ChannelCategory.INDUSTRY_MARKET,
                            channel_name="sources",
                            content="RAG and Python remain important.",
                            timestamp="2026-04-16T00:00:00+00:00",
                            signal_type=ChannelType.PROACTIVE,
                            metadata={"filename": "genai_120hr_curriculum.md"},
                        )
                    ],
                    ingested_at="2026-04-16T00:00:00+00:00",
                    source_domain="genai",
                )
            }
        return lambda state: {
            "detected_patterns": [{"pattern_id": "p1", "description": "Demand for RAG skills"}],
            "pattern_detection_status": "parsed",
            "drift_score": 0.42,
        }

    monkeypatch.setattr(runner, "_load_stage_callable", fake_callable)

    runner.execute_review_stage(
        loop_id="loop_a",
        base_state={"domain": "genai", "cycle_id": "cycle_b"},
    )
    result = runner.execute_review_stage(
        loop_id="loop_a",
        base_state={"domain": "genai", "cycle_id": "cycle_b"},
    )

    assert result["stage_id"] == "detect_patterns"
    assert result["next_stage_id"] == "update_skill_graph"
    assert "drift score 0.42" in result["review_packet"]["summary"]
    assert "genai_120hr_curriculum.md" in result["review_packet"]["key_decisions"][0]


def test_loop_review_runner_detect_patterns_fallback_wording(monkeypatch, tmp_path):
    runner = LoopReviewRunner(output_dir=str(tmp_path))

    def fake_callable(loop_id, stage_id):
        if stage_id == "ingest_signals":
            return lambda state: {
                "signal_batch": SignalBatch(
                    batch_id="batch_1",
                    signals=[
                        RawSignal(
                            signal_id="sig_1",
                            channel_category=ChannelCategory.INDUSTRY_MARKET,
                            channel_name="sources",
                            content="RAG and Python remain important.",
                            timestamp="2026-04-16T00:00:00+00:00",
                            signal_type=ChannelType.PROACTIVE,
                            metadata={"filename": "genai_120hr_curriculum.md"},
                        )
                    ],
                    ingested_at="2026-04-16T00:00:00+00:00",
                    source_domain="genai",
                )
            }
        return lambda state: {
            "detected_patterns": [{"pattern_id": "p_raw", "description": "Pattern detection returned non-JSON"}],
            "pattern_detection_status": "fallback_non_json",
            "pattern_detection_note": (
                "Pattern detection response could not be parsed as JSON. "
                "Using a fallback placeholder pattern and default drift score 0.50."
            ),
            "drift_score": 0.5,
        }

    monkeypatch.setattr(runner, "_load_stage_callable", fake_callable)

    runner.execute_review_stage(
        loop_id="loop_a",
        base_state={"domain": "genai", "cycle_id": "cycle_fallback"},
    )
    result = runner.execute_review_stage(
        loop_id="loop_a",
        base_state={"domain": "genai", "cycle_id": "cycle_fallback"},
    )

    assert result["stage_id"] == "detect_patterns"
    assert "Pattern detection parse failed" in result["review_packet"]["summary"]
    assert "fallback placeholder pattern" in result["review_packet"]["key_decisions"][2].lower()


def test_loop_review_runner_generate_curriculum_fallback_wording(monkeypatch, tmp_path):
    runner = LoopReviewRunner(output_dir=str(tmp_path))

    def fake_callable(loop_id, stage_id):
        if stage_id == "load_wiki_context":
            return lambda state: {
                "skill_graph_context": "## Skills in Wiki\n- **Python Programming**",
                "learner_context": "## Learner Segments\n- **Career Switcher**",
                "curriculum_source_context": "### Source: stack curriculum seed",
            }
        if stage_id == "resolve_product_context":
            return lambda state: {
                "product_context": {
                    "product_label": "NIAT B3",
                    "product_category": "degree_program_product",
                    "curriculum_container_kind": "academic_degree_curriculum",
                    "resolution_reason": "explicit product selection: NIAT/B3",
                }
            }
        if stage_id == "resolve_structure_profile":
            return lambda state: {
                "structure_profile": {
                    "structure_profile_id": "niat_university_structure",
                    "curriculum_container_kind": "academic_degree_curriculum",
                    "hierarchy": ["batch_curriculum_grid_template", "university", "branch"],
                }
            }
        if stage_id == "resolve_packaging_profile":
            return lambda state: {
                "packaging_profile": {
                    "packaging_profile_id": "genai_stack_packaging",
                    "module_count_per_course": {"default": 3},
                    "topic_count_per_module": {"default": 4},
                    "allowed_learning_unit_types": ["video_session_unit", "reading_material_unit"],
                }
            }
        if stage_id == "resolve_design_priority_profile":
            return lambda state: {
                "design_priority_profile": {
                    "profile_id": "niat_university_structure_design_priorities",
                    "dimension_ids": ["regulatory_compliance", "job_placement_outcomes"],
                    "ordered_dimensions": ["regulatory_compliance", "job_placement_outcomes"],
                    "dimensions": [{"dimension_id": "regulatory_compliance"}, {"dimension_id": "job_placement_outcomes"}],
                    "resolution_reason": "structure-driven",
                }
            }
        if stage_id == "resolve_time_budget_context":
            return lambda state: {
                "time_budget_context": {
                    "context_id": "time_budget_genai",
                    "source_total_hours": 120.0,
                    "target_total_hours": 120.0,
                    "slot_budget_hours": 120.0,
                    "available_design_hours": 120.0,
                    "resolution_reason": "source-defined total hours preserved",
                }
            }
        if stage_id == "resolve_pedagogy_profile":
            return lambda state: {
                "pedagogy_profile": "project_build_along",
                "pedagogy_rationale": "Project-centered stack.",
            }
        if stage_id == "generate_brief":
            return lambda state: {
                "brief_generation_status": "parsed",
                "brief": {
                    "brief_id": "brief_genai_niat_b3",
                    "program_name": "GenAI 120 Hr Curriculum",
                    "audience": {"primary": ["genai_specialization_seekers"]},
                    "pedagogy": {"default_profile": "project_build_along"},
                    "terminal_outcomes": ["Build and deploy a document-grounded GenAI app"],
                },
            }
        return lambda state: {
            "curriculum_generation_status": "fallback_non_json",
            "curriculum_generation_note": "Curriculum generation response could not be parsed as JSON. Using an empty fallback curriculum draft.",
            "curriculum_generation_raw_response": "This is not valid JSON.",
            "curriculum_map": {
                "curriculum_id": "cur_genai",
                "brief_ref": "brief_genai_niat_b3",
                "program_name": "genai Curriculum",
                "domain": "genai",
                "courses": [],
                "total_hours": 0,
            },
        }

    monkeypatch.setattr(runner, "_load_stage_callable", fake_callable)

    base_state = {"domain": "genai", "cycle_id": "cycle_curriculum", "content_type": "concept_explainer"}
    for _ in range(8):
        runner.execute_review_stage(loop_id="loop_b", base_state=base_state)
    result = runner.execute_review_stage(
        loop_id="loop_b",
        base_state=base_state,
    )

    assert result["stage_id"] == "generate_curriculum"
    assert result["next_stage_id"] == "compare_curriculum_changes"
    assert "Curriculum generation parse failed" in result["review_packet"]["summary"]
    assert "empty fallback curriculum draft" in result["review_packet"]["key_decisions"][0]


def test_load_raw_sources_prefers_manifest_for_genai():
    sources = _load_raw_sources("genai")
    filenames = sorted(source["filename"] for source in sources)
    paths = [source["path"] for source in sources]

    assert "genai_120hr_curriculum.md" in filenames
    assert "competitor_courses.md" in filenames
    assert "ml_engineer_requirements.md" in filenames
    assert all("knowledge/sources/" in path for path in paths)


def test_build_bootstrap_warnings_flags_generic_domain_coverage():
    warnings = _build_bootstrap_warnings(
        "genai",
        [
            {
                "filename": "niat_b3_learner_profile.md",
                "category": "learner",
                "content": "persona",
                "path": "/tmp/niat_b3_learner_profile.md",
            },
            {
                "filename": "ml_engineer_requirements.md",
                "category": "job_postings",
                "content": "requirements",
                "path": "/tmp/ml_engineer_requirements.md",
            },
            {
                "filename": "competitor_courses.md",
                "category": "competitors",
                "content": "competitors",
                "path": "/tmp/competitor_courses.md",
            },
        ],
    )

    assert any("job postings" in warning for warning in warnings)
    assert any("competitors" in warning for warning in warnings)
