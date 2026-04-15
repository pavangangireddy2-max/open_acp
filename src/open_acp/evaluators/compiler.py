"""Evaluator compiler — runs all 5 evaluators and computes final score."""
from datetime import datetime, UTC
from typing import Optional

from open_acp.models.evaluation import EvalDimension, EvalScore, EvalReport
from open_acp.evaluators.accuracy import AccuracyEvaluator
from open_acp.evaluators.pedagogy import PedagogyEvaluator
from open_acp.evaluators.engagement import EngagementEvaluator
from open_acp.evaluators.brand import BrandEvaluator
from open_acp.evaluators.citation import CitationProvenanceEvaluator
from open_acp.config.constants import CONTENT_PASS_THRESHOLD


class EvaluatorCompiler:
    """Runs all evaluators and produces an EvalReport."""

    def __init__(self):
        self.evaluators = [
            AccuracyEvaluator(),
            PedagogyEvaluator(),
            EngagementEvaluator(),
            BrandEvaluator(),
            CitationProvenanceEvaluator(),
        ]

    def evaluate(
        self,
        content: str,
        context: dict,
        content_type: str = "concept_explainer",
        module_id: str = "unknown",
        iteration: int = 1,
    ) -> EvalReport:
        """Run all evaluators and return a comprehensive report."""
        scores: list[EvalScore] = []

        for evaluator in self.evaluators:
            try:
                score = evaluator.evaluate(content, context, content_type)
                scores.append(score)
                print(f"    {score.dimension.value}: {score.score:.1f}")
            except Exception as e:
                # Don't fail the whole evaluation if one dimension errors
                scores.append(EvalScore(
                    dimension=evaluator.dimension,
                    score=3.0,
                    evidence=f"Evaluator error: {str(e)[:200]}",
                    failing_elements=["evaluator_error"],
                ))
                print(f"    {evaluator.dimension.value}: ERROR ({e})")

        final_score = min(s.score for s in scores) if scores else 0.0
        passed = final_score >= CONTENT_PASS_THRESHOLD

        return EvalReport(
            report_id=f"eval_{module_id}_{iteration}",
            content_type=content_type,
            module_id=module_id,
            scores=scores,
            final_score=final_score,
            passed=passed,
            iteration=iteration,
            evaluated_at=datetime.now(UTC).isoformat(),
        )
