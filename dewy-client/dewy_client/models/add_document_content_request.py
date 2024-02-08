from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import File, FileJsonType

T = TypeVar("T", bound="AddDocumentContentRequest")


@_attrs_define
class AddDocumentContentRequest:
    """
    Attributes:
        collection_id (int):
        content (Union[File, str]):
    """

    collection_id: int
    content: Union[File, str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        collection_id = self.collection_id

        content: Union[FileJsonType, str]
        if isinstance(self.content, File):
            content = self.content.to_tuple()

        else:
            content = self.content

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
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

        def _parse_content(data: object) -> Union[File, str]:
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                content_type_1 = File(payload=BytesIO(data))

                return content_type_1
            except:  # noqa: E722
                pass
            return cast(Union[File, str], data)

        content = _parse_content(d.pop("content"))

        add_document_content_request = cls(
            collection_id=collection_id,
            content=content,
        )

        add_document_content_request.additional_properties = d
        return add_document_content_request

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
