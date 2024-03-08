from typing import Annotated, List, Union

import pydantic
from fastapi import APIRouter, Path, Query
from pydantic import BaseModel

from dewy.domain import chunks
from dewy.domain.chunks import ImageChunk, RetrievedChunks, TextChunk

from ._dependencies import PgConnectionDep, ServeConfigDep


class RetrieveRequest(BaseModel):
    """A request for retrieving chunks from a collection."""

    collection: str
    """The collection to retrieve chunks from."""

    query: str
    """The query string to use for retrieval."""

    n: int = 10
    """The number of chunks to retrieve."""

    # TODO: We may want an option which only excludes nodes included in the summary.
    # For instance -- if we summarize the text statements, maybe it only includes
    # images and tables in the response. But for now, this is a big switch to
    # exclude statements entirely.
    include_text_chunks: bool = True
    """Whether to include text chunks in the result.

    If this is false, no text chunks will be included in the result, although
    the summary (if enbaled) may include information from the chunks.
    """

    include_image_chunks: bool = True
    """Whether to include image chunks in the result.

    If this is false, no image chunks will be included in the result, although
    the summary (if enbaled) may include information from the chunks.
    """

    include_summary: bool = False
    """Whether to include a generated summary."""


router = APIRouter(prefix="/chunks")


@router.get("/")
async def list_chunks(
    conn: PgConnectionDep,
    collection: Annotated[
        str | None, Query(description="Limit to chunks associated with this collection")
    ] = None,
    document_id: Annotated[
        int | None, Query(description="Limit to chunks associated with this document")
    ] = None,
    page: Annotated[
        int | None, Query(description="Page number to fetch. The first page of results is page 1")
    ] = 1,
    perPage: int | None = 10,
) -> List[
    Annotated[Union[chunks.TextChunk, chunks.ImageChunk], pydantic.Field(discriminator="kind")]
]:
    """List chunks."""

    # TODO: Allow multiple document IDs?
    perPage = perPage or 10
    page = page or 1

    result = await chunks.list_chunks(
        conn,
        collection=collection,
        offset=(page - 1) * perPage,
        limit=perPage,
        document_ids=[document_id] if document_id else None,
    )
    return result


@router.get("/{id}")
async def get_chunk(
    conn: PgConnectionDep,
    id: Annotated[int, Path(..., description="The chunk ID.")],
) -> Annotated[Union[TextChunk, ImageChunk], pydantic.Field(discriminator="kind")]:
    return await chunks.get_chunk(conn, id)


@router.post("/retrieve")
async def retrieve_chunks(
    request: RetrieveRequest,
    conn: PgConnectionDep,
    config: ServeConfigDep,
) -> RetrievedChunks:
    """Retrieve chunks based on a given query."""

    return await chunks.retrieve_chunks(
        conn,
        config,
        collection=request.collection,
        query=request.query,
        limit=request.n,
        include_text_chunks=request.include_text_chunks,
    )
