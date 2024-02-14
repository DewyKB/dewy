from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.distance_metric import DistanceMetric
from ..types import UNSET, Unset

T = TypeVar("T", bound="Collection")


@_attrs_define
class Collection:
    """
    Attributes:
        name (str):
        text_embedding_model (str):
        text_distance_metric (Union[Unset, DistanceMetric]):  Default: DistanceMetric.COSINE.
    """

    name: str
    text_embedding_model: str
    text_distance_metric: Union[Unset, DistanceMetric] = DistanceMetric.COSINE
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        text_embedding_model = self.text_embedding_model

        text_distance_metric: Union[Unset, str] = UNSET
        if not isinstance(self.text_distance_metric, Unset):
            text_distance_metric = self.text_distance_metric.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "text_embedding_model": text_embedding_model,
            }
        )
        if text_distance_metric is not UNSET:
            field_dict["text_distance_metric"] = text_distance_metric

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        text_embedding_model = d.pop("text_embedding_model")

        _text_distance_metric = d.pop("text_distance_metric", UNSET)
        text_distance_metric: Union[Unset, DistanceMetric]
        if isinstance(_text_distance_metric, Unset):
            text_distance_metric = UNSET
        else:
            text_distance_metric = DistanceMetric(_text_distance_metric)

        collection = cls(
            name=name,
            text_embedding_model=text_embedding_model,
            text_distance_metric=text_distance_metric,
        )

        collection.additional_properties = d
        return collection

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
