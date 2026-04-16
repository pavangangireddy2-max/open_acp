"""AppSettings via pydantic-settings — loads from .env."""
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    model_provider: str = "auto"
    openai_model_strong: str = "gpt-5"
    openai_model_cheap: str = "gpt-5-mini"
    openai_base_url: str = "https://api.openai.com/v1"
    log_level: str = "INFO"
    auto_approve_gates: bool = False
    default_domain: str = "ml-engineering"
    wiki_enabled: bool = True

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


def get_settings() -> AppSettings:
    return AppSettings()
