from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.image_chunk import ImageChunk
from ...models.text_chunk import TextChunk
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    collection: Union[None, Unset, str] = UNSET,
    document_id: Union[None, Unset, int] = UNSET,
    page: Union[None, Unset, int] = 0,
    per_page: Union[None, Unset, int] = 10,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_collection: Union[None, Unset, str]
    if isinstance(collection, Unset):
        json_collection = UNSET
    else:
        json_collection = collection
    params["collection"] = json_collection

    json_document_id: Union[None, Unset, int]
    if isinstance(document_id, Unset):
        json_document_id = UNSET
    else:
        json_document_id = document_id
    params["document_id"] = json_document_id

    json_page: Union[None, Unset, int]
    if isinstance(page, Unset):
        json_page = UNSET
    else:
        json_page = page
    params["page"] = json_page

    json_per_page: Union[None, Unset, int]
    if isinstance(per_page, Unset):
        json_per_page = UNSET
    else:
        json_per_page = per_page
    params["perPage"] = json_per_page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/chunks/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, List[Union["ImageChunk", "TextChunk"]]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:

            def _parse_response_200_item(data: object) -> Union["ImageChunk", "TextChunk"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    response_200_item_type_0 = TextChunk.from_dict(data)

                    return response_200_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_item_type_1 = ImageChunk.from_dict(data)

                return response_200_item_type_1

            response_200_item = _parse_response_200_item(response_200_item_data)

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
) -> Response[Union[HTTPValidationError, List[Union["ImageChunk", "TextChunk"]]]]:
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
    document_id: Union[None, Unset, int] = UNSET,
    page: Union[None, Unset, int] = 0,
    per_page: Union[None, Unset, int] = 10,
) -> Response[Union[HTTPValidationError, List[Union["ImageChunk", "TextChunk"]]]]:
    """List Chunks

     List chunks.

    Args:
        collection (Union[None, Unset, str]): Limit to chunks associated with this collection
        document_id (Union[None, Unset, int]): Limit to chunks associated with this document
        page (Union[None, Unset, int]):  Default: 0.
        per_page (Union[None, Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, List[Union['ImageChunk', 'TextChunk']]]]
    """

    kwargs = _get_kwargs(
        collection=collection,
        document_id=document_id,
        page=page,
        per_page=per_page,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    collection: Union[None, Unset, str] = UNSET,
    document_id: Union[None, Unset, int] = UNSET,
    page: Union[None, Unset, int] = 0,
    per_page: Union[None, Unset, int] = 10,
) -> Optional[Union[HTTPValidationError, List[Union["ImageChunk", "TextChunk"]]]]:
    """List Chunks

     List chunks.

    Args:
        collection (Union[None, Unset, str]): Limit to chunks associated with this collection
        document_id (Union[None, Unset, int]): Limit to chunks associated with this document
        page (Union[None, Unset, int]):  Default: 0.
        per_page (Union[None, Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, List[Union['ImageChunk', 'TextChunk']]]
    """

    return sync_detailed(
        client=client,
        collection=collection,
        document_id=document_id,
        page=page,
        per_page=per_page,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    collection: Union[None, Unset, str] = UNSET,
    document_id: Union[None, Unset, int] = UNSET,
    page: Union[None, Unset, int] = 0,
    per_page: Union[None, Unset, int] = 10,
) -> Response[Union[HTTPValidationError, List[Union["ImageChunk", "TextChunk"]]]]:
    """List Chunks

     List chunks.

    Args:
        collection (Union[None, Unset, str]): Limit to chunks associated with this collection
        document_id (Union[None, Unset, int]): Limit to chunks associated with this document
        page (Union[None, Unset, int]):  Default: 0.
        per_page (Union[None, Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, List[Union['ImageChunk', 'TextChunk']]]]
    """

    kwargs = _get_kwargs(
        collection=collection,
        document_id=document_id,
        page=page,
        per_page=per_page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    collection: Union[None, Unset, str] = UNSET,
    document_id: Union[None, Unset, int] = UNSET,
    page: Union[None, Unset, int] = 0,
    per_page: Union[None, Unset, int] = 10,
) -> Optional[Union[HTTPValidationError, List[Union["ImageChunk", "TextChunk"]]]]:
    """List Chunks

     List chunks.

    Args:
        collection (Union[None, Unset, str]): Limit to chunks associated with this collection
        document_id (Union[None, Unset, int]): Limit to chunks associated with this document
        page (Union[None, Unset, int]):  Default: 0.
        per_page (Union[None, Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, List[Union['ImageChunk', 'TextChunk']]]
    """

    return (
        await asyncio_detailed(
            client=client,
            collection=collection,
            document_id=document_id,
            page=page,
            per_page=per_page,
        )
    ).parsed
