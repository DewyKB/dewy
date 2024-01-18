import contextlib
from typing import Annotated, AsyncIterator, TypedDict

from fastapi import Depends, FastAPI, Request
from fastapi.routing import APIRoute
from llama_index import StorageContext
from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine

from app.config import app_configs, settings
from app.ingest.store import Store
from app.routes import api_router


class State(TypedDict):
    store: Store
    db: Engine

@contextlib.asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[State]:
    """Function creating instances used during the lifespan of the service."""
    engine = create_engine(settings.DB, echo=True)
    SQLModel.metadata.create_all(engine)

    state = {
        "store": Store(),
        "engine": engine,
    }

    yield state

app = FastAPI(
    lifespan=lifespan,
    **app_configs)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(api_router)
