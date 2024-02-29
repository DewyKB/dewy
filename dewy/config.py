from dataclasses import dataclass
from typing import Annotated, Any, Optional

from fastapi import Depends, Request
from fastapi.routing import APIRoute

# See https://github.com/zhanymkanov/fastapi-best-practices#10-use-pydantics-basesettings-for-configs

API_DESCRIPTION: str = """This API allows ingesting and retrieving knowledge.

Knowledge comes in a variety of forms -- text, image, tables, etc. and
from a variety of sources -- documents, web pages, audio, etc."""

def convert_snake_case_to_camel_case(string: str) -> str:
    """Convert snake case to camel case"""

    words = string.split("_")
    return words[0] + "".join(word.title() for word in words[1:])


def custom_generate_unique_id_function(route: APIRoute) -> str:
    """Custom function to generate unique id for each endpoint"""

    return convert_snake_case_to_camel_case(route.name)

APP_CONFIGS: dict[str, Any] = {
    "title": "Dewy Knowledge Base API",
    "version": "0.3.0",
    "summary": "Knowledge curation for Retrieval Augmented Generation",
    "description": API_DESCRIPTION,
    "servers": [
        {"url": "http://localhost:8000", "description": "Local server"},
    ],
    "generate_unique_id_function": custom_generate_unique_id_function,
}

@dataclass
class ServeConfig:
    """The configuration for the Dewy Service."""
    db: Optional[str] = None
    serve_openapi_ui: bool = True
    serve_admin_ui: bool = True
    apply_migrations: bool = True
    openai_api_key: Optional[str] = None

def _get_config(request: Request) -> ServeConfig:
    return request.app.config

ConfigDep = Annotated[ServeConfig, Depends(_get_config)]