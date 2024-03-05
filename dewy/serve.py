import asyncio
import contextlib
import os
from pathlib import Path
from typing import Optional

import asyncpg
import click
from fastapi.responses import JSONResponse
import taskiq
import uvicorn
from fastapi import APIRouter, FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger

from dewy import domain
from dewy.common.db_migration import apply_migrations
from dewy.config import APP_CONFIGS, ServeConfig
from dewy.tasks import DewyTasks

# Resolve paths, independent of PWD
current_file_path = Path(__file__).resolve()
react_build_path = current_file_path.parent / "frontend" / "dist"
migrations_path = current_file_path.parent / "migrations"


async def _create_pg_pool(config: ServeConfig) -> Optional[asyncpg.Pool]:
    if config.db is None:
        logger.warning("No database configured. CRUD methods will fail.")
        return None
    else:
        pg_pool = await domain.database.create_pool(config.db)
        logger.info("Created database for {}", config.db)
        if config.apply_migrations:
            async with pg_pool.acquire() as conn:
                await apply_migrations(conn, migration_dir=migrations_path)
        else:
            logger.info("Skipping migrations.")
        return pg_pool


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    """Function creating instances used during the lifespan of the service."""

    pg_pool = await _create_pg_pool(app.config)

    state = {}
    state["pg_pool"] = pg_pool

    tasks = DewyTasks(pg_pool, app.config)
    broker = tasks.broker

    await broker.startup()

    state["tasks"] = tasks

    worker_task = None
    if not isinstance(broker, taskiq.InMemoryBroker):
        # Run a worker task locally.
        # Note - this is less robust than a true taskiq worker. We likely want to provide
        # an option to *only* run the worker the conventional way (with `taskiq` owning the
        # process).
        from taskiq.api import run_receiver_task

        worker_task = asyncio.create_task(run_receiver_task(app.broker))

    # Yield. Code after this will be teardown.
    yield state

    # Tear down.
    if worker_task:
        logger.info("Cancelling task queue")
        if worker_task.cancel():
            await worker_task

    if pg_pool:
        logger.info("Closing DB")
        await pg_pool.close()


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
    logger.exception("Postgres Error")
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={})


async def handle_dewy_error(_request, exception: domain.DewyError):
    logger.exception("Dewy Error")
    return JSONResponse(status_code=exception.status(), content={"detail": str(exception)})


def create_app(config: Optional[ServeConfig] = None) -> FastAPI:
    config = config or ServeConfig()

    app_configs = dict(APP_CONFIGS)
    if not config.serve_openapi_ui:
        app_configs["openapi_url"] = None  # hide docs

    app = FastAPI(lifespan=lifespan, **app_configs)

    # Make the configuration available
    app.config = config

    install_middleware(app)

    from dewy.backend import chunks_api, collections_api, documents_api

    app.include_router(root_router)

    api_router = APIRouter(prefix="/api")
    api_router.include_router(chunks_api.router, tags=["kb"])
    api_router.include_router(collections_api.router, tags=["kb"])
    api_router.include_router(documents_api.router, tags=["kb"])
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
    app.add_exception_handler(domain.DewyError, handle_dewy_error)

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
