from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ImageResult")


@_attrs_define
class ImageResult:
    """
    Attributes:
        chunk_id (int):
        document_id (int):
        score (float):
        image (Union[None, str]): Image of the node.
        image_mimetype (Union[None, str]): Mimetype of the image.
        image_path (Union[None, str]): Path of the image.
        image_url (Union[None, str]): URL of the image.
    """

    chunk_id: int
    document_id: int
    score: float
    image: Union[None, str]
    image_mimetype: Union[None, str]
    image_path: Union[None, str]
    image_url: Union[None, str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        chunk_id = self.chunk_id

        document_id = self.document_id

        score = self.score

        image: Union[None, str]
        image = self.image

        image_mimetype: Union[None, str]
        image_mimetype = self.image_mimetype

        image_path: Union[None, str]
        image_path = self.image_path

        image_url: Union[None, str]
        image_url = self.image_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "chunk_id": chunk_id,
                "document_id": document_id,
                "score": score,
                "image": image,
                "image_mimetype": image_mimetype,
                "image_path": image_path,
                "image_url": image_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        chunk_id = d.pop("chunk_id")

        document_id = d.pop("document_id")

        score = d.pop("score")

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

        image_result = cls(
            chunk_id=chunk_id,
            document_id=document_id,
            score=score,
            image=image,
            image_mimetype=image_mimetype,
            image_path=image_path,
            image_url=image_url,
        )

        image_result.additional_properties = d
        return image_result

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
