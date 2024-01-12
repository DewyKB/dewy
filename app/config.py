from typing import Any, Optional

from pydantic import RedisDsn
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

    REDIS: Optional[RedisDsn] = None
    """The Redis service to use for queueing, indexing and document storage."""


settings = Config()

app_configs: dict[str, Any] = {
    "title": "Knowledge Bases API",
}

if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None  # hide docs
