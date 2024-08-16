from abc import ABC, abstractmethod

from entity_parser.entity import Entity, EntityField


NEG_BIGINT: int = -9223372036854775808
POS_BIGINT: int = 9223372036854775807
NEG_INTEGER: int = -2147483648
POS_INTEGER: int = 2147483647
NEG_SMALLINT: int = -32768
POS_SMALLINT: int = 32767
UPPER_LIMIT_BYTE: int = 255
LOWER_LIMIT_SBYTE: int = -128
UPPER_LIMIT_SBYTE: int = 127
UPPER_LIMIT_USHORT: int = 65535
UPPER_LIMIT_UINT: int = 4294967295
UPPER_LIMIT_ULONG: int = 18446744073709551615


class TypeMapper(ABC):
    @abstractmethod
    def get_field_type(self, entity_field: EntityField) -> str:
        pass

    @abstractmethod
    def get_enum_field_type(self, entity: Entity) -> str:
        pass
