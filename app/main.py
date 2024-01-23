import contextlib
from typing import AsyncIterator, TypedDict

import asyncpg
from fastapi import FastAPI

from app.collections.models import EmbeddingModel
from app.common import db
from app.config import app_configs, settings
from app.ingest.store import Store
from app.routes import api_router


class State(TypedDict):
    store: Store
    pg_pool: asyncpg.Pool


@contextlib.asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[State]:
    """Function creating instances used during the lifespan of the service."""

    # TODO: Look at https://gist.github.com/mattbillenstein/270a4d44cbdcb181ac2ed58526ae137d
    # for simple migration scripts.
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
