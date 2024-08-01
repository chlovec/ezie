from dataclasses import dataclass
from enum import Enum
from typing import List, Union


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


@dataclass
class RefEntityField:
    name: str
    ref_entity: "Entity"
    is_required: bool = False


@dataclass
class Entity:
    name: str
    non_ref_fields: List[EntityField]
    ref_fields: List[RefEntityField]
    pk_fields: List[EntityField]
