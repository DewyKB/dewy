from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RetrieveRequest")


@_attrs_define
class RetrieveRequest:
    """A request for retrieving chunks from a collection.

    Attributes:
        collection (str):
        query (str):
        n (Union[Unset, int]):  Default: 10.
        include_text_chunks (Union[Unset, bool]):  Default: True.
        include_image_chunks (Union[Unset, bool]):  Default: True.
        include_summary (Union[Unset, bool]):  Default: False.
    """

    collection: str
    query: str
    n: Union[Unset, int] = 10
    include_text_chunks: Union[Unset, bool] = True
    include_image_chunks: Union[Unset, bool] = True
    include_summary: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        collection = self.collection

        query = self.query

        n = self.n

        include_text_chunks = self.include_text_chunks

        include_image_chunks = self.include_image_chunks

        include_summary = self.include_summary

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "collection": collection,
                "query": query,
            }
        )
        if n is not UNSET:
            field_dict["n"] = n
        if include_text_chunks is not UNSET:
            field_dict["include_text_chunks"] = include_text_chunks
        if include_image_chunks is not UNSET:
            field_dict["include_image_chunks"] = include_image_chunks
        if include_summary is not UNSET:
            field_dict["include_summary"] = include_summary

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        collection = d.pop("collection")

        query = d.pop("query")

        n = d.pop("n", UNSET)

        include_text_chunks = d.pop("include_text_chunks", UNSET)

        include_image_chunks = d.pop("include_image_chunks", UNSET)

        include_summary = d.pop("include_summary", UNSET)

        retrieve_request = cls(
            collection=collection,
            query=query,
            n=n,
            include_text_chunks=include_text_chunks,
            include_image_chunks=include_image_chunks,
            include_summary=include_summary,
        )

        retrieve_request.additional_properties = d
        return retrieve_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
