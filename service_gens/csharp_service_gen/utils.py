from os import path

from service_gens.service_gen import ServiceUtil

ZERO: int = 0
ONE: int = 1

CLASS_1_CS: str = "Class1.cs"
CS_EXT: str = ".cs"
DB_SCRIPT_FILE: str = "init.sql"
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
        return self.get_name_space(SQL_COMMANDS)

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

    # Secret Manager
    @property
    def secret_mgr_env_mgr_dir_path(self) -> str:
        return path.join(self.secret_mgr_dir_path, ENV_MANAGER)

    @property
    def secret_mgr_class_name(self) -> str:
        return "DbSecretManager"

    @property
    def secret_mgr_db_user_name(self) -> str:
        return '"DB_USERNAME"'

    @property
    def secret_mgr_db_password(self) -> str:
        return '"DB_PASSWORD"'

    @property
    def secret_mgr_db_name(self) -> str:
        return '"DB_NAME"'

    @property
    def secret_mgr_db_port(self) -> str:
        return '"DB_PORT"'

    @property
    def secret_mgr_db_host(self) -> str:
        return '"DB_HOST"'

    @property
    def secret_mgr_ns(self) -> str:
        return f"{SECRET_MANAGER}.{ENV_MANAGER}"

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

    @property
    def db_scripts_file_name(self) -> str:
        return DB_SCRIPT_FILE

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
