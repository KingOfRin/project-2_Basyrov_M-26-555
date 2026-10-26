# Primitive DB

Консольное приложение, имитирующее работу с простой базой данных.
Метаданные таблиц хранятся в файле `db_meta.json`.

## Установка

```bash
make install        # или: uv sync
```

Установка как самостоятельной утилиты:

```bash
make build
make package-install
```

## Запуск

```bash
make run            # или: uv run database
```

После установки пакета база данных запускается командой `database`.

## Проверка кода

```bash
make lint           # или: uv run ruff check .
```

## Управление таблицами

| Команда | Описание |
|---|---|
| `create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ...` | создать таблицу |
| `list_tables` | показать список всех таблиц |
| `drop_table <имя_таблицы>` | удалить таблицу |
| `help` | справочная информация |
| `exit` | выход из программы |

Поддерживаемые типы данных: `int`, `str`, `bool`.
Столбец `ID:int` добавляется в каждую таблицу автоматически.

Пример:

```text
>>>Введите команду: create_table users name:str age:int is_active:bool
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool
>>>Введите команду: create_table users name:str
Ошибка: Таблица "users" уже существует.
>>>Введите команду: list_tables
- users
>>>Введите команду: drop_table users
Таблица "users" успешно удалена.
>>>Введите команду: drop_table products
Ошибка: Таблица "products" не существует.
```
