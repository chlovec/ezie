from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Union


class FieldType(Enum):
    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    OBJECT = "object"
    ARRAY = "array"
    BOOLEAN = "boolean"


@dataclass
class FieldData:
    name: str
    ref_entity_name: str
    data_type: str
    is_required: bool
    ref_field_name: str = None
    pl_data_type: str = None


@dataclass
class BaseEntityField:
    name: str
    is_required: bool = False

    def get_field_name(self, parent_field_name: str) -> str:
        if self.name.startswith(parent_field_name):
            return self.name
        return f"{parent_field_name}_{self.name}"


@dataclass
class EntityField(BaseEntityField):
    field_type: FieldType = None
    max_length: Union[int, str] = None
    is_primary_key: bool = False
    type_ref: str = None
    format: str = None
    is_enum: bool = False
    enum_values: List[Any] = field(default_factory=list)
    minimum: int = None
    maximum: int = None


@dataclass
class RefEntityField(BaseEntityField):
    ref_entity: "Entity" = None


@dataclass
class Entity:
    name: str
    non_ref_fields: List[EntityField]
    ref_fields: List[RefEntityField]
    pk_fields: List[EntityField]
    is_enum: bool = False
    enum_values: Any = None
    is_sub_def: bool = False
