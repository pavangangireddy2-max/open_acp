from open_acp.channels import (
    get_channel_contracts_for_category,
    get_channel_contracts_for_dimension,
    list_channel_contract_ids,
    load_channel_contract,
)
from open_acp.models.signals import ChannelCategory


def test_interview_intelligence_contract_loads():
    contract = load_channel_contract("interview_intelligence")

    assert contract.channel_id == "interview_intelligence"
    assert contract.channel_category == ChannelCategory.INTERVIEW_INTEL
    assert contract.preferred_ingest_mode == "aggregated_export"
    assert 1 in contract.owning_dimensions
    source_family_ids = {family.source_family_id for family in contract.canonical_source_families}
    assert "role_opportunity_summary" in source_family_ids
    assert "skill_opportunity_summary" in source_family_ids
    assert "recruiter_feedback" not in source_family_ids
    assert any(d.digest_id == "skill_outcomes_signal_digest" for d in contract.runtime_digests)
    assert any(t.target_id == "role_profile" for t in contract.knowledge_targets)
    assert any(t.target_id == "skill_entities" for t in contract.knowledge_targets)
    assert any(t.stage_id == "generate_curriculum" for t in contract.backprop_targets)


def test_channel_contract_registry_lists_interview_intelligence():
    ids = list_channel_contract_ids()

    assert "interview_intelligence" in ids


def test_channel_contract_registry_filters_by_dimension():
    contracts = get_channel_contracts_for_dimension(1)

    assert any(contract.channel_id == "interview_intelligence" for contract in contracts)


def test_channel_contract_registry_filters_by_category():
    contracts = get_channel_contracts_for_category(ChannelCategory.INTERVIEW_INTEL)

    assert any(contract.channel_id == "interview_intelligence" for contract in contracts)
