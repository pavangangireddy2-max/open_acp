"""Base evaluator — all evaluators inherit from this."""
from abc import ABC, abstractmethod
from pydantic import BaseModel
from open_acp.models.evaluation import EvalDimension, EvalScore


class BaseEvaluator(ABC):
    """Abstract base for content evaluators."""

    dimension: EvalDimension

    @abstractmethod
    def evaluate(self, content: str, context: dict, content_type: str = "concept_explainer") -> EvalScore:
        """Evaluate content and return a score (1-5) with evidence."""
        ...

    def _call_claude(self, prompt: str, system: str = "", model_tier: str = "strong") -> str:
        """Helper to call Claude for evaluation."""
        from open_acp.utils.claude import ClaudeClient
        client = ClaudeClient()
        return client.generate(prompt=prompt, system=system, model_tier=model_tier, max_tokens=2048, temperature=0.3)

    def _parse_score(self, response: str, dimension: EvalDimension) -> EvalScore:
        """Parse a score response from Claude."""
        import json
        try:
            cleaned = response.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned[cleaned.index("\n")+1:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            data = json.loads(cleaned.strip())
            return EvalScore(
                dimension=dimension,
                score=float(data.get("score", 3.0)),
                evidence=data.get("evidence", ""),
                failing_elements=data.get("failing_elements", []),
            )
        except (json.JSONDecodeError, ValueError):
            return EvalScore(
                dimension=dimension,
                score=3.0,
                evidence=f"Parse error: {response[:200]}",
                failing_elements=["parse_error"],
            )
