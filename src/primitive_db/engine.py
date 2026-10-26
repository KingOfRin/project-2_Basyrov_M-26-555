"""Основной цикл программы: чтение команд и вызов функций ядра."""

import prompt

from primitive_db import core
from primitive_db.constants import (
    COMMAND_PROMPT,
    ERROR_PREFIX,
    HELP_COMMON,
    HELP_TABLES,
    INVALID_VALUE,
    META_FILE,
    UNKNOWN_COMMAND,
)
from primitive_db.parser import parse_column_definitions, tokenize
from primitive_db.utils import load_metadata, save_metadata


def print_help():
    """Выводит справку по доступным командам."""
    print(HELP_TABLES)
    print(HELP_COMMON)


def require_args(args, count, user_input):
    """Проверяет, что у команды ровно count аргументов."""
    if len(args) != count:
        raise ValueError(INVALID_VALUE.format(value=user_input))


def execute_command(user_input, metadata):
    """Выполняет одну команду. Возвращает False, если нужно выйти."""
    command, *args = tokenize(user_input)

    match command:
        case "exit":
            return False
        case "help":
            print_help()
        case "list_tables":
            core.list_tables(metadata)
        case "create_table":
            if not args:
                raise ValueError(INVALID_VALUE.format(value=user_input))
            table_name, *definitions = args
            columns = parse_column_definitions(definitions)
            save_metadata(META_FILE, core.create_table(metadata, table_name, columns))
        case "drop_table":
            require_args(args, 1, user_input)
            save_metadata(META_FILE, core.drop_table(metadata, args[0]))
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
