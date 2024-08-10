from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from entity_parser.entity import Entity, EntityField


def remove_last_comma(s: str) -> str:
    if s.endswith(','):
        return s[:-1]
    return s


@dataclass
class FileData:
    file_path: str
    file_content: List[str]


class TypeMapper(ABC):
    @abstractmethod
    def get_field_type(self, entity_field: EntityField) -> str:
        pass

    @abstractmethod
    def get_enum_field_type(self, entity: Entity) -> str:
        pass
