from dataclasses import dataclass
from typing import List, Union


@dataclass
class EntityField:
    name: str
    field_type: str
    max_length: Union[int, str]
    is_required: bool = False
    is_primary_key: bool = False
    type_ref: str = None


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
