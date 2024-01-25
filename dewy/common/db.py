import contextlib
from typing import Annotated, AsyncIterator

import asyncpg
from fastapi import Depends, Request


@contextlib.asynccontextmanager
async def create_pool(dsn: str) -> AsyncIterator[asyncpg.Pool]:
    """
    Create a postgres connection pool.

    Arguments:
    - dsn: Connection arguments specified using as a single string in
           the following format:
           `postgres://user:pass@host:port/database?option=value`.
    """

    async def init_pool(conn: asyncpg.Connection):
        # Need the extension before we register, so do this here.
        await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")

        from pgvector.asyncpg import register_vector

        await register_vector(conn)

    pool = await asyncpg.create_pool(dsn, init=init_pool)
    yield pool
    await pool.close()


def _pg_pool(request: Request) -> asyncpg.Pool:
    return request.state.pg_pool


PgPoolDep = Annotated[asyncpg.Pool, Depends(_pg_pool)]


async def _pg_connection(pool: PgPoolDep) -> asyncpg.Connection:
    async with pool.acquire() as connection:
        yield connection


PgConnectionDep = Annotated[asyncpg.Connection, Depends(_pg_connection)]
