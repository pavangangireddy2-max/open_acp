"""Mock signal ingestor — generates fake signals for testing."""
from datetime import datetime, UTC
from open_acp.models.signals import RawSignal, SignalBatch, ChannelCategory, ChannelType


class MockChannelIngestor:
    """Generates mock signals for testing Loop D feedback ingestion."""

    @staticmethod
    def generate_feedback_batch(
        domain: str,
        content_modules: list[str],
        cycle_id: str = "cycle_1",
    ) -> SignalBatch:
        """Generate a batch of mock feedback signals about produced content."""
        signals = []

        # Student feedback
        for i, module_id in enumerate(content_modules[:3]):
            signals.append(RawSignal(
                signal_id=f"fb_{cycle_id}_{i}",
                channel_category=ChannelCategory.STUDENT_LEARNING,
                channel_name="Queries team",
                content=f"Students report that module '{module_id}' section on advanced topics moves too fast. Need more examples.",
                timestamp=datetime.now(UTC).isoformat(),
                signal_type=ChannelType.REACTIVE,
                metadata={"module_id": module_id, "feedback_type": "pacing"},
            ))

        # Platform analytics
        signals.append(RawSignal(
            signal_id=f"fb_{cycle_id}_analytics",
            channel_category=ChannelCategory.PLATFORM_ANALYTICS,
            channel_name="Video analytics",
            content="Average watch time drops 40% at the 25-minute mark across all modules. Suggests cognitive overload.",
            timestamp=datetime.now(UTC).isoformat(),
            signal_type=ChannelType.PROACTIVE,
            metadata={"metric": "watch_time_drop", "threshold": 0.4},
        ))

        # Placement feedback
        signals.append(RawSignal(
            signal_id=f"fb_{cycle_id}_placement",
            channel_category=ChannelCategory.PLACEMENT,
            channel_name="Recruiter insights",
            content="Recruiters report candidates lack practical MLOps experience. Theory is fine but can't set up a CI/CD pipeline for ML.",
            timestamp=datetime.now(UTC).isoformat(),
            signal_type=ChannelType.REACTIVE,
            metadata={"skill_gap": "mlops_practical"},
        ))

        return SignalBatch(
            batch_id=f"feedback_{cycle_id}",
            signals=signals,
            ingested_at=datetime.now(UTC).isoformat(),
            source_domain=domain,
        )
