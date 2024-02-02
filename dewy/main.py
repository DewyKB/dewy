import contextlib
import os
from pathlib import Path
from typing import AsyncIterator, Optional, TypedDict

import asyncpg
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger

from dewy.common import db
from dewy.common.db_migration import apply_migrations
from dewy.config import app_configs, settings
from dewy.routes import api_router


class State(TypedDict):
    pg_pool: Optional[asyncpg.Pool]


# Resolve paths, independent of PWD
current_file_path = Path(__file__).resolve()
react_build_path = current_file_path.parent / "frontend" / "dist"
migrations_path = current_file_path.parent / "migrations"


@contextlib.asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[State]:
    """Function creating instances used during the lifespan of the service."""

    if settings.DB is not None:
        async with db.create_pool(settings.DB.unicode_string()) as pg_pool:
            if settings.APPLY_MIGRATIONS:
                async with pg_pool.acquire() as conn:
                    await apply_migrations(conn, migration_dir=migrations_path)

            logger.info("Created database connection")
            state = State(pg_pool=pg_pool)
            yield state
    else:
        logger.warning("No database configured. CRUD methods will fail.")
        state = State(pg_pool=None)
        yield state


app = FastAPI(lifespan=lifespan, **app_configs)

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


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(api_router)

if settings.SERVE_ADMIN_UI and os.path.isdir(react_build_path):
    logger.info("Running admin UI at http://localhost:8000/admin")
    # Serve static files from the React app build directory
    app.mount(
        "/admin", StaticFiles(directory=str(react_build_path), html=True), name="static"
    )


# Function for running Dewy as a script
def run(*args):
    uvicorn.run("dewy.main:app", host="0.0.0.0", port=8000)
