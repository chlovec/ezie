from abc import ABC, abstractmethod
from typing import List

from entity_parser.entity import Entity, EntityField


class SqlCommandGenerator(ABC):
    def __init__(self, entity: Entity, param_marker: str = "@"):
        self.entity: Entity = entity
        self.param_marker = param_marker

    @abstractmethod
    def _get_list_where_clause(self) -> str:
        pass

    def _get_joined_fields(self, param_marker: str = "") -> str:
        field_names: List[str] = []
        for fld in self.entity.pk_fields:
            field_names.append(param_marker + fld.name)

        for fld in self.entity.non_ref_fields:
            field_names.append(param_marker + fld.name)

        for fld in self.entity.ref_fields:
            for nm in fld.get_ref_names():
                field_names.append(param_marker + nm)

        return ", ".join(field_names)

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
        return (
            f"SELECT {self._get_joined_fields()} "
            f"FROM {self.entity.name} {self._get_where_clause()};"
        )

    def gen_list_sql_statement(self) -> str:
        matched_fields: List[str] = [
            f"{fld.name} ASC" for fld in self.entity.pk_fields
        ]
        joined_matched_fields: str = ", ".join(matched_fields)
        order_by_clause: str = (
            f"ORDER BY {joined_matched_fields} LIMIT @limit OFFSET @offset"
        )
        return (
            f"SELECT {self._get_joined_fields()} FROM {self.entity.name} "
            f"{self._get_list_where_clause()} {order_by_clause};"
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
        return (
            f"UPDATE {self.entity.name}  SET {matched_fields} "
            f"{self._get_where_clause()};"
        )

    def gen_delete_sql_statement(self) -> str:
        return f"DELETE FROM {self.entity.name} {self._get_where_clause()};"


class PgsqlCommandGenerator(SqlCommandGenerator):
    def _get_list_where_clause(self) -> str:
        field_names: List[str] = []
        for fld in self.entity.pk_fields:
            field_names.append(fld.name + "s")

        for fld in self.entity.ref_fields:
            for matched_name in fld.get_ref_names():
                field_names.append(matched_name + "s")

        matched_field_names: List[str] = []
        for name in field_names:
            matched_name = (
                f"({self.param_marker}{name} = {{}} OR "
                f"{name} = ANY({self.param_marker}{name}))"
            )
            matched_field_names.append(matched_name)

        joined_matched_fields: str = " AND ".join(matched_field_names)
        return f"WHERE {joined_matched_fields}"
