from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TextResult")


@_attrs_define
class TextResult:
    """
    Attributes:
        chunk_id (int):
        document_id (int):
        score (float):
        text (str):
        raw (bool):
        start_char_idx (Union[None, Unset, int]): Start char index of the chunk.
        end_char_idx (Union[None, Unset, int]): End char index of the chunk.
    """

    chunk_id: int
    document_id: int
    score: float
    text: str
    raw: bool
    start_char_idx: Union[None, Unset, int] = UNSET
    end_char_idx: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        chunk_id = self.chunk_id

        document_id = self.document_id

        score = self.score

        text = self.text

        raw = self.raw

        start_char_idx: Union[None, Unset, int]
        if isinstance(self.start_char_idx, Unset):
            start_char_idx = UNSET
        else:
            start_char_idx = self.start_char_idx

        end_char_idx: Union[None, Unset, int]
        if isinstance(self.end_char_idx, Unset):
            end_char_idx = UNSET
        else:
            end_char_idx = self.end_char_idx

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "chunk_id": chunk_id,
                "document_id": document_id,
                "score": score,
                "text": text,
                "raw": raw,
            }
        )
        if start_char_idx is not UNSET:
            field_dict["start_char_idx"] = start_char_idx
        if end_char_idx is not UNSET:
            field_dict["end_char_idx"] = end_char_idx

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        chunk_id = d.pop("chunk_id")

        document_id = d.pop("document_id")

        score = d.pop("score")

        text = d.pop("text")

        raw = d.pop("raw")

        def _parse_start_char_idx(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        start_char_idx = _parse_start_char_idx(d.pop("start_char_idx", UNSET))

        def _parse_end_char_idx(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        end_char_idx = _parse_end_char_idx(d.pop("end_char_idx", UNSET))

        text_result = cls(
            chunk_id=chunk_id,
            document_id=document_id,
            score=score,
            text=text,
            raw=raw,
            start_char_idx=start_char_idx,
            end_char_idx=end_char_idx,
        )

        text_result.additional_properties = d
        return text_result

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