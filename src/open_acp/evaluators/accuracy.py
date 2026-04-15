"""Accuracy evaluator — checks factual correctness and precision."""
from open_acp.evaluators.base import BaseEvaluator
from open_acp.models.evaluation import EvalDimension, EvalScore


class AccuracyEvaluator(BaseEvaluator):
    dimension = EvalDimension.ACCURACY

    def evaluate(self, content: str, context: dict, content_type: str = "concept_explainer") -> EvalScore:
        rubric = self._get_rubric(content_type)
        prompt = f"""Evaluate this content for ACCURACY on a scale of 1-5.

## Rubric
{rubric}

## Content to Evaluate
{content[:8000]}

## Context
Domain: {context.get('domain', 'unknown')}
Content Type: {content_type}

Return JSON: {{"score": 1-5, "evidence": "specific examples", "failing_elements": ["list of inaccurate claims if any"]}}"""

        response = self._call_claude(prompt, system="You are a domain expert fact-checker. Be precise and cite specific issues.", model_tier="strong")
        return self._parse_score(response, self.dimension)

    def _get_rubric(self, content_type: str) -> str:
        base = "1=Multiple errors present, 2=Some inaccuracies, 3=Mostly correct with minor issues, 4=Accurate with rare minor issues, 5=Expert-level precision"
        if content_type in ("mcq_practice", "coding_practice"):
            return base + "\nFor assessments: verify all solutions are correct, distractors are genuinely wrong, and explanations are accurate."
        return base
