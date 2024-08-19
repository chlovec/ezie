from os import path
import os
import subprocess
from entity_parser.entity_parser import JsonSchemaParser
from service_gens.csharp_service_gen.db_service_gen import (
    DbServiceGenerator, DbServiceUtil
)
from service_gens.service_gen import CSharpTypeMapper, ServiceUtil
from sql_generator.sql_generator import PgsqlCommandGenerator
from utils.utils import FileData

ZERO: int = 0
ONE: int = 0

CLASS_1_CS: str = "Class1.cs"
CS_EXT: str = ".cs"
DB_SCRIPTS: str = "DbScripts"
DB_SERVICE = "DbService"
DB_SERVICES: str = "DbServices"
ENV_MANAGER: str = "EnvManagers"
INTERFACES: str = "Interfaces"
MODELS: str = "Models"
REPOS: str = "Repos"
SQL_COMMANDS: str = "SqlCommands"
SECRET_MANAGER: str = "SecretManager"


class CsharpServiceUtil(ServiceUtil):
    # file paths
    @property
    def db_scripts_dir_path(self) -> str:
        return path.join(self.sln_path, DB_SCRIPTS)

    @property
    def env_mgr_dir_path(self) -> str:
        return path.join(self.secret_mgr_dir_path, ENV_MANAGER)

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
    def db_services_dir_path(self) -> str:
        return self.get_path(DB_SERVICES)

    @property
    def secret_mgr_dir_path(self) -> str:
        return path.join(self.sln_path, self.src, SECRET_MANAGER)

    @property
    def sql_cmd_dir_path(self) -> str:
        return self.get_path(SQL_COMMANDS)

    # namespaces
    @property
    def db_service_ns(self) -> str:
        return self.get_name_space(DB_SERVICES)

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

    # interfaces
    @property
    def db_service_interface_name(self) -> str:
        return "IDbService"

    @property
    def sql_cmd_interface_name(self) -> str:
        return "ISqlCommand"

    # class names
    @property
    def db_service_class_name(self) -> str:
        return DB_SERVICE

    @property
    def proj_full_name(self) -> str:
        return path.join(self.service_path, self.service_name + ".csproj")

    @property
    def secret_mgr_full_name(self) -> str:
        return path.join(self.secret_mgr_dir_path, SECRET_MANAGER + ".csproj")

    @property
    def secret_mgr_class1_cs(self) -> str:
        return path.join(self.secret_mgr_dir_path, CLASS_1_CS)

    @property
    def service_class1_cs(self) -> str:
        return path.join(self.service_path, CLASS_1_CS)

    @property
    def sln_full_name(self) -> str:
        return path.join(self.sln_path, self.sln_name + ".sln")

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
        return path.join(self.service_path, dir)

    def get_repo_interface_name(self, cls_name: str) -> str:
        return f"I{cls_name}Repo"

    def get_repo_name(self, cls_name: str) -> str:
        return f"{cls_name}Repo"

    def get_var_name(self, cls_name: str) -> str:
        return cls_name[ZERO].lower() + cls_name[ONE:]

    def normalize_name(self, cls_name: str) -> str:
        return cls_name[ZERO].upper() + cls_name[ONE:]

    def get_sql_cmd_name(self, cls_name: str) -> str:
        return f"{cls_name}SqlCommand"


class DotnetProcessRunner:
    @staticmethod
    def setup_project(
        svc_util: CsharpServiceUtil, create_db_scripts_dir: bool = True
    ) -> None:
        DotnetProcessRunner.create_sln(svc_util)
        DotnetProcessRunner.create_db_service(svc_util)
        DotnetProcessRunner.create_secret_manager(svc_util)

        # Create directories
        dir_paths = [
            svc_util.env_mgr_dir_path,
            svc_util.models_dir_path,
            svc_util.repos_dir_path,
            svc_util.interfaces_dir_path,
            svc_util.db_services_dir_path,
            svc_util.sql_cmd_dir_path
        ]

        if create_db_scripts_dir:
            dir_paths.append(svc_util.db_scripts_dir_path)

        for dir_path in dir_paths:
            os.mkdir(dir_path)

        # Delete Class1.cs files
        os.remove(svc_util.service_class1_cs)
        os.remove(svc_util.secret_mgr_class1_cs)

    @staticmethod
    def create_sln(svc_util: CsharpServiceUtil) -> None:
        sln_name: str = svc_util.sln_name
        sln_dir: str = svc_util.sln_path
        subprocess.run([
            "dotnet", "new", "sln", "-n", sln_name, "-o", sln_dir
        ])

    @staticmethod
    def create_db_service(svc_util: CsharpServiceUtil) -> None:
        # Create class library for db service
        proj_name: str = svc_util.service_name
        proj_path: str = svc_util.service_path
        DotnetProcessRunner.create_class_lib(proj_name, proj_path)

        # Add class library to the solution
        sln_full_name: str = svc_util.sln_full_name
        proj_full_name: str = svc_util.proj_full_name
        DotnetProcessRunner.add_proj_to_solution(
            sln_full_name, proj_full_name
        )

        # Add dapper package
        DotnetProcessRunner.add_package(proj_path, "Dapper")

    @staticmethod
    def create_secret_manager(svc_util: CsharpServiceUtil) -> None:
        # Create class library for db service
        proj_name: str = SECRET_MANAGER
        proj_path: str = svc_util.secret_mgr_dir_path
        DotnetProcessRunner.create_class_lib(proj_name, proj_path)

        # Add class library to the solution
        sln_full_name: str = svc_util.sln_full_name
        proj_full_name: str = svc_util.secret_mgr_full_name
        DotnetProcessRunner.add_proj_to_solution(
            sln_full_name, proj_full_name
        )

    @staticmethod
    def create_class_lib(proj_name: str, proj_dir: str) -> None:
        subprocess.run([
            "dotnet", "new", "classlib", "-n", proj_name, "-o", proj_dir
        ])

    @staticmethod
    def add_proj_to_solution(sln_full_name: str, proj_full_name: str) -> None:
        subprocess.run([
            "dotnet", "sln", sln_full_name, "add", proj_full_name
        ])

    def add_package(proj_path: str, package_name: str) -> None:
        os.chdir(proj_path)
        subprocess.run(
            ["dotnet", "add", "package", package_name],
            check=True,
            text=True
        )


class CsharpRestServiceGenerator:
    @staticmethod
    def gen_services_from_file_content(
        output_path: str,
        sln_name: str,
        service_name: str,
        file_content: str
    ) -> None:
        # Setup project
        svc_util = CsharpServiceUtil(
            output_path=output_path,
            sln_name=sln_name,
            service_name=service_name + "Dal",
            src="src"
        )
        DotnetProcessRunner.setup_project(svc_util)

        # Parse Json Schema
        parser = JsonSchemaParser()
        entities = parser.parse(file_content=file_content)

        # Generate and write db service files
        svc_dir = DbServiceUtil(
            output_path=output_path,
            sln_name=sln_name,
            service_name=service_name + "Dal",
            src="src"
        )
        service_gen = DbServiceGenerator(
            service_name=service_name,
            svc_dir=svc_dir,
            entities=entities,
            pl_type_mapper=CSharpTypeMapper(),
            db_type_mapper=None,
            sql_gen=PgsqlCommandGenerator(entity=None)
        )

        for file_data in service_gen.gen_service():
            CsharpRestServiceGenerator.write_file_data(file_data)

    @staticmethod
    def write_file_data(file_data: FileData) -> None:
        file_path = os.path.join(file_data.file_path, file_data.file_name)
        with open(file_path, "w") as file:
            for line in file_data.file_content:
                file.write(line + "\n")
