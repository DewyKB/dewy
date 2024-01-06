from typing import Any

from pydantic_settings import BaseSettings

from app.constants import Environment

# See https://github.com/zhanymkanov/fastapi-best-practices#10-use-pydantics-basesettings-for-configs

class Config(BaseSettings):
    """Application configuration, parsed from environment variables."""

    class Config:
        """Configurations for the pydantic BaseSettings."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "KB_"

    ENVIRONMENT: Environment = Environment.PRODUCTION
    """The environment the application is running in."""

settings = Config()

app_configs: dict[str, Any] = {
    "title": "Knowledge Bases API",
}

if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None  # hide docs
