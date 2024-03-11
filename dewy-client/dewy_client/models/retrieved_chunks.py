from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.image_chunk import ImageChunk
    from ..models.text_chunk import TextChunk


T = TypeVar("T", bound="RetrievedChunks")


@_attrs_define
class RetrievedChunks:
    """The response from a retrieval request.

    Attributes:
        summary (Union[None, Unset, str]):
        text_chunks (Union[Unset, List['TextChunk']]):
        image_chunks (Union[Unset, List['ImageChunk']]):
    """

    summary: Union[None, Unset, str] = UNSET
    text_chunks: Union[Unset, List["TextChunk"]] = UNSET
    image_chunks: Union[Unset, List["ImageChunk"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        summary: Union[None, Unset, str]
        if isinstance(self.summary, Unset):
            summary = UNSET
        else:
            summary = self.summary

        text_chunks: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.text_chunks, Unset):
            text_chunks = []
            for text_chunks_item_data in self.text_chunks:
                text_chunks_item = text_chunks_item_data.to_dict()
                text_chunks.append(text_chunks_item)

        image_chunks: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.image_chunks, Unset):
            image_chunks = []
            for image_chunks_item_data in self.image_chunks:
                image_chunks_item = image_chunks_item_data.to_dict()
                image_chunks.append(image_chunks_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if summary is not UNSET:
            field_dict["summary"] = summary
        if text_chunks is not UNSET:
            field_dict["text_chunks"] = text_chunks
        if image_chunks is not UNSET:
            field_dict["image_chunks"] = image_chunks

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.image_chunk import ImageChunk
        from ..models.text_chunk import TextChunk

        d = src_dict.copy()

        def _parse_summary(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        summary = _parse_summary(d.pop("summary", UNSET))

        text_chunks = []
        _text_chunks = d.pop("text_chunks", UNSET)
        for text_chunks_item_data in _text_chunks or []:
            text_chunks_item = TextChunk.from_dict(text_chunks_item_data)

            text_chunks.append(text_chunks_item)

        image_chunks = []
        _image_chunks = d.pop("image_chunks", UNSET)
        for image_chunks_item_data in _image_chunks or []:
            image_chunks_item = ImageChunk.from_dict(image_chunks_item_data)

            image_chunks.append(image_chunks_item)

        retrieved_chunks = cls(
            summary=summary,
            text_chunks=text_chunks,
            image_chunks=image_chunks,
        )

        retrieved_chunks.additional_properties = d
        return retrieved_chunks

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
