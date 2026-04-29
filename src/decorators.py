import functools
import os
from typing import Any, Callable, Optional, TypeVar

# Типизация для декоратора
F = TypeVar("F", bound=Callable[..., Any])


def log(filename: Optional[str] = None) -> Callable[[F], F]:
    """Декоратор, логирующий начало, результат или ошибку работы функции."""

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok. Result: {result}"
                _write_log(log_message, filename)
                return result
            except Exception as e:
                error_type = type(e).__name__
                log_message = f"{func.__name__} error: {error_type}. Inputs: {args}, {kwargs}"
                _write_log(log_message, filename)
                raise e

        return wrapper  # type: ignore

    return decorator


def _write_log(message: str, filename: Optional[str]) -> None:
    """Записывает сообщение в файл или выводит в консоль."""
    if filename:
        # Проверка: если в пути есть папки, создаем их
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(filename, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    else:
        print(message)
