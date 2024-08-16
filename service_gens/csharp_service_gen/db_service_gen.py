from abc import abstractmethod
from os import path
from typing import Generator, List

from entity_parser.entity import FieldData, FieldType
from service_gens.service_gen import ServiceGenerator
from utils.constants import TAB_4, TAB_8
from utils.utils import EntityFieldData, FileData


INTERFACES: str = "Interfaces"
MODELS: str = "Models"
REPOS: str = "Repos"
SERVICES: str = "Services"
SQL_COMMANDS: str = "SqlCommands"
SRC: str = "src"
CS_EXT: str = ".cs"


class DbServiceDirectory:
    def __init__(self, output_path: str, sln_name: str, db_service_name: str):
        self.output_path = path.join(
            output_path, sln_name, SRC, db_service_name
        )

    def get_path(self, dir: str) -> str:
        return path.join(self.output_path, dir)

    @property
    def interfaces_dir_path(self) -> str:
        return self.get_path(INTERFACES)

    @property
    def models_dir_path(self) -> str:
        return self.get_path(MODELS)

    @property
    def repos_dir_path(self) -> str:
        return self.get_path(REPOS)

    @property
    def services_dir_path(self) -> str:
        return self.get_path(SERVICES)

    @property
    def sql_cmd_dir_path(self) -> str:
        return self.get_path(SQL_COMMANDS)


class DbServiceGenerator(ServiceGenerator):
    def gen_service(self) -> Generator[FileData, None, None]:
        svc_dir = DbServiceDirectory(
            self.output_path, self.sln_name, self.service_name
        )
        for entity in self.entities:
            entity_file_data = EntityFieldData.from_entity(
                entity, self.pl_type_mapper
            )
            yield self._gen_entity_service(entity_file_data, svc_dir)

    @abstractmethod
    def _gen_entity_service(
        self, entity: EntityFieldData, svc_dir: DbServiceDirectory
    ) -> Generator[FileData, None, None]:
        pass


class DbServiceModelGenerator(DbServiceGenerator):
    def _gen_entity_service(
        self, entity: EntityFieldData, svc_dir: DbServiceDirectory
    ) -> Generator[FileData, None, None]:
        file_path: str = svc_dir.models_dir_path
        yield self._create_entity(
            field_data=entity.pk_field_data,
            class_name=f"List{entity.entity_name}Param",
            file_path=file_path,
            is_list=True
        )

        yield self._create_entity(
            field_data=entity.pk_field_data,
            class_name=f"Get{entity.entity_name}Param",
            file_path=file_path
        )

        yield self._create_entity(
            field_data=entity.get_field_data(),
            class_name=entity.entity_name,
            file_path=file_path
        )

    @property
    def _name_space(self) -> str:
        return f"{self.service_name}.{MODELS}"

    def _create_entity(
        self,
        field_data: List[FieldData],
        class_name: str,
        file_path: str,
        is_list: bool = False
    ) -> FileData:
        # Handle no content
        if not field_data:
            return FileData(file_path="", file_name="", file_content=[])

        # Open class definition with namespace
        file_content: List[str] = [
            f"namespace {self._name_space}",
            "{",
            f"{TAB_4}public class {class_name}",
            f"{TAB_4}{{"
        ]

        # Add class properties
        for fld in field_data:
            null_type = "" if fld.is_required else "?"
            default_clause = self._get_default_clause(fld)
            prop_type = fld.data_type
            fld_name = fld.name

            # handle list properties
            if is_list:
                prop_type = f"IEnumerable<{fld.data_type}>"
                fld_name = f"{fld_name}s"

            file_content.append(
                f"{TAB_8}public {prop_type}{null_type} {fld_name} "
                f"{{ get; set; }}{default_clause}"
            )

        if is_list:
            file_content.extend(self._get_pagination_content())

        # Close class definition
        file_content.append(f"{TAB_4}}}")
        file_content.append("}")

        return FileData(
            file_path=file_path,
            file_name=f"{class_name}{CS_EXT}",
            file_content=file_content
        )

    def _get_pagination_content(self) -> List[str]:
        return [
            f"{TAB_8}public int Limit {{ get; set; }} = 1000;",
            f"{TAB_8}public int OffSet {{ get; set; }} = 0;"
        ]

    def _get_default_clause(self, field: FieldData) -> str:
        if field.is_required and field.data_type == FieldType.STRING.value:
            return " = default!;"
        return ""
