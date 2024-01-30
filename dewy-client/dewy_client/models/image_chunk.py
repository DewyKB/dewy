from typing import Any, Dict, List, Literal, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ImageChunk")


@_attrs_define
class ImageChunk:
    """
    Attributes:
        id (int):
        document_id (int):
        image (Union[None, str]): Image of the node.
        image_mimetype (Union[None, str]): Mimetype of the image.
        image_path (Union[None, str]): Path of the image.
        image_url (Union[None, str]): URL of the image.
        kind (Union[Literal['image'], Unset]):  Default: 'image'.
    """

    id: int
    document_id: int
    image: Union[None, str]
    image_mimetype: Union[None, str]
    image_path: Union[None, str]
    image_url: Union[None, str]
    kind: Union[Literal["image"], Unset] = "image"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        document_id = self.document_id

        image: Union[None, str]
        image = self.image

        image_mimetype: Union[None, str]
        image_mimetype = self.image_mimetype

        image_path: Union[None, str]
        image_path = self.image_path

        image_url: Union[None, str]
        image_url = self.image_url

        kind = self.kind

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "document_id": document_id,
                "image": image,
                "image_mimetype": image_mimetype,
                "image_path": image_path,
                "image_url": image_url,
            }
        )
        if kind is not UNSET:
            field_dict["kind"] = kind

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        document_id = d.pop("document_id")

        def _parse_image(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        image = _parse_image(d.pop("image"))

        def _parse_image_mimetype(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        image_mimetype = _parse_image_mimetype(d.pop("image_mimetype"))

        def _parse_image_path(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        image_path = _parse_image_path(d.pop("image_path"))

        def _parse_image_url(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        image_url = _parse_image_url(d.pop("image_url"))

        kind = d.pop("kind", UNSET)

        image_chunk = cls(
            id=id,
            document_id=document_id,
            image=image,
            image_mimetype=image_mimetype,
            image_path=image_path,
            image_url=image_url,
            kind=kind,
        )

        image_chunk.additional_properties = d
        return image_chunk

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
