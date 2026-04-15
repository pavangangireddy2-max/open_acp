"""Engagement evaluator — checks if content is compelling and motivating."""
from open_acp.evaluators.base import BaseEvaluator
from open_acp.models.evaluation import EvalDimension, EvalScore


class EngagementEvaluator(BaseEvaluator):
    dimension = EvalDimension.ENGAGEMENT

    def evaluate(self, content: str, context: dict, content_type: str = "concept_explainer") -> EvalScore:
        prompt = f"""Evaluate this content for ENGAGEMENT on a scale of 1-5.

## Rubric
1=Dry exposition, reads like a textbook appendix
2=Functional but uninspiring
3=Adequate — maintains attention
4=Engaging — uses hooks, examples, and varied structure
5=Compelling — would hold attention of the target audience throughout

## Content to Evaluate
{content[:8000]}

## Context
Domain: {context.get('domain', 'unknown')}
Content Type: {content_type}

Return JSON: {{"score": 1-5, "evidence": "specific examples", "failing_elements": ["list of weak sections"]}}"""

        response = self._call_claude(prompt, system="You are an educational content reviewer focused on learner engagement.", model_tier="strong")
        return self._parse_score(response, self.dimension)
