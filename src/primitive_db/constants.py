"""Константы приложения: пути к файлам, типы данных и тексты сообщений."""

META_FILE = "db_meta.json"
FILE_ENCODING = "utf-8"
JSON_INDENT = 4

ID_COLUMN = "ID"
ID_TYPE = "int"
VALID_TYPES = ("int", "str", "bool")
COLUMN_TYPE_SEPARATOR = ":"

COMMAND_PROMPT = ">>>Введите команду: "

HELP_TABLES = """
***Процесс работы с таблицей***
Функции:
<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу
<command> list_tables - показать список всех таблиц
<command> drop_table <имя_таблицы> - удалить таблицу"""

HELP_COMMON = """
Общие команды:
<command> exit - выход из программы
<command> help - справочная информация
"""

ERROR_PREFIX = "Ошибка: "
TABLE_CREATED = 'Таблица "{table}" успешно создана со столбцами: {columns}'
TABLE_DROPPED = 'Таблица "{table}" успешно удалена.'
TABLE_EXISTS = ERROR_PREFIX + 'Таблица "{table}" уже существует.'
TABLE_NOT_FOUND = 'Таблица "{table}" не существует.'
TABLE_LIST_ITEM = "- {table}"
NO_TABLES = "Таблиц пока нет."
UNKNOWN_COMMAND = "Функции {command} нет. Попробуйте снова."
INVALID_VALUE = "Некорректное значение: {value}. Попробуйте снова."
