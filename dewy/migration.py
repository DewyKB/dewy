import click

from dewy.async_command import async_command
from dewy.common.db import create_pool
from dewy.common.db_migration import apply_migrations
from loguru import logger

@click.command()
@click.pass_context
@async_command
async def migrate(ctx):
    db = ctx.obj["db"]
    if db is None:
        raise ValueError(f"Must set `db` to apply migrations.")
    logger.info("Connectiong to {}", db)
    async with create_pool(db) as pool:
        logger.info("Applying migrations to {}", db)
        await apply_migrations(pool)
    logger.info("Applied migrations to {}", db)