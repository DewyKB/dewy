import contextlib
import os
from pathlib import Path
from typing import AsyncIterator, Optional, TypedDict

import asyncpg
import click
import uvicorn
from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger

from dewy.common import db
from dewy.common.db_migration import apply_migrations
from dewy.config import APP_CONFIGS, ServeConfig
from dewy.routes import api_router


class State(TypedDict):
    pg_pool: Optional[asyncpg.Pool]


# Resolve paths, independent of PWD
current_file_path = Path(__file__).resolve()
react_build_path = current_file_path.parent / "frontend" / "dist"
migrations_path = current_file_path.parent / "migrations"


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[State]:
    """Function creating instances used during the lifespan of the service."""

    if app.config.db is not None:
        async with db.create_pool(app.config.db) as pg_pool:
            if app.config.apply_migrations:
                async with pg_pool.acquire() as conn:
                    await apply_migrations(conn, migration_dir=migrations_path)

            logger.info("Created database connection")
            state = State(pg_pool=pg_pool)
            yield state
    else:
        logger.warning("No database configured. CRUD methods will fail.")
        state = State(pg_pool=None)
        yield state


root_router = APIRouter()


@root_router.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


def install_middleware(app: FastAPI) -> None:
    origins = [
        "*",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


async def handle_postgres_error(_request: Request, exception: asyncpg.PostgresError):
    print(f"Error: {exception}")


def create_app(config: Optional[ServeConfig] = None) -> FastAPI:
    config = config or ServeConfig()
    app_configs = dict(APP_CONFIGS)
    if not config.serve_openapi_ui:
        app_configs["openapi_url"] = None  # hide docs

    app = FastAPI(lifespan=lifespan, **app_configs)

    # Make the configuration available
    app.config = config

    install_middleware(app)

    app.include_router(root_router)
    app.include_router(api_router)

    if config.serve_admin_ui:
        assert os.path.isdir(react_build_path), "Unable to serve admin UI without react build."

        logger.info("Running admin UI at http://localhost:8000/admin")
        # Serve static files from the React app build directory
        app.mount(
            "/admin",
            StaticFiles(directory=str(react_build_path), html=True),
            name="static",
        )

    app.add_exception_handler(asyncpg.PostgresError, handle_postgres_error)

    return app


@click.command()
@click.option(
    "-p",
    "--port",
    default=8000,
    type=click.IntRange(0, 49151),
    envvar="DEWY_PORT",
    show_envvar=True,
    help="TCP port to run on.",
)
@click.option(
    "--admin-ui/--no-admin-ui", default=True, help="If true, serve the Admin UI on `/admin`."
)
@click.option(
    "--openapi-ui/--no-openapi-ui",
    default=True,
    help="If true, serve the OpenAPI docs on `/docs`.",
)
@click.option(
    "--apply-migrations/--no-apply-migrations",
    default=True,
    help="If true, apply database migrations.",
)
@click.option(
    "--openai-api-key",
    envvar="OPENAI_API_KEY",
    show_envvar=True,
    help="The OpenAI API key to use.",
)
@click.pass_context
def serve(
    ctx,
    port: int = 8000,
    admin_ui: bool = True,
    openapi_ui: bool = True,
    apply_migrations: bool = True,
    openai_api_key: Optional[str] = None,
):
    """
    Serve the Dewy API and (if configured) Admin UI.
    """
    config = ServeConfig(
        db=ctx.obj["db"],
        serve_admin_ui=admin_ui,
        serve_openapi_ui=openapi_ui,
        apply_migrations=apply_migrations,
        openai_api_key=openai_api_key,
    )
    app = create_app(config)

    uvicorn.run(app, host="0.0.0.0", port=port)
