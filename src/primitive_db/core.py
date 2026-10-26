"""Бизнес-логика базы данных: управление таблицами."""

from primitive_db.constants import (
    ID_COLUMN,
    ID_TYPE,
    INVALID_VALUE,
    NO_TABLES,
    TABLE_CREATED,
    TABLE_DROPPED,
    TABLE_EXISTS,
    TABLE_LIST_ITEM,
    TABLE_NOT_FOUND,
    VALID_TYPES,
)


def format_schema(schema):
    """Возвращает схему таблицы в виде строки "ID:int, name:str, ..."."""
    return ", ".join(f"{name}:{column_type}" for name, column_type in schema.items())


def get_table_schema(metadata, table_name):
    """Возвращает схему таблицы; если таблицы нет, выбрасывает KeyError."""
    if table_name not in metadata:
        raise KeyError(TABLE_NOT_FOUND.format(table=table_name))
    return metadata[table_name]


def create_table(metadata, table_name, columns):
    """Добавляет в метаданные таблицу со столбцом ID и столбцами columns.

    columns — список пар (имя_столбца, тип). Возвращает обновлённые метаданные.
    """
    if table_name in metadata:
        raise ValueError(TABLE_EXISTS.format(table=table_name))

    schema = {ID_COLUMN: ID_TYPE}
    for name, column_type in columns:
        if column_type not in VALID_TYPES or name in schema:
            raise ValueError(INVALID_VALUE.format(value=f"{name}:{column_type}"))
        schema[name] = column_type

    metadata[table_name] = schema
    print(TABLE_CREATED.format(table=table_name, columns=format_schema(schema)))
    return metadata


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
