"""Вспомогательные функции для работы с файлами базы данных."""

import json
import os

from primitive_db.constants import (
    DATA_DIR,
    DATA_FILE_EXTENSION,
    FILE_ENCODING,
    JSON_INDENT,
)


def read_json(filepath, default):
    """Читает JSON-файл; если файла нет, возвращает default."""
    try:
        with open(filepath, encoding=FILE_ENCODING) as file:
            return json.load(file)
    except FileNotFoundError:
        return default


def write_json(filepath, data):
    """Записывает данные в JSON-файл, создавая недостающие директории."""
    directory = os.path.dirname(filepath)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(filepath, "w", encoding=FILE_ENCODING) as file:
        json.dump(data, file, ensure_ascii=False, indent=JSON_INDENT)


def load_metadata(filepath):
    """Загружает метаданные из JSON-файла; если файла нет, возвращает {}."""
    return read_json(filepath, {})


def save_metadata(filepath, data):
    """Сохраняет метаданные в JSON-файл."""
    write_json(filepath, data)


def get_table_path(table_name):
    """Возвращает путь к файлу с данными таблицы, например data/users.json."""
    return os.path.join(DATA_DIR, table_name + DATA_FILE_EXTENSION)


def load_table_data(table_name):
    """Загружает записи таблицы; если файла нет, возвращает []."""
    return read_json(get_table_path(table_name), [])


def save_table_data(table_name, data):
    """Сохраняет записи таблицы в её JSON-файл."""
    write_json(get_table_path(table_name), data)


def delete_table_data(table_name):
    """Удаляет файл с данными таблицы, если он существует."""
    try:
        os.remove(get_table_path(table_name))
    except FileNotFoundError:
        pass
