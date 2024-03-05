from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.retrieve_request import RetrieveRequest
    from ..models.serve_config import ServeConfig


T = TypeVar("T", bound="BodyRetrieveChunks")


@_attrs_define
class BodyRetrieveChunks:
    """
    Attributes:
        config (ServeConfig):
        request (RetrieveRequest): A request for retrieving chunks from a collection.
    """

    config: "ServeConfig"
    request: "RetrieveRequest"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        config = self.config.to_dict()

        request = self.request.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "config": config,
                "request": request,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.retrieve_request import RetrieveRequest
        from ..models.serve_config import ServeConfig

        d = src_dict.copy()
        config = ServeConfig.from_dict(d.pop("config"))

        request = RetrieveRequest.from_dict(d.pop("request"))

        body_retrieve_chunks = cls(
            config=config,
            request=request,
        )

        body_retrieve_chunks.additional_properties = d
        return body_retrieve_chunks

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
