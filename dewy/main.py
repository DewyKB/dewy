import contextlib
import os
from pathlib import Path
from typing import AsyncIterator, Optional, TypedDict

import asyncpg
import uvicorn
from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger

from dewy.common import db
from dewy.common.db_migration import apply_migrations
from dewy.config import Config
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

    if app.config.DB is not None:
        async with db.create_pool(app.config.DB.unicode_string()) as pg_pool:
            if app.config.APPLY_MIGRATIONS:
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


async def handle_postgres_error(request: Request, exception: asyncpg.PostgresError):
    print("Error: {exception}")


def create_app(config: Optional[Config] = None) -> FastAPI:
    config = config or Config()
    app = FastAPI(lifespan=lifespan, **config.app_configs())
    app.config = config

    install_middleware(app)

    app.include_router(root_router)
    app.include_router(api_router)

    if config.SERVE_ADMIN_UI and os.path.isdir(react_build_path):
        logger.info("Running admin UI at http://localhost:8000/admin")
        # Serve static files from the React app build directory
        app.mount(
            "/admin",
            StaticFiles(directory=str(react_build_path), html=True),
            name="static",
        )

    app.add_exception_handler(asyncpg.PostgresError, handle_postgres_error)

    return app


# Function for running Dewy as a script
def run(*args):
    uvicorn.run("dewy.main:create_app", host="0.0.0.0", port=8000)
