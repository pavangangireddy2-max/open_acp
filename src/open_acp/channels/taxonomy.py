"""Channel taxonomy — 42 channels across 11 categories."""
from open_acp.models.signals import ChannelCategory, ChannelType

# Full channel taxonomy mapping
CHANNEL_TAXONOMY: dict[ChannelCategory, list[dict]] = {
    ChannelCategory.STUDENT_LEARNING: [
        {"name": "Queries team", "type": ChannelType.REACTIVE},
        {"name": "Mentors", "type": ChannelType.REACTIVE},
        {"name": "Coaches", "type": ChannelType.REACTIVE},
        {"name": "Instructors", "type": ChannelType.REACTIVE},
    ],
    ChannelCategory.CUSTOMER_SUPPORT: [
        {"name": "Escalated queries", "type": ChannelType.REACTIVE},
        {"name": "Escalated calls", "type": ChannelType.REACTIVE},
    ],
    ChannelCategory.SALES: [
        {"name": "Lead resistances", "type": ChannelType.REACTIVE},
        {"name": "Objections", "type": ChannelType.REACTIVE},
        {"name": "Escalated calls", "type": ChannelType.REACTIVE},
    ],
    ChannelCategory.SOCIAL_MEDIA: [
        {"name": "LinkedIn", "type": ChannelType.REACTIVE},
        {"name": "Instagram", "type": ChannelType.REACTIVE},
        {"name": "YouTube", "type": ChannelType.REACTIVE},
        {"name": "X", "type": ChannelType.REACTIVE},
        {"name": "WhatsApp", "type": ChannelType.REACTIVE},
        {"name": "Telegram", "type": ChannelType.REACTIVE},
    ],
    ChannelCategory.PLACEMENT: [
        {"name": "Recruiter insights", "type": ChannelType.REACTIVE},
        {"name": "Skill assessments", "type": ChannelType.REACTIVE},
    ],
    ChannelCategory.PLATFORM_ANALYTICS: [
        {"name": "Video analytics", "type": ChannelType.PROACTIVE},
        {"name": "Reading analytics", "type": ChannelType.PROACTIVE},
        {"name": "MCQ analytics", "type": ChannelType.PROACTIVE},
        {"name": "Coding analytics", "type": ChannelType.PROACTIVE},
        {"name": "Exam feedback", "type": ChannelType.PROACTIVE},
    ],
    ChannelCategory.PERFORMANCE_ANALYTICS: [
        {"name": "Quiz scores", "type": ChannelType.PROACTIVE},
        {"name": "Module scores", "type": ChannelType.PROACTIVE},
        {"name": "Academic scores", "type": ChannelType.PROACTIVE},
        {"name": "Skill scores", "type": ChannelType.PROACTIVE},
        {"name": "Interview scores", "type": ChannelType.PROACTIVE},
    ],
    ChannelCategory.INTERVIEW_INTEL: [
        {"name": "TR questions", "type": ChannelType.PROACTIVE},
        {"name": "Written tests", "type": ChannelType.PROACTIVE},
        {"name": "Take-home assignments", "type": ChannelType.PROACTIVE},
        {"name": "Dev insights", "type": ChannelType.PROACTIVE},
    ],
    ChannelCategory.INTERNAL_TEAM: [
        {"name": "Curriculum team", "type": ChannelType.PROACTIVE},
        {"name": "Product team", "type": ChannelType.PROACTIVE},
        {"name": "Pedagogy team", "type": ChannelType.PROACTIVE},
        {"name": "Placement ops", "type": ChannelType.PROACTIVE},
        {"name": "Program managers", "type": ChannelType.PROACTIVE},
    ],
    ChannelCategory.INDUSTRY_MARKET: [
        {"name": "Competitor analysis", "type": ChannelType.PROACTIVE},
        {"name": "Tech shifts", "type": ChannelType.PROACTIVE},
    ],
    ChannelCategory.CROSS_PROGRAM: [
        {"name": "Workshops", "type": ChannelType.PROACTIVE},
        {"name": "Corp trainings", "type": ChannelType.PROACTIVE},
        {"name": "Bootcamps", "type": ChannelType.PROACTIVE},
        {"name": "Alumni feedback", "type": ChannelType.PROACTIVE},
    ],
}


def get_total_channels() -> int:
    return sum(len(channels) for channels in CHANNEL_TAXONOMY.values())


def get_channels_by_type(channel_type: ChannelType) -> list[dict]:
    result = []
    for category, channels in CHANNEL_TAXONOMY.items():
        for ch in channels:
            if ch["type"] == channel_type:
                result.append({"category": category, **ch})
    return result
