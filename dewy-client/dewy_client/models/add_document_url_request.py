from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AddDocumentUrlRequest")


@_attrs_define
class AddDocumentUrlRequest:
    """
    Attributes:
        collection_id (int):
        url (str):
    """

    collection_id: int
    url: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        collection_id = self.collection_id

        url = self.url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "collection_id": collection_id,
                "url": url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        collection_id = d.pop("collection_id")

        url = d.pop("url")

        add_document_url_request = cls(
            collection_id=collection_id,
            url=url,
        )

        add_document_url_request.additional_properties = d
        return add_document_url_request

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
