from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.document import Document
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    collection: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_collection: Union[None, Unset, str]
    if isinstance(collection, Unset):
        json_collection = UNSET
    else:
        json_collection = collection
    params["collection"] = json_collection

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/documents/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, List["Document"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Document.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Union[HTTPValidationError, List["Document"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    collection: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, List["Document"]]]:
    """List Documents

     List documents.

    Args:
        collection (Union[None, Unset, str]): Limit to documents associated with this collection

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, List['Document']]]
    """

    kwargs = _get_kwargs(
        collection=collection,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    collection: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, List["Document"]]]:
    """List Documents

     List documents.

    Args:
        collection (Union[None, Unset, str]): Limit to documents associated with this collection

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, List['Document']]
    """

    return sync_detailed(
        client=client,
        collection=collection,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    collection: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, List["Document"]]]:
    """List Documents

     List documents.

    Args:
        collection (Union[None, Unset, str]): Limit to documents associated with this collection

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, List['Document']]]
    """

    kwargs = _get_kwargs(
        collection=collection,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    collection: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, List["Document"]]]:
    """List Documents

     List documents.

    Args:
        collection (Union[None, Unset, str]): Limit to documents associated with this collection

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, List['Document']]
    """

    return (
        await asyncio_detailed(
            client=client,
            collection=collection,
        )
    ).parsed
