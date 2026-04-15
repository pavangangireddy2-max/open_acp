"""Citation provenance evaluator — checks that claims are grounded."""
from open_acp.evaluators.base import BaseEvaluator
from open_acp.models.evaluation import EvalDimension, EvalScore


class CitationProvenanceEvaluator(BaseEvaluator):
    dimension = EvalDimension.CITATION_PROVENANCE

    def evaluate(self, content: str, context: dict, content_type: str = "concept_explainer") -> EvalScore:
        prompt = f"""Evaluate this content for CITATION PROVENANCE on a scale of 1-5.

Check each factual claim: is it grounded in common knowledge, cited, or potentially hallucinated?

## Rubric
1=Multiple ungrounded claims
2=Some claims lack provenance
3=Most claims are grounded, few concerns
4=Strong provenance, rare minor gaps
5=All claims verifiable or properly hedged

## Content to Evaluate
{content[:8000]}

Return JSON: {{"score": 1-5, "evidence": "analysis of claim grounding", "failing_elements": ["list of potentially hallucinated or ungrounded claims"]}}"""

        response = self._call_claude(prompt, system="You are a fact-checking specialist. Identify any claim that could be hallucinated or lacks provenance.", model_tier="strong")
        return self._parse_score(response, self.dimension)
