"""Brand evaluator — checks compliance with brand voice and style guidelines."""
from open_acp.evaluators.base import BaseEvaluator
from open_acp.models.evaluation import EvalDimension, EvalScore


class BrandEvaluator(BaseEvaluator):
    dimension = EvalDimension.BRAND

    def evaluate(self, content: str, context: dict, content_type: str = "concept_explainer") -> EvalScore:
        # Load the full brand playbook
        brand_rules = ""
        try:
            from open_acp.styles.style_loader import StyleLoader
            loader = StyleLoader()
            playbook_text = loader.load_as_text("default")
            # Include the most actionable sections for evaluation
            brand_rules = f"""
## Brand Playbook (ForgeAI/NxtWave)

{playbook_text[:4000]}
"""
        except Exception:
            brand_rules = "\nNo brand playbook found — evaluate against general best practices."

        prompt = f"""Evaluate this educational content for BRAND compliance on a scale of 1-5.

## Rubric
1=Off-brand — wrong fonts, colors, voice, or structure
2=Partially aligned — some rules followed, noticeable inconsistencies
3=Adequate — most brand rules followed, minor deviations
4=Strong — consistent voice, formatting, and structure throughout
5=Unmistakable — perfect compliance with all brand guidelines

## Key Rules to Check
- Voice: clear, instructional, encouraging, semi-formal
- No end periods on paragraphs
- Max 30-40 words per slide/section
- Title Case for headings
- Code uses Fira Code font, 2-space indentation, VS Code Light+ theme
- No dark red color — use dark orange (#f79903) instead
- Green bullet points for listed points
- Blue (#006daf) for headings and highlights
- Orange (#ff9900) for code highlighting borders
- Analogy-first teaching pattern
- Recap → Agenda → Content → Key Takeaways structure
- Speaker notes present with presenter triggers
{brand_rules}

## Content to Evaluate
{content[:6000]}

## Context
Content Type: {content_type}
Domain: {context.get('domain', 'unknown')}

Check EACH brand rule systematically. Return JSON:
{{"score": 1-5, "evidence": "specific examples of compliance and violations", "failing_elements": ["list of specific brand violations found"]}}"""

        response = self._call_claude(
            prompt,
            system="You are a brand compliance auditor for an educational technology company. Check content against the brand playbook rules systematically.",
            model_tier="cheap",
        )
        return self._parse_score(response, self.dimension)
