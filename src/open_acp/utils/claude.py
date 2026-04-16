"""Model client wrapper with Anthropic + OpenAI fallback support."""
from __future__ import annotations

from typing import Optional

import anthropic
import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from open_acp.config.constants import (
    ANTHROPIC_CHEAP_MODEL,
    ANTHROPIC_STRONG_MODEL,
    API_MAX_RETRIES,
    API_RETRY_BACKOFF,
)
from open_acp.config.settings import get_settings


class OpenAIRetryableError(Exception):
    """Raised for transient OpenAI transport or rate-limit failures."""


class ClaudeClient:
    """Backward-compatible text generation client with provider fallback.

    The class name stays the same to avoid invasive repo-wide renames, but it can
    now call either Anthropic or OpenAI depending on configuration.
    """

    def __init__(self):
        settings = get_settings()
        self.settings = settings
        self.anthropic_api_key = settings.anthropic_api_key
        self.openai_api_key = settings.openai_api_key
        self.model_provider = (settings.model_provider or "auto").strip().lower()
        self.openai_base_url = settings.openai_base_url.rstrip("/")
        self.openai_model_strong = settings.openai_model_strong
        self.openai_model_cheap = settings.openai_model_cheap
        self._provider_override: Optional[str] = None
        self.anthropic_client: Optional[anthropic.Anthropic] = None

        if self.anthropic_api_key:
            self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_api_key)

    def generate(
        self,
        prompt: str,
        system: str = "",
        model_tier: str = "strong",
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        """Generate text using the configured provider, with fallback support."""
        provider = self._resolve_provider()

        if provider == "openai":
            return self._generate_openai(
                prompt=prompt,
                system=system,
                model_tier=model_tier,
                max_tokens=max_tokens,
                temperature=temperature,
            )

        try:
            return self._generate_anthropic(
                prompt=prompt,
                system=system,
                model_tier=model_tier,
                max_tokens=max_tokens,
                temperature=temperature,
            )
        except Exception as exc:
            if self._should_fallback_to_openai(exc):
                self._provider_override = "openai"
                return self._generate_openai(
                    prompt=prompt,
                    system=system,
                    model_tier=model_tier,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
            raise

    def active_provider(self) -> str:
        """Expose the currently selected provider for diagnostics."""
        return self._resolve_provider()

    def _resolve_provider(self) -> str:
        if self._provider_override:
            return self._provider_override

        if self.model_provider == "openai":
            if not self.openai_api_key:
                raise RuntimeError("MODEL_PROVIDER=openai but OPENAI_API_KEY is missing.")
            return "openai"

        if self.model_provider == "anthropic":
            if not self.anthropic_api_key:
                raise RuntimeError("MODEL_PROVIDER=anthropic but ANTHROPIC_API_KEY is missing.")
            return "anthropic"

        if self.anthropic_api_key:
            return "anthropic"
        if self.openai_api_key:
            return "openai"

        raise RuntimeError("No model API key configured. Set ANTHROPIC_API_KEY or OPENAI_API_KEY.")

    @retry(
        stop=stop_after_attempt(API_MAX_RETRIES),
        wait=wait_exponential(multiplier=API_RETRY_BACKOFF, min=1, max=30),
        retry=retry_if_exception_type((anthropic.RateLimitError, anthropic.APIConnectionError)),
        reraise=True,
    )
    def _generate_anthropic(
        self,
        prompt: str,
        system: str,
        model_tier: str,
        max_tokens: int,
        temperature: float,
    ) -> str:
        if not self.anthropic_client:
            raise RuntimeError("ANTHROPIC_API_KEY is missing.")

        model = ANTHROPIC_STRONG_MODEL if model_tier == "strong" else ANTHROPIC_CHEAP_MODEL
        messages = [{"role": "user", "content": prompt}]

        kwargs = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": messages,
            "temperature": temperature,
        }
        if system:
            kwargs["system"] = system

        response = self.anthropic_client.messages.create(**kwargs)
        return response.content[0].text

    @retry(
        stop=stop_after_attempt(API_MAX_RETRIES),
        wait=wait_exponential(multiplier=API_RETRY_BACKOFF, min=1, max=30),
        retry=retry_if_exception_type((OpenAIRetryableError, httpx.TransportError)),
        reraise=True,
    )
    def _generate_openai(
        self,
        prompt: str,
        system: str,
        model_tier: str,
        max_tokens: int,
        temperature: float,
    ) -> str:
        if not self.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is missing.")

        model = self.openai_model_strong if model_tier == "strong" else self.openai_model_cheap
        payload = {
            "model": model,
            "input": prompt,
            "max_output_tokens": max_tokens,
            "store": False,
        }
        if system:
            payload["instructions"] = system
        if self._supports_temperature(model):
            payload["temperature"] = temperature

        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json",
        }

        with httpx.Client(timeout=120.0) as client:
            response = client.post(f"{self.openai_base_url}/responses", headers=headers, json=payload)

        if response.status_code in {429, 500, 502, 503, 504}:
            raise OpenAIRetryableError(self._format_openai_error(response))

        if response.is_error:
            raise RuntimeError(self._format_openai_error(response))

        data = response.json()
        text = self._extract_openai_text(data)
        if not text:
            raise RuntimeError("OpenAI response did not contain output text.")
        return text

    def _should_fallback_to_openai(self, exc: Exception) -> bool:
        if self.model_provider != "auto" or not self.openai_api_key:
            return False

        message = str(exc).lower()
        anthropic_low_credit_markers = [
            "credit balance is too low",
            "plans & billing",
            "purchase credits",
        ]
        return any(marker in message for marker in anthropic_low_credit_markers)

    @staticmethod
    def _extract_openai_text(data: dict) -> str:
        if isinstance(data.get("output_text"), str) and data["output_text"].strip():
            return data["output_text"].strip()

        texts: list[str] = []
        for item in data.get("output", []):
            if item.get("type") == "message":
                for content in item.get("content", []):
                    if content.get("type") in {"output_text", "text"} and content.get("text"):
                        texts.append(content["text"])
            elif item.get("type") in {"output_text", "text"} and item.get("text"):
                texts.append(item["text"])

        if texts:
            return "\n".join(part.strip() for part in texts if part.strip()).strip()
        return ""

    @staticmethod
    def _format_openai_error(response: httpx.Response) -> str:
        try:
            data = response.json()
        except ValueError:
            return f"OpenAI API error {response.status_code}: {response.text}"

        error = data.get("error", {})
        if isinstance(error, dict):
            message = error.get("message") or error.get("type") or str(error)
        else:
            message = str(error)
        return f"OpenAI API error {response.status_code}: {message}"

    @staticmethod
    def _supports_temperature(model: str) -> bool:
        normalized = model.strip().lower()
        return not normalized.startswith("gpt-5")
