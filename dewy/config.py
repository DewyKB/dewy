from typing import Any, Optional

from fastapi.routing import APIRoute
from pydantic import PostgresDsn, RedisDsn, ValidationInfo, field_validator
from pydantic_core import Url
from pydantic_settings import BaseSettings, SettingsConfigDict

from dewy.constants import Environment

# See https://github.com/zhanymkanov/fastapi-best-practices#10-use-pydantics-basesettings-for-configs


class Config(BaseSettings):
    """Application configuration, parsed from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    SERVE_ADMIN_UI: bool = True
    """If true, serve the admin UI."""

    DB: PostgresDsn
    """The Postgres database to connect to."""

    APPLY_MIGRATIONS: bool = True
    """Whether migrations should be applied to the database.

    This should be set to false if there are multiple services running to prevent
    concurrent migrations.
    """

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
                context = info.context
                if context:
                    value = context.get(model, "")
                    if value.startswith("ollama"):
                        raise ValueError(
                            f"{info.field_name} must be set to use '{model}={value}'"
                        )
        return v


settings = Config()


def convert_snake_case_to_camel_case(string: str) -> str:
    """Convert snake case to camel case"""

    words = string.split("_")
    return words[0] + "".join(word.title() for word in words[1:])


def custom_generate_unique_id_function(route: APIRoute) -> str:
    """Custom function to generate unique id for each endpoint"""

    return convert_snake_case_to_camel_case(route.name)


API_DESCRIPTION: str = """This API allows ingesting and retrieving knowledge.

Knowledge comes in a variety of forms -- text, image, tables, etc. and
from a variety of sources -- documents, web pages, audio, etc.
"""

app_configs: dict[str, Any] = {
    "title": "Dewy Knowledge Base API",
    "summary": "Knowledge curation for Retrieval Augmented Generation",
    "description": API_DESCRIPTION,
    "servers": [
        {"url": "http://localhost:8000", "description": "Local server"},
    ],
    "generate_unique_id_function": custom_generate_unique_id_function,
}

if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None  # hide docs
