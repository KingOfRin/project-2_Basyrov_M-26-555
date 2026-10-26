"""Бизнес-логика базы данных: управление таблицами и CRUD-операции."""

import json

from primitive_db.constants import (
    ACTION_DELETE_RECORDS,
    ACTION_DROP_TABLE,
    COLUMN_NOT_FOUND,
    ID_COLUMN,
    ID_NOT_EDITABLE,
    ID_TYPE,
    INVALID_VALUE,
    INVALID_VALUES_COUNT,
    NO_MATCHING_RECORDS,
    NO_TABLES,
    PYTHON_TYPES,
    RECORD_DELETED,
    RECORD_INSERTED,
    RECORD_UPDATED,
    TABLE_CREATED,
    TABLE_DROPPED,
    TABLE_EXISTS,
    TABLE_INFO,
    TABLE_LIST_ITEM,
    TABLE_NOT_FOUND,
    VALID_TYPES,
)
from primitive_db.decorators import (
    confirm_action,
    create_cacher,
    handle_db_errors,
    log_time,
)

select_cache = create_cacher()


def format_schema(schema):
    """Возвращает схему таблицы в виде строки "ID:int, name:str, ..."."""
    return ", ".join(f"{name}:{column_type}" for name, column_type in schema.items())


def get_table_schema(metadata, table_name):
    """Возвращает схему таблицы; если таблицы нет, выбрасывает KeyError."""
    if table_name not in metadata:
        raise KeyError(TABLE_NOT_FOUND.format(table=table_name))
    return metadata[table_name]


def validate_value(column_type, value):
    """Проверяет, что значение соответствует типу столбца."""
    if type(value) is not PYTHON_TYPES[column_type]:
        raise ValueError(INVALID_VALUE.format(value=value))


def validate_clause(schema, clause):
    """Проверяет, что столбцы условия есть в схеме, а значения подходят по типу."""
    for column, value in clause.items():
        if column not in schema:
            raise KeyError(COLUMN_NOT_FOUND.format(column=column))
        validate_value(schema[column], value)


def matches(record, where_clause):
    """Проверяет, что запись удовлетворяет всем условиям where_clause."""
    return all(record.get(column) == value for column, value in where_clause.items())


@handle_db_errors
def create_table(metadata, table_name, columns):
    """Добавляет в метаданные таблицу со столбцом ID и столбцами columns.

    columns — список пар (имя_столбца, тип). Возвращает обновлённые метаданные.
    """
    if not table_name.isidentifier():
        raise ValueError(INVALID_VALUE.format(value=table_name))
    if table_name in metadata:
        raise ValueError(TABLE_EXISTS.format(table=table_name))

    schema = {ID_COLUMN: ID_TYPE}
    for name, column_type in columns:
        if (
            not name.isidentifier()
            or column_type not in VALID_TYPES
            or name in schema
        ):
            raise ValueError(INVALID_VALUE.format(value=f"{name}:{column_type}"))
        schema[name] = column_type

    metadata[table_name] = schema
    print(TABLE_CREATED.format(table=table_name, columns=format_schema(schema)))
    return metadata


@handle_db_errors
@confirm_action(ACTION_DROP_TABLE)
def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных и возвращает обновлённые метаданные."""
    get_table_schema(metadata, table_name)
    del metadata[table_name]
    print(TABLE_DROPPED.format(table=table_name))
    return metadata


def list_tables(metadata):
    """Выводит список всех таблиц."""
    if not metadata:
        print(NO_TABLES)
        return
    for table_name in metadata:
        print(TABLE_LIST_ITEM.format(table=table_name))


@handle_db_errors
@log_time
def insert(metadata, table_name, values, table_data):
    """Добавляет запись в таблицу и возвращает обновлённые данные таблицы.

    values — значения всех столбцов, кроме ID; ID генерируется автоматически.
    """
    schema = get_table_schema(metadata, table_name)
    data_columns = [column for column in schema if column != ID_COLUMN]
    if len(values) != len(data_columns):
        raise ValueError(
            INVALID_VALUES_COUNT.format(expected=len(data_columns), actual=len(values))
        )
    for column, value in zip(data_columns, values):
        validate_value(schema[column], value)

    new_id = max((record[ID_COLUMN] for record in table_data), default=0) + 1
    record = {ID_COLUMN: new_id, **dict(zip(data_columns, values))}
    print(RECORD_INSERTED.format(record_id=new_id, table=table_name))
    return [*table_data, record]


@handle_db_errors
@log_time
def select(table_data, where_clause=None):
    """Возвращает все записи или только те, что удовлетворяют where_clause.

    Результат кэшируется по содержимому таблицы и условию, поэтому повторный
    одинаковый запрос к неизменённым данным не фильтрует записи заново.
    """
    where_clause = where_clause or {}
    cache_key = json.dumps([table_data, where_clause], sort_keys=True)
    return select_cache(
        cache_key,
        lambda: [record for record in table_data if matches(record, where_clause)],
    )


@handle_db_errors
def update(table_data, set_clause, where_clause, table_name):
    """Обновляет поля set_clause у записей, подходящих под where_clause."""
    if ID_COLUMN in set_clause:
        raise ValueError(ID_NOT_EDITABLE)

    updated_ids = []
    for record in table_data:
        if matches(record, where_clause):
            record.update(set_clause)
            updated_ids.append(record[ID_COLUMN])

    if not updated_ids:
        print(NO_MATCHING_RECORDS)
    for record_id in updated_ids:
        print(RECORD_UPDATED.format(record_id=record_id, table=table_name))
    return table_data


@handle_db_errors
@confirm_action(ACTION_DELETE_RECORDS)
def delete(table_data, where_clause, table_name):
    """Удаляет записи, подходящие под where_clause, и возвращает остальные."""
    remaining = [record for record in table_data if not matches(record, where_clause)]
    deleted_ids = [
        record[ID_COLUMN] for record in table_data if matches(record, where_clause)
    ]

    if not deleted_ids:
        print(NO_MATCHING_RECORDS)
    for record_id in deleted_ids:
        print(RECORD_DELETED.format(record_id=record_id, table=table_name))
    return remaining


@handle_db_errors
def info(metadata, table_name, table_data):
    """Выводит схему таблицы и количество записей в ней."""
    schema = get_table_schema(metadata, table_name)
    print(
        TABLE_INFO.format(
            table=table_name, columns=format_schema(schema), count=len(table_data)
        )
    )
