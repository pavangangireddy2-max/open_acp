"""AppSettings via pydantic-settings — loads from .env."""
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    anthropic_api_key: str = ""
    log_level: str = "INFO"
    auto_approve_gates: bool = False
    default_domain: str = "ml-engineering"
    wiki_enabled: bool = True

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


def get_settings() -> AppSettings:
    return AppSettings()
