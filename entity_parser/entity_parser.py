
from abc import ABC, abstractmethod
import json
from typing import Any, Dict, List, Set, Union

from entity_parser.entity import Entity, EntityField, FieldType, RefEntityField


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


class JsonSchemaParser(EntityParser):
    def __init__(self) -> None:
        super().__init__()
        self.created_objects: Dict[str, Entity] = {}
        self.obj_attributes: Dict[str. List[EntityField]] = {}

    def parse(
        self, file_content: str = None, file_path: str = None
    ) -> List[Entity]:
        schema: Dict[str, Any] = {}
        if file_content:
            schema = json.loads(file_content)
        elif file_path:
            with open(file_path) as file:
                schema = json.load(file)
        else:
            raise ValueError(
                """
                Either `file_content` or `file_path` is require but
                none was provided
                """
            )

        self._process_schema(schema, True)
        for obj_name, attributes in self.obj_attributes.items():
            self._update_entity_fields(obj_name, attributes)

        return list(self.created_objects.values())

    def _get_field_type(self, field_type: str) -> Union[FieldType, None]:
        if not field_type:
            return None

        try:
            return FieldType(field_type)
        except KeyError:
            raise ValueError(f"`{field_type}` is not a valid JSON type")

    def _get_type_ref(self, type_ref: str) -> str:
        if not type_ref:
            return None

        refs = type_ref.split("/")
        if len(refs) == THREE:
            return refs[TWO]

        raise ValueError(f"Json schema contains invalid ref `{type_ref}`")

    def _process_schema(
        self, schema: Dict[str, Any], process_title: bool = False
    ) -> None:
        if not schema:
            return

        self._process_definitions(
            schema, "definitions"
        )
        self._process_definitions(
            schema, "$defs"
        )

        if process_title:
            self._process_titles(schema)

    def _process_definitions(
        self, schema: Dict[str, Any], obj_key: str
    ) -> None:
        definitions = schema.get(obj_key, {})
        self._process_schema(definitions)

        # Create the entities first
        for obj_name in definitions:
            if self.created_objects.get(obj_name, None):
                continue

            self.created_objects[obj_name] = Entity(
                name=obj_name,
                non_ref_fields=[],
                ref_fields=[],
                pk_fields=[]
            )

        for obj_name, obj_defs in definitions.items():
            self._process_obj_properties(
                obj_name=obj_name,
                obj_properties=obj_defs.get("properties", {}),
                required_props=set(obj_defs.get("required", []))
            )

    def _process_titles(self, schema: Dict[str, Any]) -> None:
        id: str = schema.get("title", '')
        if not id:
            id = schema.get("$id", '')

        if not id:
            return

        obj_name: str = id.split('/')[-1]
        self.created_objects[obj_name] = Entity(
            name=obj_name,
            non_ref_fields=[],
            ref_fields=[],
            pk_fields=[]
        )
        self._process_obj_properties(
            obj_name=obj_name,
            obj_properties=schema.get("properties", {}),
            required_props=set(schema.get("required", []))
        )

    def _process_obj_properties(
        self,
        obj_name: str,
        obj_properties: Dict[str, Any],
        required_props: Set[str]
    ) -> None:
        self._process_schema(obj_properties)

        attributes: List[EntityField] = []
        for prop_name, prop_def in obj_properties.items():
            type_ref: str = ""
            prop_type: FieldType = self._get_field_type(
                prop_def.get("type", "")
            )
            if prop_type and prop_type == FieldType.OBJECT:
                self.created_objects[prop_name] = Entity(
                    name=prop_name,
                    non_ref_fields=[],
                    ref_fields=[],
                    pk_fields=[]
                )
                self._process_obj_properties(
                    obj_name=prop_name,
                    obj_properties=prop_def.get("properties", {}),
                    required_props=prop_def.get("required", [])
                )
                type_ref = prop_name
            else:
                type_ref = self._get_type_ref(prop_def.get("$ref", None))

            enum_values: List[Any] = prop_def.get("enum", [])
            attributes.append(
                EntityField(
                    name=prop_name,
                    field_type=prop_type,
                    max_length=prop_def.get("maxLength", None),
                    is_required=(prop_name in required_props),
                    is_primary_key=prop_def.get("primaryKey", False),
                    type_ref=type_ref,
                    format=prop_def.get("format", None),
                    is_enum=bool(enum_values),
                    enum_values=enum_values
                ))

        self.obj_attributes[obj_name] = attributes

    def _update_entity_fields(
        self, class_name: str, attributes: List[EntityField]
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
                    `{class_name}.{field.name}`
                    """
                )
            elif field.type_ref and field.type_ref not in self.created_objects:
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
                        ref_entity=self.created_objects[field.type_ref],
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
            if pk_field:
                pk_fields = [pk_field]

        # Remove all pk_fields from non_ref_fields
        non_ref_fields = [
            field for field in non_ref_fields if field not in pk_fields
        ]

        # Update entity
        self.created_objects[class_name].non_ref_fields = non_ref_fields
        self.created_objects[class_name].ref_fields = ref_fields
        self.created_objects[class_name].pk_fields = pk_fields
