import contextlib
from typing import AsyncIterator, TypedDict

from fastapi import FastAPI
from llama_index import StorageContext

from app.config import app_configs
from app.ingest.store import Store
from app.routes import api_router


class State(TypedDict):
    storage_context: StorageContext


@contextlib.asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[State]:
    """Function creating instances used during the lifespan of the service."""
    state = {"store": Store()}

    yield state


app = FastAPI(lifespan=lifespan, **app_configs)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(api_router)
