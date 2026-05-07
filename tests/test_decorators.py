import os
from typing import Any
import pytest
from src.decorators import log


# Тестовые функции для использования с декоратором
@log()
def add_numbers(x: int, y: int) -> int:
    return x + y


@log()
def divide_numbers(x: int, y: int) -> float:
    return x / y


def test_log_to_console_ok(capsys: pytest.CaptureFixture) -> None:
    """Проверка логирования успешного выполнения в консоль."""
    add_numbers(5, 10)
    captured = capsys.readouterr()
    assert "add_numbers ok. Result: 15" in captured.out


def test_log_to_console_error(capsys: pytest.CaptureFixture) -> None:
    """Проверка логирования ошибки в консоль."""
    with pytest.raises(ZeroDivisionError):
        divide_numbers(1, 0)
    captured = capsys.readouterr()
    assert "divide_numbers error: ZeroDivisionError. Inputs: (1, 0), {}" in captured.out


def test_log_to_file_ok(tmp_path: Any) -> None:
    """Проверка логирования успешного выполнения в файл."""
    log_file = tmp_path / "test_log.txt"

    @log(filename=str(log_file))
    def multiply(x: int, y: int) -> int:
        return x * y

    multiply(3, 4)

    with open(log_file, "r", encoding="utf-8") as f:
        log_content = f.read()
    assert "multiply ok. Result: 12" in log_content


def test_log_to_file_error(tmp_path: Any) -> None:
    """Проверка логирования ошибки в файл."""
    log_file = tmp_path / "error_log.txt"

    @log(filename=str(log_file))
    def fail_func() -> None:
        raise ValueError("Something went wrong")

    with pytest.raises(ValueError):
        fail_func()

    with open(log_file, "r", encoding="utf-8") as f:
        log_content = f.read()
    assert "fail_func error: ValueError. Inputs: (), {}" in log_content


def test_log_creates_directory(tmp_path: Any) -> None:
    """Проверка автоматического создания папок для лога."""
    deep_log_file = tmp_path / "new_folder" / "sub_folder" / "log.txt"

    @log(filename=str(deep_log_file))
    def simple_func() -> str:
        return "done"

    simple_func()
    assert os.path.exists(deep_log_file)
