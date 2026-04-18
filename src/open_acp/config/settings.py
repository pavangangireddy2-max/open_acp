"""AppSettings via pydantic-settings — loads from .env."""
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    openrouter_api_key: str = ""
    model_provider: str = "auto"
    openai_model_strong: str = "gpt-5"
    openai_model_cheap: str = "gpt-5-mini"
    openai_base_url: str = "https://api.openai.com/v1"
    openrouter_model_strong: str = "openai/gpt-5.4-pro"
    openrouter_model_cheap: str = "openai/gpt-5.4"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    continue_config_path: str = "~/.continue/config.yaml"
    log_level: str = "INFO"
    auto_approve_gates: bool = False
    default_domain: str = "ml-engineering"
    wiki_enabled: bool = True

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


def get_settings() -> AppSettings:
    return AppSettings()
