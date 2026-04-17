"""Feedback-channel contract models and manifest loader."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from open_acp.config.curriculum_context import find_project_root, load_yaml
from open_acp.models.signals import ChannelCategory


class CanonicalSourceFamily(BaseModel):
    source_family_id: str
    description: str
    expected_location: str
    preferred_granularity: Literal["aggregated_export", "normalized_snapshot", "raw_event"] = "aggregated_export"


class CanonicalVocabulary(BaseModel):
    vocabulary_id: str
    description: str
    owner: str


class RuntimeDigestTarget(BaseModel):
    digest_id: str
    purpose: str


class KnowledgeTarget(BaseModel):
    target_id: str
    target_type: Literal["runtime_entity", "stack_profile", "product_summary", "cycle_artifact"]
    update_mode: Literal["create", "update", "enrich", "derive"]


class BackpropTarget(BaseModel):
    loop_id: Literal["loop_a", "loop_b", "loop_c", "loop_d"]
    stage_id: str
    rationale: str


class FeedbackChannelContract(BaseModel):
    channel_id: str
    label: str
    channel_category: ChannelCategory
    unit_of_data: str
    owning_dimensions: list[int] = Field(default_factory=list)
    keep_raw_analysis_external: bool = True
    preferred_ingest_mode: Literal["aggregated_export", "normalized_entries"] = "aggregated_export"
    canonical_source_families: list[CanonicalSourceFamily] = Field(default_factory=list)
    canonical_vocabularies: list[CanonicalVocabulary] = Field(default_factory=list)
    runtime_digests: list[RuntimeDigestTarget] = Field(default_factory=list)
    knowledge_targets: list[KnowledgeTarget] = Field(default_factory=list)
    loop_b_influence: list[str] = Field(default_factory=list)
    backprop_targets: list[BackpropTarget] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    manifest_path: str | None = None


def channel_contracts_root() -> Path:
    return find_project_root() / "knowledge" / "manifests" / "channels"


def load_channel_contract(channel_id: str) -> FeedbackChannelContract:
    manifest_path = channel_contracts_root() / f"{channel_id}.yaml"
    data = load_yaml(manifest_path)
    if not data:
        raise FileNotFoundError(f"Channel contract not found: {channel_id}")
    data["manifest_path"] = str(manifest_path)
    return FeedbackChannelContract.model_validate(data)


def list_channel_contract_ids() -> list[str]:
    root = channel_contracts_root()
    if not root.exists():
        return []
    return sorted(path.stem for path in root.glob("*.yaml"))


def list_channel_contracts() -> list[FeedbackChannelContract]:
    return [load_channel_contract(channel_id) for channel_id in list_channel_contract_ids()]


def get_channel_contracts_for_dimension(dimension_id: int) -> list[FeedbackChannelContract]:
    return [
        contract
        for contract in list_channel_contracts()
        if dimension_id in contract.owning_dimensions
    ]


def get_channel_contracts_for_category(category: ChannelCategory) -> list[FeedbackChannelContract]:
    return [
        contract
        for contract in list_channel_contracts()
        if contract.channel_category == category
    ]
