
from abc import ABC, abstractmethod
import json
from typing import Any, Dict, List, Union

from entity_parser.entity import Entity, EntityField, RefEntityField


TWO: int = 2
THREE: int = 3


class EntityParser(ABC):
    @abstractmethod
    def parse(
        self, file_content: str = None, file_path: str = None
    ) -> List[Entity]:
        pass

    def _get_pk_fields(
        self, pk_field_names: List[str], non_ref_field: List[EntityField]
    ) -> Union[EntityField, None]:
        # Respect order of precedence in pk_field_names
        for field_name in pk_field_names:
            for field in non_ref_field:
                if field.name.lower() == field_name:
                    return field

        return None

    def _get_type_ref(self, type_ref: str) -> str:
        refs = type_ref.split("/")
        if len(refs) == THREE:
            return refs[TWO]

        raise ValueError(f"Json schema contains invalid ref '{type_ref}'")

    def _set_entity_attributes(
        self,
        class_name: str,
        attributes: List[EntityField],
        created_entities: Dict[str, Entity]
    ) -> None:
        ref_fields: List[RefEntityField] = []
        non_ref_fields: List[EntityField] = []
        pk_fields: List[EntityField] = []
        for field in attributes:
            # Validate that a referenced entity is not used as primary key
            # field
            if (
                (field.field_type == "object" or field.type_ref)
                and field.is_primary_key
            ):
                raise ValueError(
                    f"""
                    Cannot use a referenced entity as primary key field -
                    '{class_name}.{field.name}'
                    """
                )
            elif field.type_ref and field.type_ref not in created_entities:
                raise ValueError(
                    f"""
                    `{field.type_ref}` is referenced in `{class_name}` but
                    does not have a definition
                    """
                )
            elif field.type_ref:
                ref_fields.append(
                    RefEntityField(
                        name=field.name,
                        ref_entity=created_entities[field.type_ref],
                        is_required=field.is_required
                    )
                )
            elif field.is_primary_key:
                pk_fields.append(field)
            else:
                non_ref_fields.append(field)

        if not pk_fields:
            pk_field = self._get_pk_fields(
                ["id", f"{class_name}_id".lower(), f"{class_name}id".lower()],
                non_ref_fields
            )
            if not pk_field:
                raise ValueError(
                    f"No primary key field found for entity '{class_name}'"
                )

            pk_fields = [pk_field]

        # Remove all pk_fields from non_ref_fields
        non_ref_fields = [
            field for field in non_ref_fields if field not in pk_fields
        ]

        # Update entity
        created_entities[class_name].non_ref_fields = non_ref_fields
        created_entities[class_name].ref_fields = ref_fields
        created_entities[class_name].pk_fields = pk_fields

    def _create_entities(
        self, class_attributes: Dict[str, List[EntityField]]
    ) -> List[Entity]:
        # Create entities
        created_entities: Dict[str, Entity] = {}
        for class_name in class_attributes:
            created_entities[class_name] = Entity(class_name, [], [], [])

        # Create entities attributes
        for class_name, attributes in class_attributes.items():
            self._set_entity_attributes(
                class_name, attributes, created_entities
            )

        return list(created_entities.values())


class JsonSchemaParser(EntityParser):
    def parse(
        self, file_content: str = None, file_path: str = None
    ) -> List[Entity]:
        if file_content:
            schema = json.loads(file_content)
            return self._parse_schema(schema)
        elif file_path:
            with open(file_path) as file:
                return self._parse_schema(json.load(file))
        else:
            raise ValueError(
                """
                Either `file_content` or `file_path` is require but
                none was provided
                """
            )

    def _map_class_attributes(
        self, schema: Dict[str, Any]
    ) -> Dict[str, List[EntityField]]:
        # Extract definitions and process classes within it
        definitions = schema.get("definitions", {})
        class_attributes_map: Dict[str, List[EntityField]] = {}
        for class_name, class_def in definitions.items():
            properties = class_def.get("properties", {})
            attributes: List[str, EntityField] = {}

            # Extract and create class attributes
            for prop_name, prop_def in properties.items():
                type_ref = prop_def.get("$ref", None)
                type_ref = self._get_type_ref(type_ref) if type_ref else None
                ent_field = EntityField(
                    name=prop_name,
                    field_type=prop_def.get("type", None),
                    max_length=prop_def.get("maxLength", None),
                    is_primary_key=prop_def.get("primaryKey", False),
                    type_ref=type_ref,
                    format=prop_def.get("format", None)
                )
                attributes[prop_name] = ent_field

            # Extract and set required attributes
            required_attr = class_def.get("required", [])
            for prop_name in required_attr:
                attributes[prop_name].is_required = True

            # Set class attributes
            class_attributes_map[class_name] = attributes.values()

        return class_attributes_map

    def _parse_schema(self, schema: Dict[str, Any]) -> List[Entity]:
        # Extract class attributes mapping
        class_attributes: Dict[str, List[EntityField]] = (
            self._map_class_attributes(schema)
        )
        return self._create_entities(class_attributes)
