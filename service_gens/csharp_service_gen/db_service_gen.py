from os import path
from typing import Generator, List

from data_type_mapper.data_type_mapper import TypeMapper
from entity_parser.entity import Entity, FieldData, FieldType
from service_gens.service_gen import ServiceGenerator, ServiceUtil
from utils.constants import TAB_4, TAB_8
from utils.utils import EntityFieldData, FileData

ZERO: int = 0
ONE: int = 1
INTERFACES: str = "Interfaces"
MODELS: str = "Models"
REPOS: str = "Repos"
SERVICES: str = "Services"
SQL_COMMANDS: str = "SqlCommands"
CS_EXT: str = ".cs"


class DbServiceUtil(ServiceUtil):
    # file paths
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

    # namespaces
    @property
    def model_ns(self) -> str:
        return self.get_name_space(MODELS)

    @property
    def repos_ns(self) -> str:
        return self.get_name_space(REPOS)

    @property
    def interfaces_ns(self) -> str:
        return self.get_name_space(INTERFACES)

    @property
    def sql_cmd_ns(self) -> str:
        return self.get_name_space(INTERFACES)

    @property
    def sql_cmd_interface_name(self) -> str:
        return "ISqlCommand"

    @property
    def services_ns(self) -> str:
        return self.get_name_space(SERVICES)

    # utility methods
    def get_file_name(self, cls_name: str) -> str:
        return f"{cls_name}{CS_EXT}"

    def get_get_param_name(self, cls_name: str) -> str:
        return f"{cls_name}GetParam"

    def get_list_param_name(self, cls_name: str) -> str:
        return f"{cls_name}ListParam"

    def get_interface_name(self, cls_name: str) -> str:
        return f"I{cls_name}"

    def get_name_space(self, dir: str) -> str:
        return f"{self.service_name}.{dir}"

    def get_path(self, dir: str) -> str:
        return path.join(self.output_path, dir)

    def get_repo_interface_name(self, cls_name: str) -> str:
        return f"I{cls_name}Repo"

    def get_var_name(self, cls_name: str) -> str:
        return cls_name[ZERO].lower() + cls_name[ONE:]

    def normalize_name(self, cls_name: str) -> str:
        return cls_name[ZERO].upper() + cls_name[ONE:]


class DbServiceGenerator(ServiceGenerator):
    def __init__(
        self,
        service_name: str,
        svc_dir: DbServiceUtil,
        entities: List[Entity],
        pl_type_mapper: TypeMapper,
        db_type_mapper: TypeMapper = None
    ):
        super().__init__(
            service_name=service_name,
            entities=entities,
            pl_type_mapper=pl_type_mapper,
            db_type_mapper=db_type_mapper
        )
        self.svc_dir = svc_dir

    def gen_service(self) -> Generator[FileData, None, None]:
        # Generate sql command interface
        yield self._gen_sql_command_interface()

        # Generate files for each entity
        for entity in self.entities:
            ent_name: str = self.svc_dir.normalize_name(entity.name)

            # Generate repo interfaces
            yield self._gen_repo_interface(ent_name)

            entity_file_data = EntityFieldData.from_entity(
                entity, self.pl_type_mapper
            )

            # Generate Db Models
            for model in self._gen_db_models(entity_file_data, ent_name):
                yield model

    # Db models section
    def _gen_db_models(
        self, entity: EntityFieldData, ent_name: str
    ) -> Generator[FileData, None, None]:
        file_path: str = self.svc_dir.models_dir_path
        yield self._gen_db_model(
            field_data=entity.pk_field_data,
            class_name=self.svc_dir.get_list_param_name(ent_name),
            file_path=file_path,
            is_list=True
        )

        yield self._gen_db_model(
            field_data=entity.pk_field_data,
            class_name=self.svc_dir.get_get_param_name(ent_name),
            file_path=file_path
        )

        yield self._gen_db_model(
            field_data=entity.get_field_data(),
            class_name=ent_name,
            file_path=file_path
        )

    def _gen_db_model(
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
            f"namespace {self.svc_dir.model_ns}",
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

    # Interfaces section
    def _gen_repo_interface(self, ent_name: str) -> FileData:
        get_param: str = self.svc_dir.get_get_param_name(ent_name)
        get_param_var: str = self.svc_dir.get_var_name(get_param)
        list_param: str = self.svc_dir.get_list_param_name(ent_name)
        list_param_var: str = self.svc_dir.get_var_name(list_param)
        interface_name: str = self.svc_dir.get_repo_interface_name(ent_name)
        ent_var_name: str = self.svc_dir.get_var_name(ent_name)
        file_content = [
            f"using {self.svc_dir.model_ns};",
            "",
            f"namespace {self.svc_dir.interfaces_ns}",
            "{",
            f"{TAB_4}public interface {interface_name}",
            f"{TAB_4}{{",
            f"{TAB_8}Task<{ent_name}?> GetAsync({get_param} {get_param_var});",
            f"{TAB_8}Task<IEnumerable<{ent_name}>> ListAsync"
            f"({list_param} {list_param_var});",
            f"{TAB_8}Task<int> CreateAsync({ent_name} {ent_var_name});",
            f"{TAB_8}Task<int> UpdateAsync({ent_name} {ent_var_name});",
            f"{TAB_8}Task<int> DeleteAsync({get_param} {get_param_var});",
            f"{TAB_4}}}",
            "}"
        ]
        return FileData(
            file_path=self.svc_dir.interfaces_dir_path,
            file_name=self.svc_dir.get_file_name(interface_name),
            file_content=file_content
        )

    def _gen_sql_command_interface(self) -> FileData:
        ent_name: str = self.svc_dir.sql_cmd_interface_name
        file_content = [
            f"namespace {self.svc_dir.interfaces_ns}",
            "{",
            f"{TAB_4}public interface {ent_name}",
            f"{TAB_4}{{",
            f"{TAB_8}string GetCommand {{ get; }}",
            f"{TAB_8}string ListCommand {{ get; }}",
            f"{TAB_8}string CreateCommand {{ get; }}",
            f"{TAB_8}string UpdateCommand {{ get; }}",
            f"{TAB_8}string DeleteCommand {{ get; }}",
            f"{TAB_4}}}",
            "}"
        ]
        return FileData(
            file_path=self.svc_dir.interfaces_dir_path,
            file_name=self.svc_dir.get_file_name(ent_name),
            file_content=file_content
        )
