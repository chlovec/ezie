from os import path
import os
import subprocess
from service_gens.service_gen import ServiceUtil

ZERO: int = 0
ONE: int = 0

CS_EXT: str = ".cs"


class CsharpServiceUtil(ServiceUtil):
    @property
    def proj_full_name(self) -> str:
        return path.join(self.service_path, self.service_name + ".csproj")

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

    def get_var_name(self, cls_name: str) -> str:
        return cls_name[ZERO].lower() + cls_name[ONE:]

    def normalize_name(self, cls_name: str) -> str:
        return cls_name[ZERO].upper() + cls_name[ONE:]


class DotnetProcessRunner:
    @staticmethod
    def setup_project(svc_util: CsharpServiceUtil) -> None:
        DotnetProcessRunner.create_sln(svc_util)
        DotnetProcessRunner.create_db_service(svc_util)
        # TO-DOS:
        # create secret manager class library
        # create solution directories
        # create project directories

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
