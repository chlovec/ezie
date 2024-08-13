from abc import ABC, abstractmethod
from typing import List, Tuple

from data_type_mapper.data_type_mapper import (
    NEG_BIGINT, NEG_INTEGER, NEG_SMALLINT, POS_BIGINT, POS_INTEGER,
    POS_SMALLINT, FieldFormat
)
from data_type_mapper.sql_type_mapper import PgSQLDataType
from entity_parser.entity import Entity, EntityField, FieldData, FieldType
from utils.constants import TAB_4
from utils.utils import TypeMapper, EntityFieldData, remove_last_comma


SELECT: str = "SELECT"
END_TOKEN: str = ";"
FROM: str = "FROM"
WHERE: str = "WHERE"


class SqlCommandGenerator(ABC):
    def __init__(
        self,
        entity: Entity,
        type_mapper: TypeMapper = None,
        param_marker: str = "@"
    ):
        self.entity: Entity = entity
        self.param_marker: str = param_marker
        self.entity_field_data: EntityFieldData = EntityFieldData.from_entity(
            entity=entity, type_mapper=type_mapper
        )

    @abstractmethod
    def _get_list_where_clause(self) -> str:
        pass

    def _get_joined_fields(self, param_marker: str = "") -> str:
        field_names = [
            f"{param_marker}{fld.name}"
            for fld in self.entity_field_data.get_field_data()
        ]
        return ", ".join(field_names)

    def _get_matched_fields(
        self, field_data: List[FieldData], separator: str = ", "
    ) -> str:
        if not field_data:
            return ""

        matched_fields = (
            f"{fld.name} = {self.param_marker}{fld.name}"
            for fld in field_data
        )
        return separator.join(matched_fields)

    def _get_where_clause(self) -> str:
        if not self.entity_field_data.pk_field_data:
            return ""

        pk_fields = self.entity_field_data.pk_field_data
        return f"{WHERE} {self._get_matched_fields(pk_fields, " AND ")}"

    def gen_get_sql_statement(self) -> str:
        select_part = (
            f"{SELECT} {self._get_joined_fields()} {FROM} "
            f"{self.entity_field_data.entity_name}"
        )
        if (where_part := self._get_where_clause()):
            return f"{select_part} {where_part}{END_TOKEN}"
        else:
            return select_part + END_TOKEN

    def gen_list_sql_statement(self) -> str:
        select_part = (
            f"{SELECT} {self._get_joined_fields()} {FROM} "
            f"{self.entity_field_data.entity_name}"
        )
        where_part = self._get_list_where_clause()
        if not where_part:
            return select_part + END_TOKEN

        order_by_fields: List[str] = [
            f"{fld.name} ASC" for fld in self.entity.pk_fields
        ]
        return (
            f"{select_part} {where_part} ORDER BY {", ".join(order_by_fields)}"
            f" LIMIT @limit OFFSET @offset{END_TOKEN}"
        )

    def gen_create_sql_statement(self) -> str:
        return (
            f"INSERT INTO {self.entity_field_data.entity_name} "
            f"({self._get_joined_fields()}) "
            f"VALUES({self._get_joined_fields(self.param_marker)}){END_TOKEN}"
        )

    def gen_update_sql_statement(self) -> str:
        matched_fields = self._get_matched_fields(
            self.entity_field_data.get_non_pk_field_data()
        )
        update_part = (
            f"UPDATE {self.entity_field_data.entity_name}  "
            f"SET {matched_fields}"
        )
        if (where_clause := self._get_where_clause()):
            return f"{update_part} {where_clause}{END_TOKEN}"
        else:
            return update_part + END_TOKEN

    def gen_delete_sql_statement(self) -> str:
        delete_part = f"DELETE {FROM} {self.entity_field_data.entity_name}"

        if (where_part := self._get_where_clause()):
            return f"{delete_part} {where_part}{END_TOKEN}"
        else:
            return delete_part + END_TOKEN


class PgsqlCommandGenerator(SqlCommandGenerator):
    def _get_list_where_clause(self) -> str:
        matched_field_names: List[str] = [
            (
                f"({self.param_marker}{fld.name}s = {{}} OR "
                f"{fld.name}s = ANY({self.param_marker}{fld.name}s))"
            )
            for fld in self.entity_field_data.get_pk_and_fk_field_data()
        ]

        if not matched_field_names:
            return ""

        joined_matched_fields: str = " AND ".join(matched_field_names)
        return f"{WHERE} {joined_matched_fields}"


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
        if not pk_fields:
            return [], ""

        # Handle the case where there is only one primary key field
        elif len(pk_fields) == 1:
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
        self, entity: Entity, type_mapper: TypeMapper,
        parent_field_name: str = ""
    ) -> List[str]:
        # Get sql field statement for pk fields
        sql_strs, pk_statement = self._get_pk_field_sql(
            entity.pk_fields, type_mapper
        )

        # Add non ref fields
        for fld in entity.non_ref_fields:
            prefix_name = ""
            if (
                parent_field_name and
                not fld.name.startswith(parent_field_name)
            ):
                prefix_name = f"{parent_field_name}_"

            nullable = self._get_nullable_part(fld)
            sql_strs.append(
                f"{TAB_4}{prefix_name}{fld.name} "
                f"{type_mapper.get_field_type(fld)} {nullable},"
            )

        # Add ref fields
        fk_stmts = []
        for fld in entity.ref_fields:
            prefix_name = ""
            if (
                parent_field_name and
                not fld.name.startswith(parent_field_name)
            ):
                prefix_name = f"{parent_field_name}_"

            # Handle enum type
            if fld.ref_entity.is_enum:
                sql_strs.append(
                    f"{TAB_4}{prefix_name}{fld.name} "
                    f"{type_mapper.get_enum_field_type(fld.ref_entity)} "
                    f"{self._get_nullable_part(fld)},"
                )

            # Handle sub def entities
            elif fld.ref_entity.is_sub_def:
                sql_strs.extend(self._get_field_sqls(
                    fld.ref_entity, type_mapper, fld.name
                ))

            # Handle foreign key
            else:
                fk_sqls, curr_fk_stmts = self._get_fk_field_sql(
                    fld.ref_entity.pk_fields,
                    fld.name,
                    fld.ref_entity.name,
                    type_mapper,
                )
                fk_stmts.extend(curr_fk_stmts)
                sql_strs.extend(fk_sqls)

        # Add pk statement
        if pk_statement:
            sql_strs.append(pk_statement)

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
