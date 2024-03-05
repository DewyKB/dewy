from typing import Annotated, AsyncIterator

import asyncpg
from fastapi import Depends, Request
from dewy.config import ServeConfig

from dewy.tasks.dewy_tasks import DewyTasks


async def _pg_connection(request: Request) -> AsyncIterator[asyncpg.Connection]:
    pg_pool = request.state.pg_pool
    if pg_pool is None:
        raise ValueError("DB not configured. Unable to get pool.")
    async with pg_pool.acquire() as connection:
        yield connection


PgConnectionDep = Annotated[asyncpg.Connection, Depends(_pg_connection)]


async def _dewy_tasks(request: Request) -> DewyTasks:
    return request.state.tasks


DewyTasksDep = Annotated[DewyTasks, Depends(_dewy_tasks)]

def _get_config(request: Request) -> ServeConfig:
    return request.app.config


ServeConfigDep = Annotated[ServeConfig, Depends(_get_config)]
