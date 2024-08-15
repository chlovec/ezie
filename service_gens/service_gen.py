from abc import ABC, abstractmethod
from typing import Generator, List

from data_type_mapper.data_type_mapper import TypeMapper
from entity_parser.entity import Entity
from utils.utils import FileData


class ServiceGenerator(ABC):
    def __init__(
        self,
        output_path: str,
        sln_name: str,
        service_name: str,
        entities: List[Entity],
        pl_type_mapper: TypeMapper,
        db_type_mapper: TypeMapper = None
    ):
        self.output_path = output_path
        self.sln_name = sln_name
        self.service_name = service_name
        self.entities = entities
        self.pl_type_mapper = pl_type_mapper
        self.db_type_mapper = db_type_mapper

    @abstractmethod
    def gen_service(self) -> Generator[FileData, None, None]:
        """
        Generates the file contents for the service to be created.

        Returns:
            List[FileData]: A list of file data that are part of the service.
        """
        pass
