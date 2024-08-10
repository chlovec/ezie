from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Tuple

from entity_parser.entity import Entity, EntityField, FieldFormat, FieldType
from utils.constants import (
    NEG_BIGINT, NEG_INTEGER, NEG_SMALLINT, POS_BIGINT,
    POS_INTEGER, POS_SMALLINT, TAB_4
)
from utils.utils import TypeMapper, remove_last_comma


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


class SqlCommandGenerator(ABC):
    def __init__(self, entity: Entity, param_marker: str = "@"):
        self.entity: Entity = entity
        self.param_marker = param_marker

    @abstractmethod
    def _get_list_where_clause(self) -> str:
        pass

    def _get_joined_fields(self, param_marker: str = "") -> str:
        field_names = self._join_fields(self.entity, param_marker)
        return ", ".join(field_names)

    def _join_fields(
        self, entity: Entity, param_marker: str, name_prefix: str = ""
    ) -> List[str]:
        field_names: List[str] = []
        for fld in entity.pk_fields:
            field_names.append(param_marker + name_prefix + fld.name)

        for fld in entity.non_ref_fields:
            field_names.append(param_marker + name_prefix + fld.name)

        for fld in entity.ref_fields:
            if fld.ref_entity.is_sub_def:
                field_names.extend(self._join_fields(
                    fld.ref_entity, param_marker, fld.name + "_"
                ))
            else:
                for nm in fld.get_ref_names():
                    field_names.append(param_marker + name_prefix + nm)

        return field_names

    def _get_matched_fields(
        self,
        entity_fields: List[EntityField],
        field_names: List[str],
        separator: str = ", "
    ) -> str:
        matched_field_names = [
            f"{fld.name} = {self.param_marker}{fld.name}"
            for fld in entity_fields
        ]
        matched_field_names += [
            f"{name} = {self.param_marker}{name}" for name in field_names
        ]
        return separator.join(matched_field_names)

    def _get_where_clause(self) -> str:
        if not self.entity.pk_fields:
            return ""

        pk_fields = self.entity.pk_fields
        return f"WHERE {self._get_matched_fields(pk_fields, [], " AND ")}"

    def gen_get_sql_statement(self) -> str:
        select_part = (
            f"SELECT {self._get_joined_fields()} FROM {self.entity.name}"
        )
        if (where_part := self._get_where_clause()):
            return f"{select_part} {where_part};"
        else:
            return select_part + ";"

    def gen_list_sql_statement(self) -> str:
        select_part = (
            f"SELECT {self._get_joined_fields()} FROM {self.entity.name}"
        )
        where_part = self._get_list_where_clause()
        if not where_part:
            return select_part + ";"

        order_by_fields: List[str] = [
            f"{fld.name} ASC" for fld in self.entity.pk_fields
        ]
        return (
            f"{select_part} {where_part} ORDER BY "
            f"{", ".join(order_by_fields)} LIMIT @limit OFFSET @offset;"
        )

    def gen_create_sql_statement(self) -> str:
        return (
            f"INSERT INTO {self.entity.name} ({self._get_joined_fields()}) "
            f"VALUES({self._get_joined_fields(self.param_marker)});"
        )

    def gen_update_sql_statement(self) -> str:
        matched_fields = self._get_matched_fields(
            self.entity.non_ref_fields + self.entity.ref_fields, []
        )
        update_part = f"UPDATE {self.entity.name}  SET {matched_fields}"
        if (where_clause := self._get_where_clause()):
            return f"{update_part} {where_clause};"
        else:
            return update_part + ";"

    def gen_delete_sql_statement(self) -> str:
        delete_part = f"DELETE FROM {self.entity.name}"
        if (where_part := self._get_where_clause()):
            return f"{delete_part} {where_part};"
        else:
            return delete_part + ";"


class PgsqlCommandGenerator(SqlCommandGenerator):
    def _get_list_where_clause(self) -> str:
        field_names: List[str] = []
        for fld in self.entity.pk_fields:
            field_names.append(fld.name + "s")

        for fld in self.entity.ref_fields:
            if fld.ref_entity.is_enum:
                continue

            for matched_name in fld.get_ref_names():
                field_names.append(matched_name + "s")

        if not field_names:
            return ""

        matched_field_names: List[str] = []
        for name in field_names:
            matched_name = (
                f"({self.param_marker}{name} = {{}} OR "
                f"{name} = ANY({self.param_marker}{name}))"
            )
            matched_field_names.append(matched_name)

        joined_matched_fields: str = " AND ".join(matched_field_names)
        return f"WHERE {joined_matched_fields}"


class TableSqlGenerator(ABC):
    @abstractmethod
    def gen_table_sql(self) -> List[str]:
        pass


class PgsqlTableSqlGenerator(TableSqlGenerator):
    def _get_nullable_part(self, field: EntityField) -> str:
        return "NOT NULL" if field.is_required else "NULL"

    def _get_pk_field_sql(
        self, pk_fields: List[EntityField], type_mapper: TypeMapper
    ) -> Tuple[List[str], str]:
        # Handle the case where there is only one primary key field
        if len(pk_fields) == 1:
            fld = pk_fields[0]
            field_sql = (
                f"{TAB_4}{fld.name} {type_mapper.get_field_type(fld)} "
                "PRIMARY KEY,"
            )
            return [field_sql], ""

        # Handle the case where there are multiple primary key fields
        field_sql = [
            f"{TAB_4}{fld.name} {type_mapper.get_field_type(fld)},"
            for fld in pk_fields
        ]
        pk_field_names = [fld.name for fld in pk_fields]
        pk_statement = f"{TAB_4}PRIMARY KEY ({', '.join(pk_field_names)}),"
        return field_sql, pk_statement

    def _get_fk_field_sql(
        self,
        entity_fields: List[EntityField],
        parent_field_name: str,
        ref_entity_name: str,
        type_mapper: TypeMapper
    ) -> Tuple[List[str], List[str]]:
        fk_sql, fk_stmts = [], []
        for fld in entity_fields:
            fld_name = fld.get_ref_name(parent_field_name, ref_entity_name)
            fk_sql.append(
                f"{TAB_4}{fld_name} {type_mapper.get_field_type(fld)} "
                f"{self._get_nullable_part(fld)},"
            )
            fk_stmts.append(
                f"{TAB_4}FOREIGN KEY ({fld_name}) REFERENCES "
                f"{ref_entity_name} ({fld.name}),"
            )

        return fk_sql, fk_stmts

    def _get_field_sqls(
        self, entity: Entity, type_mapper: TypeMapper
    ) -> List[str]:
        # Get sql field statement for pk fields
        sql_strs, pk_statement = self._get_pk_field_sql(
            entity.pk_fields, type_mapper
        )

        # Add non ref fields
        for fld in entity.non_ref_fields:
            nullable = self._get_nullable_part(fld)
            sql_strs.append(
                f"{TAB_4}{fld.name} {type_mapper.get_field_type(fld)} "
                f"{nullable},"
            )

        # Add ref fields
        fk_stmts = []
        for fld in entity.ref_fields:
            # Handle enum type
            if fld.ref_entity.is_enum:
                sql_strs.append(
                    f"{TAB_4}{fld.name} "
                    f"{type_mapper.get_enum_field_type(fld.ref_entity)} "
                    f"{self._get_nullable_part(fld)},"
                )

            # Handle sub def entities
            elif fld.ref_entity.is_sub_def:
                sql_strs.extend(self._get_field_sqls(
                    fld.ref_entity, type_mapper
                ))

            # Handle foreign key
            else:
                fk_sqls, curr_fk_stmts = self._get_fk_field_sql(
                    fld.ref_entity.pk_fields,
                    fld.name,
                    fld.ref_entity.name,
                    type_mapper
                )
                fk_stmts.extend(curr_fk_stmts)
                sql_strs.extend(fk_sqls)

        # Add pk statement
        if pk_statement:
            sql_strs.extend(pk_statement)

        # Add foreign key statement and field sql statements
        sql_strs.extend(fk_stmts)
        return sql_strs

    def gen_table_sql(
        self, entity: Entity, type_mapper: TypeMapper
    ) -> List[str]:
        # create table statement
        sql_strs = [f"CREATE TABLE IF NOT EXISTS {entity.name} ("]

        # Add field statements
        sql_strs.extend(self._get_field_sqls(entity, type_mapper))

        # trim off last comma
        sql_strs[-1] = remove_last_comma(sql_strs[-1])

        # Close and return create table statement
        sql_strs.append(");")
        return sql_strs


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
                return PgSQLDataType.INTEGER
            elif maximum <= POS_BIGINT:
                return PgSQLDataType.BIGINT

        return PgSQLDataType.INTEGER.name

    def _get_num_type(self, format: FieldFormat) -> str:
        if format == FieldFormat.DOUBLE:
            return PgSQLDataType.DOUBLE.name
        elif format == FieldFormat.FLOAT:
            return PgSQLDataType.REAL
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
        return PgSQLDataType.TEXT

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
