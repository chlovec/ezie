from dataclasses import dataclass
import os
from typing import List, NamedTuple

from data_type_mapper.data_type_mapper import TypeMapper
from entity_parser.entity import Entity, EntityField, FieldData, RefEntityField


def read_file_content(file_path: str) -> None:
    with open(file_path) as file:
        return file.read()


def remove_last_comma(s: str) -> str:
    if s.endswith(","):
        return s[:-1]
    return s


def get_field_data(
    non_ref_fields: List[EntityField],
    type_mapper: TypeMapper = None,
    parent_field_name: str = "",
    ref_entity_name: str = ""
) -> List[FieldData]:
    return [
        FieldData(
            name=fld.get_field_name(parent_field_name),
            ref_entity_name=ref_entity_name,
            data_type=type_mapper.get_field_type(fld) if type_mapper else None,
            is_required=fld.is_required,
            ref_field_name=fld.name
        )
        for fld in non_ref_fields
    ]


def write_file_data(file_data: "FileData") -> None:
    file_path = os.path.join(file_data.file_path, file_data.file_name)
    with open(file_path, "w") as file:
        for line in file_data.file_content:
            file.write(line + "\n")


def get_ref_field_data(
    ref_fields: List[RefEntityField],
    type_mapper: TypeMapper = None,
    parent_field_name: str = ""
) -> "RefFieldData":
    non_fk_fields_data, fk_fields_data = [], []
    for fld in ref_fields:
        if fld.ref_entity.is_sub_def:
            non_fk_fields_data.extend(get_field_data(
                non_ref_fields=fld.ref_entity.pk_fields,
                type_mapper=type_mapper,
                parent_field_name=fld.name,
                ref_entity_name=fld.ref_entity.name
            ))
            non_fk_fields_data.extend(get_field_data(
                non_ref_fields=fld.ref_entity.non_ref_fields,
                type_mapper=type_mapper,
                parent_field_name=fld.name,
                ref_entity_name=fld.ref_entity.name
            ))
            ref_field_data = get_ref_field_data(
                ref_fields=fld.ref_entity.ref_fields,
                type_mapper=type_mapper,
                parent_field_name=fld.name
            )
            non_fk_fields_data.extend(ref_field_data.other_field_data)
            fk_fields_data.extend(ref_field_data.fk_field_data)
        elif fld.ref_entity.is_enum:
            data_type = (
                type_mapper.get_enum_field_type(fld.ref_entity)
                if type_mapper else None
            )
            non_fk_fields_data.append(
                FieldData(
                    name=fld.get_field_name(parent_field_name),
                    ref_entity_name=fld.ref_entity.name,
                    data_type=data_type,
                    is_required=fld.is_required
                )
            )
        else:
            fk_fields_data.extend(get_field_data(
                non_ref_fields=fld.ref_entity.pk_fields,
                type_mapper=type_mapper,
                parent_field_name=fld.name,
                ref_entity_name=fld.ref_entity.name
            ))

    return RefFieldData(non_fk_fields_data, fk_fields_data)


class RefFieldData(NamedTuple):
    other_field_data: List[FieldData]
    fk_field_data: List[FieldData]


@dataclass
class EntityFieldData:
    entity_name: str
    pk_field_data: List[FieldData]
    fk_field_data: List[FieldData]
    other_field_data: List[FieldData]
    entity: Entity

    @classmethod
    def from_entity(
        cls, entity: Entity, type_mapper: TypeMapper = None
    ) -> "EntityFieldData":
        ref_data = get_ref_field_data(
            ref_fields=entity.ref_fields,
            type_mapper=type_mapper
        )

        pk_data = get_field_data(
            non_ref_fields=entity.pk_fields,
            type_mapper=type_mapper
        )

        other_data = get_field_data(
            non_ref_fields=entity.non_ref_fields,
            type_mapper=type_mapper
        ) + ref_data.other_field_data

        return cls(
            entity_name=entity.name,
            pk_field_data=pk_data,
            fk_field_data=ref_data.fk_field_data,
            other_field_data=other_data,
            entity=entity
        )

    def get_field_data(self) -> List[FieldData]:
        return self.pk_field_data + self.other_field_data + self.fk_field_data

    def get_non_pk_field_data(self) -> List[FieldData]:
        return self.other_field_data + self.fk_field_data

    def get_pk_and_fk_field_data(self) -> List[FieldData]:
        return self.pk_field_data + self.fk_field_data


@dataclass
class FileData:
    file_path: str
    file_name: str
    file_content: List[str]
