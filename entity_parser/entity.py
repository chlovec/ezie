from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Union


class FieldFormat(Enum):
    DATE = "date"
    DOUBLE = "double"
    FLOAT = "float"
    TIME = "time"
    TIMESTAMP = "date-time"
    UUID = "uuid"
    IPV4 = "ipv4"
    IPV6 = "ipv6"
    MAC = "mac"
    JSON = "json"
    BYTEA = "byte"


class FieldType(Enum):
    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    OBJECT = "object"
    ARRAY = "array"
    BOOLEAN = "boolean"


@dataclass
class EntityField:
    name: str
    field_type: FieldType
    max_length: Union[int, str]
    is_required: bool = False
    is_primary_key: bool = False
    type_ref: str = None
    format: str = None
    is_enum: bool = False
    enum_values: List[Any] = field(default_factory=list)

    def get_ref_name(
        self, parent_field_name: str, ref_entity_name: str
    ) -> str:
        if self.name.startswith((parent_field_name, ref_entity_name)):
            return self.name
        return f"{parent_field_name}_{self.name}"


@dataclass
class RefEntityField:
    name: str
    ref_entity: "Entity"
    is_required: bool = False

    def get_ref_names(self) -> List[str]:
        if self.ref_entity.is_enum:
            return [self.name]

        return [
            fld.get_ref_name(self.name, self.ref_entity.name)
            for fld in self.ref_entity.pk_fields
        ]


@dataclass
class Entity:
    name: str
    non_ref_fields: List[EntityField]
    ref_fields: List[RefEntityField]
    pk_fields: List[EntityField]
    is_enum: bool = False
    enum_values: Any = None
    is_sub_def: bool = False
