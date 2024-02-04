from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ingest_state import IngestState
from ..types import UNSET, Unset

T = TypeVar("T", bound="DocumentStatus")


@_attrs_define
class DocumentStatus:
    """Model for document status.

    Attributes:
        id (int):
        ingest_state (IngestState):
        ingest_error (Union[None, Unset, str]):
    """

    id: int
    ingest_state: IngestState
    ingest_error: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        ingest_state = self.ingest_state.value

        ingest_error: Union[None, Unset, str]
        if isinstance(self.ingest_error, Unset):
            ingest_error = UNSET
        else:
            ingest_error = self.ingest_error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "ingest_state": ingest_state,
            }
        )
        if ingest_error is not UNSET:
            field_dict["ingest_error"] = ingest_error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        ingest_state = IngestState(d.pop("ingest_state"))

        def _parse_ingest_error(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ingest_error = _parse_ingest_error(d.pop("ingest_error", UNSET))

        document_status = cls(
            id=id,
            ingest_state=ingest_state,
            ingest_error=ingest_error,
        )

        document_status.additional_properties = d
        return document_status

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
