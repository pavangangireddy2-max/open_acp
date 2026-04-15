"""Content type and pipeline family enumerations."""

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
    FORTNIGHT_QUIZ = "fortnight_quiz"
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
