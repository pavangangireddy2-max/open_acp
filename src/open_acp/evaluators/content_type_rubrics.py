"""Content-type-specific rubric adjustments for evaluators."""
from open_acp.models.evaluation import EvalDimension


# Maps content_type -> dimension -> rubric adjustment text
RUBRIC_ADJUSTMENTS: dict[str, dict[EvalDimension, str]] = {
    "concept_explainer": {
        EvalDimension.PEDAGOGY: "Concept explanations should use analogies before definitions, progress through Bloom levels, and include concrete examples.",
        EvalDimension.ENGAGEMENT: "Hook with a real-world problem or question. Vary section structure.",
    },
    "problem_solving": {
        EvalDimension.ACCURACY: "All worked solutions must be correct. Multiple approaches should be valid.",
        EvalDimension.PEDAGOGY: "Difficulty must progress. Hints should scaffold without giving answers.",
    },
    "mcq_practice": {
        EvalDimension.ACCURACY: "Every correct answer must be unambiguously correct. Every distractor must be unambiguously wrong.",
        EvalDimension.PEDAGOGY: "Distractors should target common misconceptions. Explanations should teach.",
    },
    "coding_practice": {
        EvalDimension.ACCURACY: "All solutions must compile/run correctly. All test cases must pass.",
        EvalDimension.PEDAGOGY: "Problems should have clear constraints. Starter code should compile.",
    },
    "classroom_quiz": {
        EvalDimension.PEDAGOGY: "Focus on Remember/Understand. Quick formative check, not summative.",
    },
    "graded_assessment": {
        EvalDimension.ACCURACY: "University-grade rigor. No ambiguous questions. Partial credit criteria clear.",
        EvalDimension.PEDAGOGY: "Full Bloom range. Fair difficulty distribution. Time-appropriate.",
    },
}


def get_rubric_adjustment(content_type: str, dimension: EvalDimension) -> str:
    """Get content-type-specific rubric text for a dimension."""
    return RUBRIC_ADJUSTMENTS.get(content_type, {}).get(dimension, "")
