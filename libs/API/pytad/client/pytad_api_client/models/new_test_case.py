import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="NewTestCase")


@_attrs_define
class NewTestCase:
    """
    Attributes:
        id (int):
        name (str):
        relative_path (str):
        create_date (datetime.datetime):
        code_hash (str):
        code (str):
        internal_id (Union[None, Unset, str]):
    """

    id: int
    name: str
    relative_path: str
    create_date: datetime.datetime
    code_hash: str
    code: str
    internal_id: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        relative_path = self.relative_path

        create_date = self.create_date.isoformat()

        code_hash = self.code_hash

        code = self.code

        internal_id: Union[None, Unset, str]
        if isinstance(self.internal_id, Unset):
            internal_id = UNSET
        else:
            internal_id = self.internal_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "relative_path": relative_path,
                "create_date": create_date,
                "code_hash": code_hash,
                "code": code,
            }
        )
        if internal_id is not UNSET:
            field_dict["internal_id"] = internal_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        relative_path = d.pop("relative_path")

        create_date = isoparse(d.pop("create_date"))

        code_hash = d.pop("code_hash")

        code = d.pop("code")

        def _parse_internal_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        internal_id = _parse_internal_id(d.pop("internal_id", UNSET))

        new_test_case = cls(
            id=id,
            name=name,
            relative_path=relative_path,
            create_date=create_date,
            code_hash=code_hash,
            code=code,
            internal_id=internal_id,
        )

        new_test_case.additional_properties = d
        return new_test_case

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
