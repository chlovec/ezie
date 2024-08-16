from enum import Enum
from data_type_mapper.data_type_mapper import (
    NEG_BIGINT, NEG_INTEGER, NEG_SMALLINT, POS_BIGINT, POS_INTEGER,
    POS_SMALLINT, TypeMapper
)
from entity_parser.entity import Entity, EntityField, FieldFormat, FieldType


class PgSQLDataType(Enum):
    # Numeric Types
    SMALLINT = "smallint"
    INTEGER = "integer"
    BIGINT = "bigint"
    DECIMAL = "decimal"
    NUMERIC = "numeric"
    REAL = "real"
    DOUBLE = "double precision"
    SMALLSERIAL = "smallserial"
    SERIAL = "serial"
    BIGSERIAL = "bigserial"

    # Monetary Types
    MONEY = "money"

    # Character Types
    CHAR = "char"
    VARCHAR = "varchar"
    TEXT = "text"

    # Binary Data Types
    BYTEA = "bytea"

    # Date/Time Types
    TIMESTAMP = "timestamp"
    TIMESTAMPTZ = "timestamptz"
    DATE = "date"
    TIME = "time"
    TIMETZ = "timetz"
    INTERVAL = "interval"

    # Boolean Type
    BOOLEAN = "boolean"

    # Enumerated Types
    ENUM = "enum"

    # Geometric Types
    POINT = "point"
    LINE = "line"
    LSEG = "lseg"
    BOX = "box"
    PATH = "path"
    POLYGON = "polygon"
    CIRCLE = "circle"

    # Network Address Types
    CIDR = "cidr"
    INET = "inet"
    MACADDR = "macaddr"

    # JSON Types
    JSON = "json"
    JSONB = "jsonb"

    # XML Type
    XML = "xml"

    # UUID Type
    UUID = "uuid"

    # Array Type
    ARRAY = "array"

    # Composite Types
    COMPOSITE = "composite"

    # Range Types
    INT4RANGE = "int4range"
    INT8RANGE = "int8range"
    NUMRANGE = "numrange"
    TSRANGE = "tsrange"
    TSTZRANGE = "tstzrange"
    DATERANGE = "daterange"

    # Other Types
    TSQUERY = "tsquery"
    TSVECTOR = "tsvector"
    UNKNOWN = "unknown"


class PgsqlTypeMapper(TypeMapper):
    """_summary_
    Class for mapping data from json type to pgsql data type
    """

    def get_array_type(self, entity_field: EntityField) -> str:
        return PgSQLDataType.ARRAY

    def _get_int_type(self, minimum: int, maximum: int) -> str:
        if maximum and minimum:
            if minimum >= NEG_SMALLINT and maximum <= POS_SMALLINT:
                return PgSQLDataType.SMALLINT.name
            elif minimum >= NEG_INTEGER and maximum <= POS_INTEGER:
                return PgSQLDataType.INTEGER.name
            elif minimum >= NEG_BIGINT and maximum <= POS_BIGINT:
                return PgSQLDataType.BIGINT.name
        elif minimum:
            if minimum >= NEG_SMALLINT:
                return PgSQLDataType.SMALLINT.name
            elif minimum >= NEG_INTEGER:
                return PgSQLDataType.INTEGER.name
            elif minimum >= NEG_BIGINT:
                return PgSQLDataType.BIGINT.name
        elif maximum:
            if maximum <= POS_SMALLINT:
                return PgSQLDataType.SMALLINT.name
            elif maximum <= POS_INTEGER:
                return PgSQLDataType.INTEGER.name
            elif maximum <= POS_BIGINT:
                return PgSQLDataType.BIGINT.name

        return PgSQLDataType.INTEGER.name

    def _get_num_type(self, format: FieldFormat) -> str:
        if format == FieldFormat.DOUBLE:
            return PgSQLDataType.DOUBLE.name
        elif format == FieldFormat.FLOAT:
            return PgSQLDataType.REAL.name
        return PgSQLDataType.DOUBLE.name

    def _get_string_type(self, format: FieldFormat, max_length: int) -> str:
        if format == FieldFormat.BYTE:
            return PgSQLDataType.BYTEA.name
        elif format == FieldFormat.DATE:
            return PgSQLDataType.DATE.name
        elif format == FieldFormat.DATETIME:
            return PgSQLDataType.TIMESTAMPTZ.name
        elif format == FieldFormat.TIME:
            return PgSQLDataType.TIME.name
        elif format == FieldFormat.IPV4:
            return PgSQLDataType.CIDR.name
        elif format == FieldFormat.IPV6:
            return PgSQLDataType.CIDR.name
        elif format == FieldFormat.JSON:
            return PgSQLDataType.JSON.name
        elif format == FieldFormat.MAC:
            return PgSQLDataType.MACADDR.name
        elif format == FieldFormat.UUID:
            return PgSQLDataType.UUID.name
        elif max_length:
            return f"{PgSQLDataType.VARCHAR.name}({max_length})"
        return PgSQLDataType.TEXT.name

    def get_field_type(self, entity_field: EntityField) -> str:
        if entity_field.field_type == FieldType.STRING:
            return self._get_string_type(
                entity_field.format, entity_field.max_length
            )
        elif entity_field.field_type == FieldType.INTEGER:
            return self._get_int_type(
                entity_field.minimum, entity_field.maximum
            )
        elif entity_field.field_type == FieldType.NUMBER:
            return self._get_num_type(entity_field.format)
        elif entity_field.field_type == FieldType.BOOLEAN:
            return PgSQLDataType.BOOLEAN.name
        return None

    def get_enum_field_type(self, entity: Entity) -> str:
        return "VARCHAR(50)"
