from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.body_retrieve_chunks import BodyRetrieveChunks
from ...models.http_validation_error import HTTPValidationError
from ...models.retrieved_chunks import RetrievedChunks
from ...types import Response


def _get_kwargs(
    *,
    body: BodyRetrieveChunks,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/api/chunks/retrieve",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, RetrievedChunks]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = RetrievedChunks.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, RetrievedChunks]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: BodyRetrieveChunks,
) -> Response[Union[HTTPValidationError, RetrievedChunks]]:
    """Retrieve Chunks

     Retrieve chunks based on a given query.

    Args:
        body (BodyRetrieveChunks):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, RetrievedChunks]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: BodyRetrieveChunks,
) -> Optional[Union[HTTPValidationError, RetrievedChunks]]:
    """Retrieve Chunks

     Retrieve chunks based on a given query.

    Args:
        body (BodyRetrieveChunks):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, RetrievedChunks]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: BodyRetrieveChunks,
) -> Response[Union[HTTPValidationError, RetrievedChunks]]:
    """Retrieve Chunks

     Retrieve chunks based on a given query.

    Args:
        body (BodyRetrieveChunks):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, RetrievedChunks]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: BodyRetrieveChunks,
) -> Optional[Union[HTTPValidationError, RetrievedChunks]]:
    """Retrieve Chunks

     Retrieve chunks based on a given query.

    Args:
        body (BodyRetrieveChunks):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, RetrievedChunks]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
