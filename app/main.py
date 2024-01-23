import contextlib
from typing import AsyncIterator, TypedDict

from fastapi import FastAPI
from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine
from loguru import logger

from app.common import db
from app.config import app_configs, settings
from app.ingest.store import Store
from app.routes import api_router


class State(TypedDict):
    store: Store
    db: Engine


@contextlib.asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[State]:
    """Function creating instances used during the lifespan of the service."""

    # if settings.APPLY_MIGRATIONS:
        # from yoyo import get_backend, read_migrations
        # backend = get_backend(settings.DB.unicode_string())
        # migrations = read_migrations('migrations')
        # with backend.lock():
        #     outstanding = backend.to_apply(migrations)

        #     logger.info("Applying {} migrations", len(outstanding))

        #     # Apply any outstanding migrations
        #     backend.apply_migrations(outstanding)

        #     logger.info("Done applying migrations.")

    async with db.create_pool(settings.DB.unicode_string()) as pg_pool:
        if settings.APPLY_MIGRATIONS:
            async with pg_pool.acquire() as conn:
                with open("migrations/0001_schema.sql") as schema_file:
                    schema = schema_file.read()
                    await conn.execute(schema)
        state = {
            "store": Store(),
            "pg_pool": pg_pool,
        }

        yield state


app = FastAPI(lifespan=lifespan, **app_configs)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(api_router)
