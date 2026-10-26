"""Декораторы (обработка ошибок, подтверждение, замер времени) и кэширование."""

import time

import prompt

from primitive_db.constants import (
    ACTION_CANCELLED,
    CONFIRM_PROMPT,
    CONFIRM_YES,
    DATA_FILE_NOT_FOUND,
    ERROR_PREFIX,
    LOG_TIME_MESSAGE,
    UNEXPECTED_ERROR,
)


def copy_metadata(wrapper, func):
    """Переносит имя и docstring исходной функции на обёртку."""
    wrapper.__name__ = func.__name__
    wrapper.__qualname__ = func.__qualname__
    wrapper.__doc__ = func.__doc__
    return wrapper


def handle_db_errors(func):
    """Перехватывает ошибки базы данных, печатает сообщение и возвращает None."""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(DATA_FILE_NOT_FOUND)
        except KeyError as error:
            print(ERROR_PREFIX + str(error.args[0] if error.args else error))
        except ValueError as error:
            print(error)
        except Exception as error:
            print(UNEXPECTED_ERROR.format(error=error))
        return None

    return copy_metadata(wrapper, func)


def confirm_action(action_name):
    """Запрашивает подтверждение [y/n] перед выполнением опасной операции.

    Если пользователь ответил не "y", операция отменяется и возвращается None.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                answer = prompt.string(CONFIRM_PROMPT.format(action=action_name))
            except EOFError:
                answer = ""
            if answer.strip().lower() != CONFIRM_YES:
                print(ACTION_CANCELLED)
                return None
            return func(*args, **kwargs)

        return copy_metadata(wrapper, func)

    return decorator


def log_time(func):
    """Выводит время выполнения функции, измеренное через time.monotonic()."""

    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        elapsed = time.monotonic() - start
        print(LOG_TIME_MESSAGE.format(name=func.__name__, seconds=elapsed))
        return result

    return copy_metadata(wrapper, func)


def create_cacher():
    """Возвращает функцию cache_result(key, value_func) с кэшем в замыкании.

    При повторном вызове с тем же ключом value_func не вызывается,
    а результат берётся из кэша.
    """
    cache = {}

    def cache_result(key, value_func):
        if key not in cache:
            cache[key] = value_func()
        return cache[key]

    return cache_result
