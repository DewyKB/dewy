from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.image_result import ImageResult
    from ..models.text_result import TextResult


T = TypeVar("T", bound="RetrieveResponse")


@_attrs_define
class RetrieveResponse:
    """The response from a retrieval request.

    Attributes:
        summary (Union[None, str]):
        text_results (List['TextResult']):
        image_results (List['ImageResult']):
    """

    summary: Union[None, str]
    text_results: List["TextResult"]
    image_results: List["ImageResult"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        summary: Union[None, str]
        summary = self.summary

        text_results = []
        for text_results_item_data in self.text_results:
            text_results_item = text_results_item_data.to_dict()
            text_results.append(text_results_item)

        image_results = []
        for image_results_item_data in self.image_results:
            image_results_item = image_results_item_data.to_dict()
            image_results.append(image_results_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "summary": summary,
                "text_results": text_results,
                "image_results": image_results,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.image_result import ImageResult
        from ..models.text_result import TextResult

        d = src_dict.copy()

        def _parse_summary(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        summary = _parse_summary(d.pop("summary"))

        text_results = []
        _text_results = d.pop("text_results")
        for text_results_item_data in _text_results:
            text_results_item = TextResult.from_dict(text_results_item_data)

            text_results.append(text_results_item)

        image_results = []
        _image_results = d.pop("image_results")
        for image_results_item_data in _image_results:
            image_results_item = ImageResult.from_dict(image_results_item_data)

            image_results.append(image_results_item)

        retrieve_response = cls(
            summary=summary,
            text_results=text_results,
            image_results=image_results,
        )

        retrieve_response.additional_properties = d
        return retrieve_response

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
