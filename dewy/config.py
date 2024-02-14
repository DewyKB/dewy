from typing import Annotated, Any, Optional

from fastapi import Depends, Request
from fastapi.routing import APIRoute
from pydantic import PostgresDsn
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

    DB: Optional[PostgresDsn] = None
    """The Postgres database to connect to.

    If not provided, none of the CRUD methods will work.
    """

    APPLY_MIGRATIONS: bool = True
    """Whether migrations should be applied to the database.

    This should be set to false if there are multiple services running to prevent
    concurrent migrations.
    """

    ENVIRONMENT: Environment = Environment.PRODUCTION
    """The environment the application is running in."""

    OPENAI_API_KEY: Optional[str] = None
    """ The OpenAI API Key to use for OpenAI models.

    This is required for using openai models.
    """

    def app_configs(self) -> dict[str, Any]:
        API_DESCRIPTION: str = """This API allows ingesting and retrieving knowledge.

        Knowledge comes in a variety of forms -- text, image, tables, etc. and
        from a variety of sources -- documents, web pages, audio, etc."""

        app_configs: dict[str, Any] = {
            "title": "Dewy Knowledge Base API",
            "version": "0.2.0",
            "summary": "Knowledge curation for Retrieval Augmented Generation",
            "description": API_DESCRIPTION,
            "servers": [
                {"url": "http://localhost:8000", "description": "Local server"},
            ],
            "generate_unique_id_function": custom_generate_unique_id_function,
        }

        if not self.ENVIRONMENT.is_debug:
            app_configs["openapi_url"] = None  # hide docs

        return app_configs


def convert_snake_case_to_camel_case(string: str) -> str:
    """Convert snake case to camel case"""

    words = string.split("_")
    return words[0] + "".join(word.title() for word in words[1:])


def custom_generate_unique_id_function(route: APIRoute) -> str:
    """Custom function to generate unique id for each endpoint"""

    return convert_snake_case_to_camel_case(route.name)


def _get_config(request: Request) -> Config:
    return request.app.config


ConfigDep = Annotated[Config, Depends(_get_config)]
