"""Coding challenge generator — generates coding problems with test cases."""
from open_acp.config.settings import get_settings
from open_acp.tools.base_tool import BaseTool, ToolResult, ToolTier, ToolStatus


class CodingChallenge(BaseTool):
    name = "coding_challenge"
    capability = "assessment"
    provider = "claude"
    tier = ToolTier.STRONG
    cost_per_call = 0.02
    description = "Generate coding problems with starter code, test cases, and solutions"
    agent_skills = ["claude_api_patterns"]

    def execute(self, **kwargs) -> ToolResult:
        prompt = kwargs.get("prompt", "")
        system = kwargs.get("system", "You are an expert coding challenge designer.")
        model_tier = kwargs.get("model_tier", "strong")
        max_tokens = kwargs.get("max_tokens", 8192)

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
