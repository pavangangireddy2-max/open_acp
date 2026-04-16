"""Rubric builder — generates assessment rubrics from learning objectives."""
from open_acp.config.settings import get_settings
from open_acp.tools.base_tool import BaseTool, ToolResult, ToolTier, ToolStatus


class RubricBuilder(BaseTool):
    name = "rubric_builder"
    capability = "assessment"
    provider = "claude"
    tier = ToolTier.CHEAP
    cost_per_call = 0.005
    description = "Generate assessment rubrics from learning objectives"
    agent_skills = ["claude_api_patterns"]

    def execute(self, **kwargs) -> ToolResult:
        prompt = kwargs.get("prompt", "")
        system = kwargs.get("system", "You are an assessment rubric specialist.")
        model_tier = kwargs.get("model_tier", "cheap")
        max_tokens = kwargs.get("max_tokens", 4096)

        try:
            from open_acp.utils.claude import ClaudeClient
            client = ClaudeClient()
            response = client.generate(prompt=prompt, system=system, model_tier=model_tier, max_tokens=max_tokens)
            return ToolResult(success=True, data={"text": response})
        except Exception as e:
            return ToolResult(success=False, error=str(e))

    def get_status(self) -> ToolStatus:
        settings = get_settings()
        if settings.anthropic_api_key or settings.openai_api_key:
            return ToolStatus.AVAILABLE
        return ToolStatus.UNAVAILABLE
