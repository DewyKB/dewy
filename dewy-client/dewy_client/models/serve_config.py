from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ServeConfig")


@_attrs_define
class ServeConfig:
    """
    Attributes:
        db (Union[None, Unset, str]):
        broker (Union[None, Unset, str]):
        serve_openapi_ui (Union[Unset, bool]):  Default: True.
        serve_admin_ui (Union[Unset, bool]):  Default: True.
        apply_migrations (Union[Unset, bool]):  Default: True.
        openai_api_key (Union[None, Unset, str]):
    """

    db: Union[None, Unset, str] = UNSET
    broker: Union[None, Unset, str] = UNSET
    serve_openapi_ui: Union[Unset, bool] = True
    serve_admin_ui: Union[Unset, bool] = True
    apply_migrations: Union[Unset, bool] = True
    openai_api_key: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        db: Union[None, Unset, str]
        if isinstance(self.db, Unset):
            db = UNSET
        else:
            db = self.db

        broker: Union[None, Unset, str]
        if isinstance(self.broker, Unset):
            broker = UNSET
        else:
            broker = self.broker

        serve_openapi_ui = self.serve_openapi_ui

        serve_admin_ui = self.serve_admin_ui

        apply_migrations = self.apply_migrations

        openai_api_key: Union[None, Unset, str]
        if isinstance(self.openai_api_key, Unset):
            openai_api_key = UNSET
        else:
            openai_api_key = self.openai_api_key

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if db is not UNSET:
            field_dict["db"] = db
        if broker is not UNSET:
            field_dict["broker"] = broker
        if serve_openapi_ui is not UNSET:
            field_dict["serve_openapi_ui"] = serve_openapi_ui
        if serve_admin_ui is not UNSET:
            field_dict["serve_admin_ui"] = serve_admin_ui
        if apply_migrations is not UNSET:
            field_dict["apply_migrations"] = apply_migrations
        if openai_api_key is not UNSET:
            field_dict["openai_api_key"] = openai_api_key

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_db(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        db = _parse_db(d.pop("db", UNSET))

        def _parse_broker(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        broker = _parse_broker(d.pop("broker", UNSET))

        serve_openapi_ui = d.pop("serve_openapi_ui", UNSET)

        serve_admin_ui = d.pop("serve_admin_ui", UNSET)

        apply_migrations = d.pop("apply_migrations", UNSET)

        def _parse_openai_api_key(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        openai_api_key = _parse_openai_api_key(d.pop("openai_api_key", UNSET))

        serve_config = cls(
            db=db,
            broker=broker,
            serve_openapi_ui=serve_openapi_ui,
            serve_admin_ui=serve_admin_ui,
            apply_migrations=apply_migrations,
            openai_api_key=openai_api_key,
        )

        serve_config.additional_properties = d
        return serve_config

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
