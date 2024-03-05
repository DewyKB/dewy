import asyncpg


async def create_pool(dsn: str) -> asyncpg.Pool:
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
    return pool
