"""ClaudeGenerate tool — wraps ClaudeClient for text generation."""
import time

from open_acp.config.settings import get_settings
from open_acp.tools.base_tool import BaseTool, ToolResult, ToolStatus, ToolTier
from open_acp.utils.claude import ClaudeClient, _load_continue_openrouter_config


class ClaudeGenerate(BaseTool):
    """Generate text content using the configured model provider."""

    name = "claude_generate"
    capability = "generation"
    provider = "claude"
    tier = ToolTier.STRONG
    cost_per_call = 0.02
    agent_skills = ["claude_api_patterns"]
    description = "Generate text content using Claude API"

    def execute(self, **kwargs) -> ToolResult:
        """Generate text via ClaudeClient.

        Args:
            prompt: The user prompt to send.
            system: Optional system prompt.
            model_tier: "strong" or "cheap" (default "strong").
            max_tokens: Maximum tokens in the response (default 4096).
        """
        prompt: str = kwargs.get("prompt", "")
        system: str = kwargs.get("system", "")
        model_tier: str = kwargs.get("model_tier", "strong")
        max_tokens: int = kwargs.get("max_tokens", 4096)

        if not prompt:
            return ToolResult(success=False, error="prompt is required")

        try:
            start = time.time()
            client = ClaudeClient()
            response_text = client.generate(
                prompt=prompt,
                system=system,
                model_tier=model_tier,
                max_tokens=max_tokens,
            )
            duration = time.time() - start

            return ToolResult(
                success=True,
                data={"text": response_text},
                cost_usd=self.cost_per_call,
                duration_seconds=round(duration, 2),
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))

    def get_status(self) -> ToolStatus:
        """Check whether any supported model provider key is set."""
        settings = get_settings()
        continue_openrouter = _load_continue_openrouter_config(settings.continue_config_path)
        if (
            settings.anthropic_api_key
            or settings.openai_api_key
            or settings.openrouter_api_key
            or continue_openrouter.get("api_key")
        ):
            return ToolStatus.AVAILABLE
        return ToolStatus.UNAVAILABLE
