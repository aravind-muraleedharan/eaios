"""One place to hold all configuration-related settings."""

from functools import lru_cache
from typing import Literal
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """ Application settings, loaded from environment varibales or a .env file"""

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_prefix = "EAIOS_",
        extra = "ignore",
    )

    app_name: str = "EAIOS"
    environment: Literal["development", "staging", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    # System prompts
    system_prompt_file: Path = Path("prompts/system.md")

    # Claude
    anthropic_api_key: SecretStr
    claude_model: str = "claude-haiku-5-5"
    claude_max_tokens: int = 128
    claude_timeout_sec: float = 30.0


@lru_cache
def get_settings() -> Settings:
    "Load settings once and reuse them"
    return Settings()



