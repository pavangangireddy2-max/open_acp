"""Content type and pipeline family enumerations.

Canonical runtime names may differ from legacy pipeline/file names.
Use ``normalize_content_type`` before making taxonomy decisions.
"""

from enum import Enum


class PipelineFamily(str, Enum):
    SESSION = "session"           # PPT + speaker notes
    WRITTEN = "written"           # Markdown output
    PRACTICE = "practice"         # Item banks
    ASSESSMENT = "assessment"     # Scored, time-boxed


class ContentType(str, Enum):
    # Session family (6)
    CONCEPT_EXPLAINER = "concept_explainer"
    PROBLEM_SOLVING = "problem_solving"
    PROJECT_BUILDING = "project_building"
    LEARNING_SUPPORT = "learning_support"
    PLATFORM_WALKTHROUGH = "platform_walkthrough"
    INDUCTION = "induction"
    # Written family (2)
    READING_MATERIAL = "reading_material"
    SUMMARY_CHEATSHEET = "summary_cheatsheet"
    # Practice family (2)
    MCQ_PRACTICE = "mcq_practice"
    CODING_PRACTICE = "coding_practice"
    # Assessment family (6)
    CLASSROOM_QUIZ = "classroom_quiz"
    MODULE_QUIZ = "module_quiz"
    SKILL_ASSESSMENT = "skill_assessment"
    FINAL_COURSE_QUIZ = "final_course_quiz"
    FINAL_COURSE_PROJECT = "final_course_project"
    GRADED_ASSESSMENT = "graded_assessment"

    @property
    def family(self) -> PipelineFamily:
        """Return the pipeline family for this content type."""
        _session = {
            ContentType.CONCEPT_EXPLAINER,
            ContentType.PROBLEM_SOLVING,
            ContentType.PROJECT_BUILDING,
            ContentType.LEARNING_SUPPORT,
            ContentType.PLATFORM_WALKTHROUGH,
            ContentType.INDUCTION,
        }
        _written = {ContentType.READING_MATERIAL, ContentType.SUMMARY_CHEATSHEET}
        _practice = {ContentType.MCQ_PRACTICE, ContentType.CODING_PRACTICE}
        if self in _session:
            return PipelineFamily.SESSION
        if self in _written:
            return PipelineFamily.WRITTEN
        if self in _practice:
            return PipelineFamily.PRACTICE
        return PipelineFamily.ASSESSMENT

    @classmethod
    def from_value(cls, value: str) -> "ContentType":
        """Resolve a canonical enum member from a canonical or legacy string."""
        return cls(normalize_content_type(value))


LEGACY_CONTENT_TYPE_ALIASES: dict[str, str] = {
    "fortnight_quiz": ContentType.SKILL_ASSESSMENT.value,
}


CANONICAL_PIPELINE_FILE_ALIASES: dict[str, str] = {
    ContentType.SKILL_ASSESSMENT.value: "fortnight_quiz",
}


def normalize_content_type(value: str) -> str:
    """Return the canonical runtime content-type name."""
    normalized = (value or "").strip()
    return LEGACY_CONTENT_TYPE_ALIASES.get(normalized, normalized)


def pipeline_lookup_content_type(value: str) -> str:
    """Return the pipeline/file lookup key for a canonical or legacy content type."""
    normalized = normalize_content_type(value)
    return CANONICAL_PIPELINE_FILE_ALIASES.get(normalized, normalized)
