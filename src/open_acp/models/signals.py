"""Signal ingestion models: raw signals and batches from 11 channel categories."""

from enum import Enum

from pydantic import BaseModel


class ChannelCategory(str, Enum):
    STUDENT_LEARNING = "student_learning"
    CUSTOMER_SUPPORT = "customer_support"
    SALES = "sales"
    SOCIAL_MEDIA = "social_media"
    PLACEMENT = "placement"
    PLATFORM_ANALYTICS = "platform_analytics"
    PERFORMANCE_ANALYTICS = "performance_analytics"
    INTERVIEW_INTEL = "interview_intel"
    INTERNAL_TEAM = "internal_team"
    INDUSTRY_MARKET = "industry_market"
    CROSS_PROGRAM = "cross_program"


class ChannelType(str, Enum):
    REACTIVE = "reactive"
    PROACTIVE = "proactive"


class RawSignal(BaseModel):
    signal_id: str
    channel_category: ChannelCategory
    channel_name: str
    content: str
    timestamp: str
    signal_type: ChannelType
    metadata: dict


class SignalBatch(BaseModel):
    batch_id: str
    signals: list[RawSignal]
    ingested_at: str
    source_domain: str
