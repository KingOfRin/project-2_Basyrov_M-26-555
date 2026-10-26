"""Функции разбора пользовательского ввода: values, where, set и команд CRUD."""

import shlex

from primitive_db.constants import (
    ASSIGNMENT,
    BOOL_LITERALS,
    CLOSE_BRACKET,
    COLUMN_TYPE_SEPARATOR,
    COMMAND_PUNCTUATION,
    INVALID_VALUE,
    KEYWORD_FROM,
    KEYWORD_INTO,
    KEYWORD_SET,
    KEYWORD_VALUES,
    KEYWORD_WHERE,
    OPEN_BRACKET,
    QUOTE_CHARS,
    VALUES_SEPARATOR,
)


def invalid(tokens):
    """Создаёт ValueError с сообщением о некорректном значении."""
    return ValueError(INVALID_VALUE.format(value=" ".join(tokens)))


def tokenize(user_input):
    """Разбивает строку команды на токены.

    Строки в кавычках остаются одним токеном вместе с кавычками,
    а символы "(", ")", "," и "=" выделяются в отдельные токены.
    """
    lexer = shlex.shlex(user_input, posix=False, punctuation_chars=COMMAND_PUNCTUATION)
    lexer.whitespace_split = True
    try:
        raw_tokens = list(lexer)
    except ValueError:
        raise invalid([user_input]) from None

    tokens = []
    for token in raw_tokens:
        if set(token) <= set(COMMAND_PUNCTUATION):
            tokens.extend(token)
        else:
            tokens.append(token)
    return tokens


def parse_column_definitions(definitions):
    """Превращает ["name:str", ...] в список пар [("name", "str"), ...]."""
    columns = []
    for definition in definitions:
        name, separator, column_type = definition.partition(COLUMN_TYPE_SEPARATOR)
        if not name or not separator or not column_type:
            raise invalid([definition])
        columns.append((name, column_type))
    return columns


def parse_value(token):
    """Превращает токен в значение: '"Sergei"' -> 'Sergei', '28' -> 28,
    'true' -> True. Слово без кавычек считается строкой.
    """
    if token in COMMAND_PUNCTUATION:
        raise invalid([token])
    if len(token) >= 2 and token[0] == token[-1] and token[0] in QUOTE_CHARS:
        return token[1:-1]
    if token.lower() in BOOL_LITERALS:
        return BOOL_LITERALS[token.lower()]
    try:
        return int(token)
    except ValueError:
        return token


def split_tokens(tokens, separator):
    """Делит список токенов на группы по разделителю."""
    groups = [[]]
    for token in tokens:
        if token == separator:
            groups.append([])
        else:
            groups[-1].append(token)
    return groups


def parse_condition(tokens):
    """Превращает ["age", "=", "28"] в словарь {"age": 28}."""
    if len(tokens) != 3 or tokens[1] != ASSIGNMENT:
        raise invalid(tokens)
    column, _, value = tokens
    return {column: parse_value(value)}


def parse_where(tokens):
    """Разбирает условие where: "age = 28" -> {"age": 28}."""
    return parse_condition(tokens)


def parse_set(tokens):
    """Разбирает set: "age = 29, name = 'Ann'" -> {"age": 29, "name": "Ann"}."""
    set_clause = {}
    for group in split_tokens(tokens, VALUES_SEPARATOR):
        set_clause.update(parse_condition(group))
    return set_clause


def parse_values(tokens):
    """Разбирает список значений: '("Sergei", 28, true)' -> ["Sergei", 28, True]."""
    if len(tokens) < 2 or tokens[0] != OPEN_BRACKET or tokens[-1] != CLOSE_BRACKET:
        raise invalid(tokens)
    inner = tokens[1:-1]
    if not inner:
        return []
    values = []
    for group in split_tokens(inner, VALUES_SEPARATOR):
        if len(group) != 1:
            raise invalid(tokens)
        values.append(parse_value(group[0]))
    return values


def is_keyword(token, keyword):
    """Проверяет, что токен совпадает с ключевым словом без учёта регистра."""
    return token.lower() == keyword


def find_keyword(tokens, keyword):
    """Возвращает индекс ключевого слова в списке токенов или -1."""
    for index, token in enumerate(tokens):
        if is_keyword(token, keyword):
            return index
    return -1


def parse_insert(tokens):
    """insert into <таблица> values (...) -> (таблица, [значения])."""
    if (
        len(tokens) < 5
        or not is_keyword(tokens[1], KEYWORD_INTO)
        or not is_keyword(tokens[3], KEYWORD_VALUES)
    ):
        raise invalid(tokens)
    return tokens[2], parse_values(tokens[4:])


def parse_select(tokens):
    """select from <таблица> [where ...] -> (таблица, where или None)."""
    if len(tokens) < 3 or not is_keyword(tokens[1], KEYWORD_FROM):
        raise invalid(tokens)
    table_name, rest = tokens[2], tokens[3:]
    if not rest:
        return table_name, None
    if not is_keyword(rest[0], KEYWORD_WHERE):
        raise invalid(tokens)
    return table_name, parse_where(rest[1:])


def parse_update(tokens):
    """update <таблица> set ... where ... -> (таблица, set, where)."""
    where_index = find_keyword(tokens, KEYWORD_WHERE)
    if (
        len(tokens) < 3
        or not is_keyword(tokens[2], KEYWORD_SET)
        or where_index == -1
    ):
        raise invalid(tokens)
    set_clause = parse_set(tokens[3:where_index])
    where_clause = parse_where(tokens[where_index + 1 :])
    return tokens[1], set_clause, where_clause


def parse_delete(tokens):
    """delete from <таблица> where ... -> (таблица, where)."""
    if (
        len(tokens) < 4
        or not is_keyword(tokens[1], KEYWORD_FROM)
        or not is_keyword(tokens[3], KEYWORD_WHERE)
    ):
        raise invalid(tokens)
    return tokens[2], parse_where(tokens[4:])
