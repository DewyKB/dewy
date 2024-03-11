from typing import Annotated, AsyncIterator

import asyncpg
from taskiq import TaskiqDepends

from dewy.config import ServeConfig


async def _connection(
    pg_pool: Annotated[asyncpg.Pool, TaskiqDepends()],
) -> AsyncIterator[asyncpg.Connection]:
    async with pg_pool.acquire() as connection:
        yield connection


PgConnectionDep = Annotated[asyncpg.Connection, TaskiqDepends(_connection)]

ServeConfigDep = Annotated[ServeConfig, TaskiqDepends()]
