"""One place to hold all configuration-related settings."""

from functools import lru_cache
from typing import Literal
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


@lru_cache
def get_settings() -> Settings:
    "Load settings once and reuse them"
    return Settings()



