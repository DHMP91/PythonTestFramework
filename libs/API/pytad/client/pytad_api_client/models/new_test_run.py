import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.status_enum import StatusEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="NewTestRun")


@_attrs_define
class NewTestRun:
    """
    Attributes:
        name (str):
        start_time (datetime.datetime):
        code_hash (str):
        suite_id (Union[Unset, str]):
        status (Union[Unset, StatusEnum]): * `PASSED` - Pass
            * `FAILED` - Fail
            * `ERROR` - Error
            * `UNKNOWN` - Unknown
            * `XFAILED` - Xfail
            * `XPASSED` - Xpass
            * `SKIPPED` - Skipped
            * `INPROGRESS` - Inprogress
        end_time (Union[None, Unset, datetime.datetime]):
        marks (Union[Unset, str]):
        product_version (Union[Unset, str]):
        environment (Union[Unset, str]):
        defects (Union[Unset, str]):
    """

    name: str
    start_time: datetime.datetime
    code_hash: str
    suite_id: Union[Unset, str] = UNSET
    status: Union[Unset, StatusEnum] = UNSET
    end_time: Union[None, Unset, datetime.datetime] = UNSET
    marks: Union[Unset, str] = UNSET
    product_version: Union[Unset, str] = UNSET
    environment: Union[Unset, str] = UNSET
    defects: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        start_time = self.start_time.isoformat()

        code_hash = self.code_hash

        suite_id = self.suite_id

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        end_time: Union[None, Unset, str]
        if isinstance(self.end_time, Unset):
            end_time = UNSET
        elif isinstance(self.end_time, datetime.datetime):
            end_time = self.end_time.isoformat()
        else:
            end_time = self.end_time

        marks = self.marks

        product_version = self.product_version

        environment = self.environment

        defects = self.defects

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "start_time": start_time,
                "code_hash": code_hash,
            }
        )
        if suite_id is not UNSET:
            field_dict["suite_id"] = suite_id
        if status is not UNSET:
            field_dict["status"] = status
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if marks is not UNSET:
            field_dict["marks"] = marks
        if product_version is not UNSET:
            field_dict["product_version"] = product_version
        if environment is not UNSET:
            field_dict["environment"] = environment
        if defects is not UNSET:
            field_dict["defects"] = defects

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        start_time = isoparse(d.pop("start_time"))

        code_hash = d.pop("code_hash")

        suite_id = d.pop("suite_id", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, StatusEnum]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = StatusEnum(_status)

        def _parse_end_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_time_type_0 = isoparse(data)

                return end_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        end_time = _parse_end_time(d.pop("end_time", UNSET))

        marks = d.pop("marks", UNSET)

        product_version = d.pop("product_version", UNSET)

        environment = d.pop("environment", UNSET)

        defects = d.pop("defects", UNSET)

        new_test_run = cls(
            name=name,
            start_time=start_time,
            code_hash=code_hash,
            suite_id=suite_id,
            status=status,
            end_time=end_time,
            marks=marks,
            product_version=product_version,
            environment=environment,
            defects=defects,
        )

        new_test_run.additional_properties = d
        return new_test_run

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
