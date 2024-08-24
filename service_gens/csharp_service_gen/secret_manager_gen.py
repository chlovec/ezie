from typing import Generator, List

from service_gens.csharp_service_gen.utils import CsharpServiceUtil
from service_gens.service_gen import ServiceGenerator
from utils.constants import TAB_4, TAB_8
from utils.utils import FileData


class SecretManagerGen(ServiceGenerator):
    def __init__(
        self,
        service_name: str,
        svc_dir: CsharpServiceUtil,
    ):
        super().__init__(
            service_name=service_name,
            entities=None,
            pl_type_mapper=None,
            db_type_mapper=None
        )
        self.svc_dir = svc_dir
        self.service_name = service_name

    def gen_service(self) -> Generator[FileData, None, None]:
        file_content: List[str] = [
            f"namespace {self.svc_dir.secret_mgr_ns}",
            "{",
            "",
            f"{TAB_4}public static class {self.svc_dir.secret_mgr_class_name}",
            f"{TAB_4}{{",
            f"{TAB_8}public static string? DbUserName => Environment."
            f"GetEnvironmentVariable({self.svc_dir.secret_mgr_db_user_name});",
            f"{TAB_8}public static string? DbPassword => Environment."
            f"GetEnvironmentVariable({self.svc_dir.secret_mgr_db_password});",
            f"{TAB_8}public static string? DbName => Environment."
            f"GetEnvironmentVariable({self.svc_dir.secret_mgr_db_name});",
            f"{TAB_8}public static string? DbPort => Environment."
            f"GetEnvironmentVariable({self.svc_dir.secret_mgr_db_port});",
            f"{TAB_8}public static string? DbHost => Environment."
            f"GetEnvironmentVariable({self.svc_dir.secret_mgr_db_host});",
            f"{TAB_4}}}",
            "}"
        ]

        yield FileData(
            file_path=self.svc_dir.secret_mgr_env_mgr_dir_path,
            file_name=self.svc_dir.get_file_name(
                self.svc_dir.secret_mgr_class_name
            ),
            file_content=file_content
        )
