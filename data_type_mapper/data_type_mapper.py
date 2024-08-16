from abc import ABC, abstractmethod

from entity_parser.entity import Entity, EntityField


NEG_BIGINT: int = -9223372036854775808
POS_BIGINT: int = 9223372036854775807
NEG_INTEGER: int = -2147483648
POS_INTEGER: int = 2147483647
NEG_SMALLINT: int = -32768
POS_SMALLINT: int = 32767


class TypeMapper(ABC):
    @abstractmethod
    def get_field_type(self, entity_field: EntityField) -> str:
        pass

    @abstractmethod
    def get_enum_field_type(self, entity: Entity) -> str:
        pass
