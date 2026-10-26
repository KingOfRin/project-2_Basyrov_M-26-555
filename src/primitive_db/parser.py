"""Функции разбора пользовательского ввода."""

import shlex

from primitive_db.constants import COLUMN_TYPE_SEPARATOR, INVALID_VALUE


def tokenize(user_input):
    """Разбивает строку команды на токены с учётом кавычек."""
    try:
        return shlex.split(user_input)
    except ValueError:
        raise ValueError(INVALID_VALUE.format(value=user_input)) from None


def parse_column_definitions(definitions):
    """Превращает ["name:str", ...] в список пар [("name", "str"), ...]."""
    columns = []
    for definition in definitions:
        name, separator, column_type = definition.partition(COLUMN_TYPE_SEPARATOR)
        if not name or not separator or not column_type:
            raise ValueError(INVALID_VALUE.format(value=definition))
        columns.append((name, column_type))
    return columns
