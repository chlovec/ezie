from abc import ABC, abstractmethod
from enum import Enum
from os import path
from typing import Generator, List

from data_type_mapper.data_type_mapper import (
    LOWER_LIMIT_SBYTE, NEG_BIGINT, NEG_INTEGER, NEG_SMALLINT, POS_BIGINT,
    POS_INTEGER, POS_SMALLINT, UPPER_LIMIT_BYTE, UPPER_LIMIT_SBYTE,
    UPPER_LIMIT_UINT, UPPER_LIMIT_ULONG, UPPER_LIMIT_USHORT, TypeMapper
)
from entity_parser.entity import Entity, EntityField, FieldFormat, FieldType
from utils.utils import FileData


class CSharpDataType(Enum):
    BOOLEAN = "bool"
    BYTE = "byte"
    SBYTE = "sbyte"
    CHAR = "char"
    DECIMAL = "decimal"
    DOUBLE = "double"
    FLOAT = "float"
    INT = "int"
    UINT = "uint"
    LONG = "long"
    ULONG = "ulong"
    SHORT = "short"
    USHORT = "ushort"
    STRING = "string"
    DATETIME = "dateTime"
    DATETIMEOFFSET = "DateTimeOffset"
    TIMESPAN = "TimeSpan"
    GUID = "Guid"


class CSharpTypeMapper(TypeMapper):
    """_summary_
    Class for mapping data from json type to C# data type
    """

    def _get_int_type(self, minimum: int, maximum: int) -> str:
        if maximum and not minimum:
            if maximum <= UPPER_LIMIT_BYTE:
                return CSharpDataType.BYTE.value
            elif maximum <= UPPER_LIMIT_USHORT:
                return CSharpDataType.USHORT.value
            elif maximum <= UPPER_LIMIT_UINT:
                return CSharpDataType.UINT.value
            elif maximum <= UPPER_LIMIT_ULONG:
                return CSharpDataType.ULONG.value
        elif maximum and minimum:
            if minimum >= LOWER_LIMIT_SBYTE and maximum <= UPPER_LIMIT_SBYTE:
                return CSharpDataType.SBYTE.value
            elif minimum >= NEG_SMALLINT and maximum <= POS_SMALLINT:
                return CSharpDataType.SHORT.value
            elif minimum >= NEG_INTEGER and maximum <= POS_INTEGER:
                return CSharpDataType.INT.value
            elif minimum >= NEG_BIGINT and maximum <= POS_BIGINT:
                return CSharpDataType.LONG.value
        elif minimum:
            if minimum >= NEG_SMALLINT:
                return CSharpDataType.SHORT.value
            elif minimum >= NEG_INTEGER:
                return CSharpDataType.INT.value
            elif minimum >= NEG_BIGINT:
                return CSharpDataType.LONG.value
        elif maximum:
            if maximum <= POS_SMALLINT:
                return CSharpDataType.SHORT.value
            elif maximum <= POS_INTEGER:
                return CSharpDataType.INT.value
            elif maximum <= POS_BIGINT:
                return CSharpDataType.LONG.value

        return CSharpDataType.INT.value

    def _get_num_type(self, format: FieldFormat) -> str:
        if format == FieldFormat.DOUBLE:
            return CSharpDataType.DOUBLE.value
        elif format == FieldFormat.FLOAT:
            return CSharpDataType.FLOAT.value
        elif format == FieldFormat.DECIMAL:
            return CSharpDataType.DECIMAL.value
        return CSharpDataType.DOUBLE.value

    def _get_string_type(
        self, format: FieldFormat, min_len: int, max_len: int
    ) -> str:
        if format == FieldFormat.BYTE:
            return CSharpDataType.BYTE.value
        elif format == FieldFormat.DATE:
            return CSharpDataType.DATETIME.value
        elif format == FieldFormat.DATETIME:
            return CSharpDataType.DATETIMEOFFSET.value
        elif format == FieldFormat.TIME:
            return CSharpDataType.TIMESPAN.value
        elif format == FieldFormat.UUID:
            return CSharpDataType.GUID.value
        elif min_len and min_len == max_len:
            return CSharpDataType.CHAR.value

        return CSharpDataType.STRING.value

    def get_field_type(self, entity_field: EntityField) -> str:
        if entity_field.field_type == FieldType.STRING:
            return self._get_string_type(
                entity_field.format,
                entity_field.minimum,
                entity_field.maximum
            )
        elif entity_field.field_type == FieldType.INTEGER:
            return self._get_int_type(
                entity_field.minimum, entity_field.maximum
            )
        elif entity_field.field_type == FieldType.NUMBER:
            return self._get_num_type(entity_field.format)
        elif entity_field.field_type == FieldType.BOOLEAN:
            return CSharpDataType.BOOLEAN.value
        return None

    def get_enum_field_type(self, entity: Entity) -> str:
        return CSharpDataType.STRING


class ServiceUtil(ABC):
    def __init__(
        self, output_path: str, sln_name: str, service_name: str, src: str
    ):
        self.output_path = path.join(
            output_path, sln_name, src, service_name
        )
        self.service_name = service_name

    @abstractmethod
    def get_file_name(self, cls_name: str) -> str:
        pass

    @abstractmethod
    def get_get_param_name(self, cls_name: str) -> str:
        pass

    @abstractmethod
    def get_list_param_name(self, cls_name: str) -> str:
        pass

    @abstractmethod
    def get_interface_name(self, cls_name: str) -> str:
        pass

    @abstractmethod
    def get_name_space(self, dir: str) -> str:
        pass

    @abstractmethod
    def get_path(self, dir: str) -> str:
        pass

    @abstractmethod
    def get_var_name(self, cls_name: str) -> str:
        pass

    @abstractmethod
    def normalize_name(self, cls_name: str) -> str:
        pass


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
