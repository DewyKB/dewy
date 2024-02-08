from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import File, Unset

T = TypeVar("T", bound="BodyAddDocumentFromContent")


@_attrs_define
class BodyAddDocumentFromContent:
    """
    Attributes:
        collection_id (int): The collection to add the document to.
        content (File): The content containing the document.
    """

    collection_id: int
    content: File
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        collection_id = self.collection_id

        content = self.content.to_tuple()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "collection_id": collection_id,
                "content": content,
            }
        )

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        collection_id = (
            self.collection_id
            if isinstance(self.collection_id, Unset)
            else (None, str(self.collection_id).encode(), "text/plain")
        )

        content = self.content.to_tuple()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {key: (None, str(value).encode(), "text/plain") for key, value in self.additional_properties.items()}
        )
        field_dict.update(
            {
                "collection_id": collection_id,
                "content": content,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        collection_id = d.pop("collection_id")

        content = File(payload=BytesIO(d.pop("content")))

        body_add_document_from_content = cls(
            collection_id=collection_id,
            content=content,
        )

        body_add_document_from_content.additional_properties = d
        return body_add_document_from_content

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
