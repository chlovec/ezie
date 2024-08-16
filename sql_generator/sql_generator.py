from abc import ABC, abstractmethod
from typing import List, Tuple

from entity_parser.entity import FieldData
from utils.constants import TAB_4
from utils.utils import EntityFieldData, remove_last_comma


END_TOKEN: str = ";"
FROM: str = "FROM"
PRIMARY_KEY: str = "PRIMARY KEY"
SELECT: str = "SELECT"
WHERE: str = "WHERE"


class SqlCommandGenerator(ABC):
    def __init__(
        self,
        entity: EntityFieldData,
        param_marker: str = "@"
    ):
        self.param_marker: str = param_marker
        self.entity_field_data: EntityFieldData = entity

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
            f"{fld.name} ASC" for fld in self.entity_field_data.pk_field_data
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
    def gen_table_sql(self, entity: EntityFieldData) -> List[str]:
        pass


class PgsqlTableSqlGenerator(TableSqlGenerator):
    def _get_nullable_part(self, field: FieldData) -> str:
        return "NOT NULL" if field.is_required else "NULL"

    def _get_pk_field_sql(
        self, pk_fields: List[FieldData]
    ) -> Tuple[List[str], str]:
        # Handle the case where there is only one primary key field
        if not pk_fields:
            return [], ""

        # Handle the case where there is only one primary key field
        elif len(pk_fields) == 1:
            fld = pk_fields[0]
            field_sql = f"{TAB_4}{fld.name} {fld.data_type} {PRIMARY_KEY},"
            return [field_sql], ""

        # Handle the case where there are multiple primary key fields
        field_sql = [
            f"{TAB_4}{fld.name} {fld.data_type},"
            for fld in pk_fields
        ]
        pk_field_names = [fld.name for fld in pk_fields]
        pk_statement = f"{TAB_4}{PRIMARY_KEY} ({", ".join(pk_field_names)}),"
        return field_sql, pk_statement

    def _get_fk_field_sql(
        self, fk_fields: List[FieldData]
    ) -> Tuple[List[str], List[str]]:
        fk_sql, fk_stmts = [], []
        for fld in fk_fields:
            fk_sql.append(
                f"{TAB_4}{fld.name} {fld.data_type} "
                f"{self._get_nullable_part(fld)},"
            )
            fk_stmts.append(
                f"{TAB_4}FOREIGN KEY ({fld.name}) REFERENCES "
                f"{fld.ref_entity_name} ({fld.ref_field_name}),"
            )

        return fk_sql, fk_stmts

    def _get_field_sqls(
        self, entity: EntityFieldData
    ) -> List[str]:
        # Get sql field statement for primary key fields
        sql_strs, pk_statement = self._get_pk_field_sql(entity.pk_field_data)

        # Add non ref fields
        sql_strs.extend([
            (
                f"{TAB_4}{fld.name} "
                f"{fld.data_type} {self._get_nullable_part(fld)},"
            )
            for fld in entity.other_field_data
        ])

        # Add foreign key fields
        fk_sqls, fk_stmts = self._get_fk_field_sql(entity.fk_field_data)
        sql_strs.extend(fk_sqls)

        # Add primary key statement
        if pk_statement:
            sql_strs.append(pk_statement)

        # Add foreign key statement and field sql statements
        sql_strs.extend(fk_stmts)
        return sql_strs

    def gen_table_sql(
        self, entity: EntityFieldData
    ) -> List[str]:
        # create table statement
        sql_strs = [f"CREATE TABLE IF NOT EXISTS {entity.entity_name} ("]

        # Add field statements
        sql_strs.extend(self._get_field_sqls(entity))

        # trim off last comma
        sql_strs[-1] = remove_last_comma(sql_strs[-1])

        # Close and return create table statement
        sql_strs.append(");")
        return sql_strs
