from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ingest_state import IngestState
from ..types import UNSET, Unset

T = TypeVar("T", bound="Document")


@_attrs_define
class Document:
    """Model for documents in Dewy.

    Attributes:
        collection (str):
        id (Union[None, Unset, int]):
        extracted_text (Union[None, Unset, str]):
        url (Union[None, Unset, str]):
        ingest_state (Union[IngestState, None, Unset]):
        ingest_error (Union[None, Unset, str]):
    """

    collection: str
    id: Union[None, Unset, int] = UNSET
    extracted_text: Union[None, Unset, str] = UNSET
    url: Union[None, Unset, str] = UNSET
    ingest_state: Union[IngestState, None, Unset] = UNSET
    ingest_error: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        collection = self.collection

        id: Union[None, Unset, int]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        extracted_text: Union[None, Unset, str]
        if isinstance(self.extracted_text, Unset):
            extracted_text = UNSET
        else:
            extracted_text = self.extracted_text

        url: Union[None, Unset, str]
        if isinstance(self.url, Unset):
            url = UNSET
        else:
            url = self.url

        ingest_state: Union[None, Unset, str]
        if isinstance(self.ingest_state, Unset):
            ingest_state = UNSET
        elif isinstance(self.ingest_state, IngestState):
            ingest_state = self.ingest_state.value
        else:
            ingest_state = self.ingest_state

        ingest_error: Union[None, Unset, str]
        if isinstance(self.ingest_error, Unset):
            ingest_error = UNSET
        else:
            ingest_error = self.ingest_error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "collection": collection,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if extracted_text is not UNSET:
            field_dict["extracted_text"] = extracted_text
        if url is not UNSET:
            field_dict["url"] = url
        if ingest_state is not UNSET:
            field_dict["ingest_state"] = ingest_state
        if ingest_error is not UNSET:
            field_dict["ingest_error"] = ingest_error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        collection = d.pop("collection")

        def _parse_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_extracted_text(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        extracted_text = _parse_extracted_text(d.pop("extracted_text", UNSET))

        def _parse_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        url = _parse_url(d.pop("url", UNSET))

        def _parse_ingest_state(data: object) -> Union[IngestState, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                ingest_state_type_0 = IngestState(data)

                return ingest_state_type_0
            except:  # noqa: E722
                pass
            return cast(Union[IngestState, None, Unset], data)

        ingest_state = _parse_ingest_state(d.pop("ingest_state", UNSET))

        def _parse_ingest_error(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ingest_error = _parse_ingest_error(d.pop("ingest_error", UNSET))

        document = cls(
            collection=collection,
            id=id,
            extracted_text=extracted_text,
            url=url,
            ingest_state=ingest_state,
            ingest_error=ingest_error,
        )

        document.additional_properties = d
        return document

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
