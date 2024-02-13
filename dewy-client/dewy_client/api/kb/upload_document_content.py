from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.body_upload_document_content import BodyUploadDocumentContent
from ...models.document import Document
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    document_id: int,
    *,
    body: BodyUploadDocumentContent,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/api/documents/{document_id}/content",
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Document, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Document.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Document, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    document_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: BodyUploadDocumentContent,
) -> Response[Union[Document, HTTPValidationError]]:
    """Upload Document Content

     Add a document from specific content.

    Args:
        document_id (int): The collection to add the document to.
        body (BodyUploadDocumentContent):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Document, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        document_id=document_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    document_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: BodyUploadDocumentContent,
) -> Optional[Union[Document, HTTPValidationError]]:
    """Upload Document Content

     Add a document from specific content.

    Args:
        document_id (int): The collection to add the document to.
        body (BodyUploadDocumentContent):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Document, HTTPValidationError]
    """

    return sync_detailed(
        document_id=document_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    document_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: BodyUploadDocumentContent,
) -> Response[Union[Document, HTTPValidationError]]:
    """Upload Document Content

     Add a document from specific content.

    Args:
        document_id (int): The collection to add the document to.
        body (BodyUploadDocumentContent):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Document, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        document_id=document_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    document_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: BodyUploadDocumentContent,
) -> Optional[Union[Document, HTTPValidationError]]:
    """Upload Document Content

     Add a document from specific content.

    Args:
        document_id (int): The collection to add the document to.
        body (BodyUploadDocumentContent):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Document, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            document_id=document_id,
            client=client,
            body=body,
        )
    ).parsed
