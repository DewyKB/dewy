from enum import Enum
from typing import List, Optional

import asyncpg
from pydantic import BaseModel

from dewy.domain._errors import NoSuchCollection, NoSuchDocument
from dewy.domain.chunks import _encode_chunk


class IngestState(Enum):
    PENDING = "pending"
    """Document is pending ingestion."""

    INGESTED = "ingested"
    """Document has been ingested."""

    FAILED = "failed"
    """Document failed to be ingested. See `ingest_errors` for details."""


class Document(BaseModel):
    """Model for documents in Dewy."""

    id: Optional[int] = None
    """The ID of the document."""

    collection: str
    """The collection containing the document."""

    extracted_text: Optional[str] = None
    """The text that was extracted for this document.

    This is only returned when getting a specific document, not listing documents.

    Will not be set until after the document is ingested.
    """

    url: Optional[str] = None
    """The URL of the document."""

    ingest_state: Optional[IngestState] = None
    ingest_error: Optional[str] = None


async def get_status(conn: asyncpg.Connection, document_id: int) -> IngestState:
    state = await conn.fetchval("SELECT ingest_state FROM document WHERE id = $1", document_id)
    return IngestState(state)


def _document_from_record(row: asyncpg.Record) -> Document:
    return Document(
        id=row["id"],
        collection=row["collection"],
        ingest_state=IngestState(row["ingest_state"]),
        ingest_error=row["ingest_error"],
        url=row["url"],
        extracted_text=row.get("extracted_text"),
    )


async def add_document(conn: asyncpg.Connection, collection: str, url: Optional[str]) -> Document:
    """Add a document to the database.

    This does not initiate any ingestion tasks.
    """
    try:
        row = await conn.fetchrow(
            """
            INSERT INTO document (collection_id, url, ingest_state)
            VALUES ((SELECT id FROM collection WHERE lower(name) = lower($1)), $2, 'pending')
            RETURNING id, collection_id, url, ingest_state, ingest_error, $1 AS collection
            """,
            collection,
            url,
        )
        return _document_from_record(row)
    except asyncpg.NotNullViolationError as e:
        if e.column_name == "collection_id":
            raise NoSuchCollection(collection)
        else:
            raise e from None


async def get_document(
    conn: asyncpg.Connection,
    document_id: int,
) -> Document:
    """Get the given document.

    Parameters:
    - conn: The connection to use for retrieval.
    - document_id: The document ID to retrieve.
    """
    row = await conn.fetchrow(
        """
        SELECT d.id, c.name AS collection, d.url, d.ingest_state, d.ingest_error, d.extracted_text
        FROM document d
        JOIN collection c ON d.collection_id = c.id
        WHERE d.id = $1
        """,
        document_id,
    )

    if not row:
        raise NoSuchDocument(document_id)

    return _document_from_record(row)


async def get_document_status(
    conn: asyncpg.Connection,
    document_id: int,
) -> Document:
    """Get the status of the given document.

    Parameters:
    - conn: The connection to use for retrieval.
    - document_id:  The document ID to retrieve.
    """

    row = await conn.fetchrow(
        """
        SELECT d.id, c.name AS collection, d.ingest_state, d.ingest_error
        FROM document d
        JOIN collection c ON d.collection_id = c.id
        WHERE d.id = $1
        """,
        document_id,
    )

    if not row:
        raise NoSuchDocument(document_id)

    return _document_from_record(row)


async def list_documents(
    conn: asyncpg.Connection, collection: Optional[str] = None
) -> List[Document]:
    results = await conn.fetch(
        """
        SELECT d.id, c.name AS collection, d.url, d.ingest_state, d.ingest_error
        FROM document d
        JOIN collection c ON c.id = d.collection_id
        WHERE lower(c.name) = coalesce(lower($1), lower(c.name))
        """,
        collection,
    )

    return [_document_from_record(row) for row in results]


async def update_status(
    conn: asyncpg.Connection,
    document_id: int,
    state: IngestState,
    extracted_text: Optional[str] = None,
    error: Optional[str] = None,
):
    await conn.execute(
        """
        UPDATE document
        SET
            ingest_state = $2,
            ingest_error = $3,
            extracted_text = $4
        WHERE id = $1
        """,
        document_id,
        state.value,
        error,
        _encode_chunk(extracted_text),
    )


async def delete(conn: asyncpg.Connection, document_id: int):
    """Delete a document.

    Raises:
    `NoSuchDocument` if no document with that ID is found.
    """

    deleted = await conn.fetchval(
        """
        DELETE FROM document
        WHERE id = $1
        RETURNING id
        """,
        document_id,
    )

    if deleted is None:
        raise NoSuchDocument(document_id)
