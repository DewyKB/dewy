import hashlib
import os
import re
from typing import Dict, Iterable, Optional, Tuple

import asyncpg
from loguru import logger


async def apply_migrations(
    conn: asyncpg.Connection, *, migration_dir: str = "migrations"
):
    """Applies the migrations to the database."""

    # TODO: For deployments, we may wish to make this a script that
    # can be executed, rather than always calling it on startup.

    # Ensure the migration table exists.
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS migration (
            -- Record the versions we have applied.
            id INTEGER NOT NULL,
            -- Record the SHA of the version so we can detect changes.
            sha256 TEXT,
            PRIMARY KEY (id)
        );
        """
    )

    defined_migrations = _get_defined_migrations(migration_dir)
    applied_migrations = await _get_applied_migrations(conn)

    applied = 0
    for migration_id, migration_file in defined_migrations:
        applied_sha256 = applied_migrations.pop(migration_id, None)
        if await _apply_migration(conn, migration_id, migration_file, applied_sha256):
            applied += 1

    if applied_migrations:
        logger.warn("Unrecognized migrations applied: {}", applied_migrations)

    logger.info(
        "Migrations complete. {} total, {} newly applied",
        len(defined_migrations),
        applied,
    )


MIGRATION_RE = re.compile(r"([0-9]{4})[a-zA-Z0-9_-]+\.sql")


def _get_defined_migrations(dir: str) -> Iterable[Tuple[int, str]]:
    files = {}
    for file in os.listdir(dir):
        match = MIGRATION_RE.fullmatch(file)
        if match:
            number = int(match.group(1))
            existing_file = files.setdefault(number, file)
            if existing_file != file:
                raise ValueError(
                    f"Multiple migrations for {number}: '{existing_file}' and '{file}'"
                )
        else:
            logger.warning(
                "File '{}' in migrations did not match migration naming '{}'",
                file,
                MIGRATION_RE.pattern,
            )
    return [(id, os.path.join(dir, file)) for (id, file) in sorted(files.items())]


async def _get_applied_migrations(conn: asyncpg.Connection) -> Dict[int, str]:
    applied = await conn.fetch("SELECT id, sha256 FROM migration ORDER BY id")
    return {row["id"]: row["sha256"] for row in applied}


async def _apply_migration(
    conn: asyncpg.Connection,
    migration_id: int,
    migration_path: str,
    applied_sha256: Optional[str],
) -> bool:
    """Apply the given migration if it hasn't already been applied.

    Uses `applied_sha256` to determine whether it has been applied.
    """
    # NOTE: Using the sha256 from the list means that other processes
    # may have applied the migration. If we expect to run the migrations
    # concurrently, we should have a more explicit locking. On the other
    # hand, in a "production" environment, we probably want to explicitly
    # apply the migrations, rather than having every node try to apply
    # them on startup -- so we could just run them as part of the deployment
    # script, which likely means we *don't* actually run these concurrently.

    with open(migration_path) as migration_file:
        migration_content = migration_file.read()

        pending_sha256 = hashlib.sha256(migration_content.encode("utf8")).hexdigest()

        async with conn.transaction():
            if pending_sha256 == applied_sha256:
                logger.debug(
                    "Migration '{}' already applied with sha {}",
                    migration_path,
                    pending_sha256,
                )
                return False
            elif applied_sha256 is not None:
                raise ValueError(
                    f"'{migration_path}' applied with different SHA. Recreate DB."
                )
            else:
                logger.info("Applying migration '{}'", migration_path)

            # Apply the migration.
            await conn.execute(migration_content)
            await conn.execute(
                "INSERT INTO migration (id, sha256) VALUES ($1, $2);",
                migration_id,
                pending_sha256,
            )

            return True
