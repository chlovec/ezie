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


@dataclass
class RefEntityField:
    name: str
    ref_entity: "Entity"
    is_required: bool = False

    def get_ref_names(self) -> List[str]:
        """Returns a list of field that represents the names for the primary
        key fields of the referenced entities.

        Notes:
            If a primary key field does not start with the name of this field
            or the name of the referenced entity, it's name will be prefixed
            with the name of this field.
            This could return empty list of referenced entity does not have a
            primary key field.

        Returns:
            List[str]: A list of string
        """
        result: List[str] = []
        for fld in self.ref_entity.pk_fields:
            if (
                fld.name.startswith(self.name)
                or fld.name.startswith(self.ref_entity.name)
            ):
                result.append(fld.name)
            else:
                result.append(f"{self.name}_{fld.name}")

        return result


@dataclass
class Entity:
    name: str
    non_ref_fields: List[EntityField]
    ref_fields: List[RefEntityField]
    pk_fields: List[EntityField]
    is_enum: bool = False
    enum_values: Any = None
    is_sub_def: bool = False
