from typing import Union

from loguru import logger

from dewy.domain import chunks, documents
from ._dependencies import PgConnectionDep, ServeConfigDep
from dewy.domain.ingest import IngestContent, IngestURL, ingest


async def ingest_task(
    document_id: int,
    request: Union[IngestContent, IngestURL],
    conn: PgConnectionDep,
    config: ServeConfigDep,
):
    try:
        await ingest(document_id, request, conn, config)
    except Exception as e:
        logger.exception("Failed to ingest")
        async with conn.transaction():
            await chunks.remove_chunks_for_document(conn, document_id)
            await documents.update_status(
                conn, document_id, documents.IngestState.FAILED, error=str(e)
            )
