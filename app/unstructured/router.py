from typing import Annotated

import llama_index
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from loguru import logger

from app.ingest.extract import ExtractSource, extract
from app.ingest.store import StoreDep
from app.unstructured.models import (
    NodeWithScore,
    RetrieveRequest,
    RetrieveResponse,
    TextNode,
)

router = APIRouter(tags=["unstructured"], prefix="/unstructured")


class Collection:
    def __init__(
        self,
        collection: Annotated[str, Path(..., description="the name of the collection")],
    ) -> None:
        self.collection = collection
        self.id = hash(collection)


PathCollection = Annotated[Collection, Depends()]


@router.put("/{collection}/documents", operation_id="add_document", tags=["collection"])
async def add_document_unstructured(
    store: StoreDep,
    # TODO: Use the collection.
    collection: PathCollection,
    url: Annotated[str, Body(..., description="The URL of the document to add.")],
):
    """Add a document to the unstructured collection.

    Parameters:
    - collection: The ID of the collection to add to.
    - document: The URL of the document to add.
    """

    # Load the content.
    logger.debug("Loading content from {}", url)
    documents = await extract(
        ExtractSource(
            url,
        )
    )
    logger.debug("Loaded {} pages from {}", len(documents), url)
    if not documents:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"No content retrieved from '{url}'",
        )

    logger.debug("Inserting {} documents from {}", len(documents), url)
    nodes = await store.ingestion_pipeline.arun(documents=documents)
    logger.debug("Done. Inserted {} nodes", len(nodes))


@router.delete("/{collection}/documents/{document}", operation_id="delete_document", tags=["collection"])
async def delete_document_unstructured(
    store: StoreDep, collection: PathCollection, document: str
):
    """Delete a document from the unstructured collection.

    Parameters:
    - collection: The ID of the collection to remove from.
    - document: The ID of the document to remove.
    """
    raise NotImplementedError()


class RetrieveParams:
    def __init__(
        self,
        query: Annotated[
            str, Query(..., description="The query string to use for retrieval")
        ],
        n: Annotated[
            int, Query(description="Number of document chunks to retrieve")
        ] = 10,
    ):
        self.query = query
        self.n = n


@router.post("/{collection}/retrieve", operation_id="retrieve", tags=["collection"])
async def retrieve_documents_unstructured(
    store: StoreDep, collection: PathCollection, request: RetrieveRequest
) -> RetrieveResponse:
    """Retrieve chunks based on a given query."""

    results = store.index.as_query_engine(
        similarity_top_k=request.n,
        response_mode=request.synthesis_mode.value,
        # TODO: metadata filters / ACLs
    ).query(request.query)

    retrieved_nodes = [convert_node(node) for node in results.source_nodes]
    return RetrieveResponse(
        synthesized_text=results.response,
        retrieved_nodes=retrieved_nodes,
    )


def convert_node(node: llama_index.schema.NodeWithScore) -> NodeWithScore:
    score = node.score
    node = node.node

    converted = None
    if isinstance(node, llama_index.schema.TextNode):
        converted = TextNode(
            text=node.text,
            start_char_idx=node.start_char_idx,
            end_char_idx=node.end_char_idx,
        )
    else:
        raise NotImplementedError(f"Conversion of {node!r} ({node.class_name})")
    return NodeWithScore(node=converted, score=score)
