"""Pedagogy evaluator — checks alignment with learning science principles."""
from open_acp.evaluators.base import BaseEvaluator
from open_acp.models.evaluation import EvalDimension, EvalScore


class PedagogyEvaluator(BaseEvaluator):
    dimension = EvalDimension.PEDAGOGY

    def evaluate(self, content: str, context: dict, content_type: str = "concept_explainer") -> EvalScore:
        rubric = self._get_rubric(content_type)
        prompt = f"""Evaluate this content for PEDAGOGY effectiveness on a scale of 1-5.

## Rubric
{rubric}

## Content to Evaluate
{content[:8000]}

## Context
Domain: {context.get('domain', 'unknown')}
Content Type: {content_type}
Pedagogy Profile: {context.get('pedagogy_profile', context.get('pedagogy_framework', 'not specified'))}

Return JSON: {{"score": 1-5, "evidence": "specific examples of good/bad pedagogy", "failing_elements": ["list of pedagogical issues"]}}"""

        response = self._call_claude(prompt, system="You are an instructional design expert evaluating pedagogical effectiveness.", model_tier="strong")
        return self._parse_score(response, self.dimension)

    def _get_rubric(self, content_type: str) -> str:
        base = "1=No alignment with learning objectives, 2=Weak structure, 3=Adequate coverage, 4=Strong pedagogical design, 5=Exemplary transfer-enabling instruction"
        if content_type in ("classroom_quiz", "module_quiz", "fortnight_quiz", "final_course_quiz", "graded_assessment"):
            return base + "\nFor assessments: verify Bloom level distribution matches targets, questions test declared objectives, rubric criteria are clear."
        if content_type == "problem_solving":
            return base + "\nFor problem solving: verify difficulty progression, scaffolding quality, and that solutions explain reasoning not just answers."
        return base
