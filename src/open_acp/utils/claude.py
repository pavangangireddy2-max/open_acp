"""ClaudeClient — wrapper around the Anthropic SDK with retry logic."""
from typing import Optional

import anthropic
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from open_acp.config.constants import STRONG_MODEL, CHEAP_MODEL, API_MAX_RETRIES, API_RETRY_BACKOFF
from open_acp.config.settings import get_settings


class ClaudeClient:
    """Thin wrapper around anthropic.Anthropic with retry and model tier selection."""

    def __init__(self):
        settings = get_settings()
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    @retry(
        stop=stop_after_attempt(API_MAX_RETRIES),
        wait=wait_exponential(multiplier=API_RETRY_BACKOFF, min=1, max=30),
        retry=retry_if_exception_type((anthropic.RateLimitError, anthropic.APIConnectionError)),
        reraise=True,
    )
    def generate(
        self,
        prompt: str,
        system: str = "",
        model_tier: str = "strong",
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        """Generate text using Claude."""
        model = STRONG_MODEL if model_tier == "strong" else CHEAP_MODEL
        messages = [{"role": "user", "content": prompt}]

        kwargs = {"model": model, "max_tokens": max_tokens, "messages": messages, "temperature": temperature}
        if system:
            kwargs["system"] = system

        response = self.client.messages.create(**kwargs)
        return response.content[0].text
