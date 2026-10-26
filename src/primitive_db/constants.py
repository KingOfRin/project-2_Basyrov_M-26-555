"""Константы приложения: пути к файлам, типы данных и тексты сообщений."""

META_FILE = "db_meta.json"
DATA_DIR = "data"
DATA_FILE_EXTENSION = ".json"
FILE_ENCODING = "utf-8"
JSON_INDENT = 4

ID_COLUMN = "ID"
ID_TYPE = "int"
PYTHON_TYPES = {"int": int, "str": str, "bool": bool}
VALID_TYPES = tuple(PYTHON_TYPES)
COLUMN_TYPE_SEPARATOR = ":"

COMMAND_PUNCTUATION = "(),="
QUOTE_CHARS = "\"'"
BOOL_LITERALS = {"true": True, "false": False}
KEYWORD_INTO = "into"
KEYWORD_VALUES = "values"
KEYWORD_FROM = "from"
KEYWORD_WHERE = "where"
KEYWORD_SET = "set"
OPEN_BRACKET = "("
CLOSE_BRACKET = ")"
VALUES_SEPARATOR = ","
ASSIGNMENT = "="

COMMAND_PROMPT = ">>>Введите команду: "

HELP_TABLES = "\n".join(
    (
        "",
        "***Процесс работы с таблицей***",
        "Функции:",
        "<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. "
        "- создать таблицу",
        "<command> list_tables - показать список всех таблиц",
        "<command> drop_table <имя_таблицы> - удалить таблицу",
    )
)

HELP_DATA = "\n".join(
    (
        "",
        "***Операции с данными***",
        "Функции:",
        "<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) "
        "- создать запись.",
        "<command> select from <имя_таблицы> where <столбец> = <значение> "
        "- прочитать записи по условию.",
        "<command> select from <имя_таблицы> - прочитать все записи.",
        "<command> update <имя_таблицы> set <столбец1> = <новое_значение1> "
        "where <столбец_условия> = <значение_условия> - обновить запись.",
        "<command> delete from <имя_таблицы> where <столбец> = <значение> "
        "- удалить запись.",
        "<command> info <имя_таблицы> - вывести информацию о таблице.",
    )
)

HELP_COMMON = "\n".join(
    (
        "",
        "Общие команды:",
        "<command> exit - выход из программы",
        "<command> help - справочная информация",
        "",
    )
)

ERROR_PREFIX = "Ошибка: "
TABLE_CREATED = 'Таблица "{table}" успешно создана со столбцами: {columns}'
TABLE_DROPPED = 'Таблица "{table}" успешно удалена.'
TABLE_EXISTS = ERROR_PREFIX + 'Таблица "{table}" уже существует.'
TABLE_NOT_FOUND = 'Таблица "{table}" не существует.'
COLUMN_NOT_FOUND = 'Столбец "{column}" не существует.'
TABLE_LIST_ITEM = "- {table}"
NO_TABLES = "Таблиц пока нет."
UNKNOWN_COMMAND = "Функции {command} нет. Попробуйте снова."
INVALID_VALUE = "Некорректное значение: {value}. Попробуйте снова."
INVALID_VALUES_COUNT = (
    "Некорректное количество значений: ожидалось {expected}, "
    "получено {actual}. Попробуйте снова."
)
ID_NOT_EDITABLE = ERROR_PREFIX + "Столбец ID нельзя изменять."

RECORD_INSERTED = 'Запись с ID={record_id} успешно добавлена в таблицу "{table}".'
RECORD_UPDATED = 'Запись с ID={record_id} в таблице "{table}" успешно обновлена.'
RECORD_DELETED = 'Запись с ID={record_id} успешно удалена из таблицы "{table}".'
NO_MATCHING_RECORDS = "Записи, удовлетворяющие условию, не найдены."

TABLE_INFO = "Таблица: {table}\nСтолбцы: {columns}\nКоличество записей: {count}"

EXIT_COMMAND = "exit"

ACTION_DROP_TABLE = "удаление таблицы"
ACTION_DELETE_RECORDS = "удаление записи"
CONFIRM_PROMPT = 'Вы уверены, что хотите выполнить "{action}"? [y/n]: '
CONFIRM_YES = "y"
ACTION_CANCELLED = "Операция отменена."

LOG_TIME_MESSAGE = "Функция {name} выполнилась за {seconds:.3f} секунд."
DATA_FILE_NOT_FOUND = (
    ERROR_PREFIX + "Файл данных не найден. Возможно, база данных не инициализирована."
)
UNEXPECTED_ERROR = "Произошла непредвиденная ошибка: {error}"
