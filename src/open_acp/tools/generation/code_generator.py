"""Code generator — generates code snippets and solutions."""
from open_acp.tools.base_tool import BaseTool, ToolResult, ToolTier, ToolStatus
import os


class CodeGenerator(BaseTool):
    name = "code_generator"
    capability = "generation"
    provider = "claude"
    tier = ToolTier.STRONG
    cost_per_call = 0.02
    description = "Generate code snippets, solutions, and starter code"
    agent_skills = ["claude_api_patterns"]

    def execute(self, **kwargs) -> ToolResult:
        prompt = kwargs.get("prompt", "")
        system = kwargs.get("system", "You are an expert programmer generating clean, well-documented code.")
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
        return ToolStatus.AVAILABLE if os.environ.get("ANTHROPIC_API_KEY") else ToolStatus.UNAVAILABLE
