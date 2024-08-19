import os
import subprocess
from data_type_mapper.data_type_mapper import TypeMapper
from entity_parser.entity_parser import JsonSchemaParser
from service_gens.csharp_service_gen.db_service_gen import (
    DbServiceGenerator
)
from service_gens.csharp_service_gen.utils import (
    SECRET_MANAGER, CsharpServiceUtil
)
from service_gens.service_gen import CSharpTypeMapper
from sql_generator.sql_generator import SqlCommandGenerator, TableSqlGenerator
from utils.utils import write_file_data


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
        file_content: str,
        sql_gen: SqlCommandGenerator,
        db_type_mapper: TypeMapper,
        db_script_gen: TableSqlGenerator
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
        svc_dir = CsharpServiceUtil(
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
            sql_gen=sql_gen
        )

        for file_data in service_gen.gen_service():
            write_file_data(file_data)

        # Write db scripts
        db_scripts_data = db_script_gen.gen_db_scripts_file_data(
            entities=entities,
            type_mapper=db_type_mapper,
            file_path=svc_dir.db_scripts_dir_path,
            file_name=svc_dir.db_scripts_file_name
        )
        write_file_data(db_scripts_data)
