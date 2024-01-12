from typing import Any, Optional

from pydantic import RedisDsn, ValidationInfo, field_validator
from pydantic_core import Url
from pydantic_settings import BaseSettings

from app.constants import Environment

# See https://github.com/zhanymkanov/fastapi-best-practices#10-use-pydantics-basesettings-for-configs


class Config(BaseSettings):
    """Application configuration, parsed from environment variables."""

    class Config:
        """Configurations for the pydantic BaseSettings."""

        env_file = ".env"
        env_file_encoding = "utf-8"

    ENVIRONMENT: Environment = Environment.PRODUCTION
    """The environment the application is running in."""

    REDIS: Optional[RedisDsn] = None
    """The Redis service to use for queueing, indexing and document storage."""

    EMBEDDING_MODEL: str = ""
    """The embedding model to use.

    This is a string of the form `<kind>[:<model>]` with the following options:

    1. `local[:<path or repository>]` -- Run a model locally. If this is a path
       it will attempt to load a model from that location. Otherwise, it should
       be a Hugging Face repository from which to retrieve the model.
    2. `openai[:<name>]` -- The named OpenAI model. `OPENAI_API_KEY` must be set.
    3. `ollama:<name>` -- The named Ollama model. `OLLAMA_BASE_URL` must be set.

    In each of these cases, you can omit the second part for the default model of the
    given kind.

    If unset, this will default to `"openai"` if an OpenAI API KEY is available and
    otherwise will use `"local"`.

    NOTE: Changing embedding models is not currently supported.
    """

    LLM_MODEL: str = ""
    """The LLM model to use.

    This is a string of the form `<kind>:<model>` with the following options:

    1. `local[:<path or repository>]` -- Run a model locally. If this is a path
       it will attempt to load a model from that location. Otherwise, it should
       be a Hugging Face repository from which to retrieve the model.
    2. `openai[:<name>]` -- The named OpenAI model. `OPENAI_API_KEY` must be set.
    3. `ollama:<name>` -- The named Ollama model. `OLLAMA_BASE_URL` must be set.

    In each of these cases, you can omit the second part for the default model of the
    given kind.

    If unset, this will default to `"openai"` if an OpenAI API KEY is available and
    otherwise will use `"local"`.
    """

    OPENAI_API_KEY: Optional[str] = None
    """ The OpenAI API Key to use for OpenAI models.

    This is required for using openai models.
    """

    OLLAMA_BASE_URL: Optional[Url] = None
    """The Base URL for Ollama.

    This is required for using ollama models.
    """

    @field_validator("OLLAMA_BASE_URL")
    def validate_ollama_base_url(cls, v, info: ValidationInfo):
        MODELS = ["LLM_MODEL", "EMBEDDING_MODEL"]
        if v is None:
            for model in MODELS:
                value = info.get(model, "")
                if value.startswith("ollama"):
                    raise ValueError(
                        f"{info.field_name} must be set to use '{model}={value}'"
                    )
        return v


settings = Config()

app_configs: dict[str, Any] = {
    "title": "Dewy Knowledge Base API",
}

if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None  # hide docs
