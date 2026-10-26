"""Основной цикл программы: чтение команд и вызов функций ядра."""

import prompt
from prettytable import PrettyTable

from primitive_db import core, parser
from primitive_db.constants import (
    COMMAND_PROMPT,
    ERROR_PREFIX,
    HELP_COMMON,
    HELP_DATA,
    HELP_TABLES,
    META_FILE,
    UNKNOWN_COMMAND,
)
from primitive_db.utils import (
    delete_table_data,
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


def print_help():
    """Выводит справку по доступным командам."""
    print(HELP_TABLES)
    print(HELP_DATA)
    print(HELP_COMMON)


def require_args(tokens, count):
    """Проверяет, что после имени команды ровно count аргументов."""
    if len(tokens) != count + 1:
        raise parser.invalid(tokens)


def render_table(schema, records):
    """Собирает PrettyTable из записей в порядке столбцов схемы."""
    table = PrettyTable()
    table.field_names = list(schema)
    for record in records:
        table.add_row([record.get(column) for column in schema])
    return table


def handle_create_table(tokens, metadata):
    """create_table <имя_таблицы> <столбец:тип> ..."""
    if len(tokens) < 2:
        raise parser.invalid(tokens)
    table_name = tokens[1]
    columns = parser.parse_column_definitions(tokens[2:])
    save_metadata(META_FILE, core.create_table(metadata, table_name, columns))
    save_table_data(table_name, [])


def handle_drop_table(tokens, metadata):
    """drop_table <имя_таблицы>"""
    require_args(tokens, 1)
    table_name = tokens[1]
    save_metadata(META_FILE, core.drop_table(metadata, table_name))
    delete_table_data(table_name)


def handle_insert(tokens, metadata):
    """insert into <имя_таблицы> values (...)"""
    table_name, values = parser.parse_insert(tokens)
    table_data = load_table_data(table_name)
    table_data = core.insert(metadata, table_name, values, table_data)
    save_table_data(table_name, table_data)


def handle_select(tokens, metadata):
    """select from <имя_таблицы> [where <столбец> = <значение>]"""
    table_name, where_clause = parser.parse_select(tokens)
    schema = core.get_table_schema(metadata, table_name)
    if where_clause:
        core.validate_clause(schema, where_clause)
    records = core.select(load_table_data(table_name), where_clause)
    print(render_table(schema, records))


def handle_update(tokens, metadata):
    """update <имя_таблицы> set ... where ..."""
    table_name, set_clause, where_clause = parser.parse_update(tokens)
    schema = core.get_table_schema(metadata, table_name)
    core.validate_clause(schema, set_clause)
    core.validate_clause(schema, where_clause)
    table_data = load_table_data(table_name)
    table_data = core.update(table_data, set_clause, where_clause, table_name)
    save_table_data(table_name, table_data)


def handle_delete(tokens, metadata):
    """delete from <имя_таблицы> where <столбец> = <значение>"""
    table_name, where_clause = parser.parse_delete(tokens)
    schema = core.get_table_schema(metadata, table_name)
    core.validate_clause(schema, where_clause)
    table_data = load_table_data(table_name)
    table_data = core.delete(table_data, where_clause, table_name)
    save_table_data(table_name, table_data)


def handle_info(tokens, metadata):
    """info <имя_таблицы>"""
    require_args(tokens, 1)
    table_name = tokens[1]
    core.info(metadata, table_name, load_table_data(table_name))


COMMAND_HANDLERS = {
    "create_table": handle_create_table,
    "drop_table": handle_drop_table,
    "insert": handle_insert,
    "select": handle_select,
    "update": handle_update,
    "delete": handle_delete,
    "info": handle_info,
}


def execute_command(user_input, metadata):
    """Выполняет одну команду. Возвращает False, если нужно выйти."""
    tokens = parser.tokenize(user_input)
    command = tokens[0]

    match command:
        case "exit":
            return False
        case "help":
            print_help()
        case "list_tables":
            core.list_tables(metadata)
        case _ if command in COMMAND_HANDLERS:
            COMMAND_HANDLERS[command](tokens, metadata)
        case _:
            print(UNKNOWN_COMMAND.format(command=command))
    return True


def run():
    """Запускает главный цикл базы данных."""
    print_help()
    while True:
        metadata = load_metadata(META_FILE)
        try:
            user_input = prompt.string(COMMAND_PROMPT).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user_input:
            continue

        try:
            if not execute_command(user_input, metadata):
                break
        except KeyError as error:
            print(ERROR_PREFIX + error.args[0])
        except ValueError as error:
            print(error)
