from typing import Union

from fastapi import APIRouter
from llama_index.schema import NodeWithScore
from loguru import logger

from app.ingest.store import StoreDep

from .models import ImageStatement, RetrieveRequest, RetrieveResponse, TextStatement

router = APIRouter(tags=["statements"], prefix="/statements")


@router.post("/retrieve")
async def retrieve(store: StoreDep, request: RetrieveRequest) -> RetrieveResponse:
    """Retrieve statements based on a given query."""

    from llama_index.response_synthesizers import ResponseMode

    logger.info("Retrieving statements for query:", request)
    results = store.index.as_query_engine(
        similarity_top_k=request.n,
        response_mode=ResponseMode.TREE_SUMMARIZE
        if request.include_summary
        else ResponseMode.NO_TEXT,
        # TODO: metadata filters / ACLs
    ).query(request.query)

    statements = [node_to_statement(node) for node in results.source_nodes]

    return RetrieveResponse(
        summary=results.response,
        statements=statements if request.include_statements else [],
    )


def node_to_statement(node: NodeWithScore) -> Union[TextStatement, ImageStatement]:
    from llama_index.schema import ImageNode, TextNode

    if isinstance(node.node, TextNode):
        return TextStatement(
            raw=True,
            score=node.score,
            text=node.node.text,
            start_char_idx=node.node.start_char_idx,
            end_char_idx=node.node.end_char_idx,
        )
    elif isinstance(node.node, ImageNode):
        return ImageStatement(
            score=node.score,
            text=node.node.text if node.node.text else None,
            image=node.node.image,
            image_mimetype=node.node.image_mimetype,
            image_path=node.node.image_path,
            image_url=node.node.image_url,
        )
    else:
        raise NotImplementedError(
            f"Unsupported node type ({node.node.class_name()}): {node!r}"
        )
