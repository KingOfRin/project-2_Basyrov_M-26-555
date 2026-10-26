"""Вспомогательные функции для работы с файлами базы данных."""

import json

from primitive_db.constants import FILE_ENCODING, JSON_INDENT


def load_metadata(filepath):
    """Загружает метаданные из JSON-файла; если файла нет, возвращает {}."""
    try:
        with open(filepath, encoding=FILE_ENCODING) as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """Сохраняет метаданные в JSON-файл."""
    with open(filepath, "w", encoding=FILE_ENCODING) as file:
        json.dump(data, file, ensure_ascii=False, indent=JSON_INDENT)
