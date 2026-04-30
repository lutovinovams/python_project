import pytest
from typing import Any, List, Dict
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


@pytest.fixture
def transactions_data() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми данными транзакций."""
    return [
        {"id": 1, "description": "Перевод организации", "operation_amount": {"currency": {"code": "USD"}}},
        {"id": 2, "description": "Перевод со счета на счет", "operation_amount": {"currency": {"code": "RUB"}}},
        {"id": 3, "description": "Оплата услуг", "operation_amount": {"currency": {"code": "USD"}}},
    ]


# Тестирование filter_by_currency
def test_filter_by_currency_usd(transactions_data: List[Dict[str, Any]]) -> None:
    """Проверка фильтрации по существующей валюте."""
    result = list(filter_by_currency(transactions_data, "USD"))
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_filter_by_currency_empty() -> None:
    """Проверка обработки пустого списка и отсутствующей валюты."""
    assert list(filter_by_currency([], "USD")) == []

    data = [{"operationAmount": {"currency": {"code": "EUR"}}}]
    assert list(filter_by_currency(data, "USD")) == []


# Тестирование transaction_descriptions
def test_transaction_descriptions_valid(transactions_data: List[Dict[str, Any]]) -> None:
    """Проверка получения корректных описаний."""
    descriptions = transaction_descriptions(transactions_data)
    assert next(descriptions) == "Перевод организации"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Оплата услуг"


def test_transaction_descriptions_various_counts() -> None:
    """Тест с разным количеством входных данных."""
    assert list(transaction_descriptions([])) == []

    single_item = [{"description": "Тест"}]
    assert list(transaction_descriptions(single_item)) == ["Тест"]


# Тестирование card_number_generator
def test_card_number_generator_range() -> None:
    """Проверка диапазона и корректности завершения генерации."""
    gen = card_number_generator(1, 3)
    results = list(gen)
    assert len(results) == 3
    assert results[0] == "0000 0000 0000 0001"
    assert results[-1] == "0000 0000 0000 0003"


def test_card_number_generator_format() -> None:
    """Проверка правильности форматирования (пробелы и нули)."""
    gen = card_number_generator(10, 10)
    assert next(gen) == "0000 0000 0000 0010"


def test_card_number_generator_boundaries() -> None:
    """Проверка крайних значений диапазона."""
    gen = card_number_generator(9999999999999998, 9999999999999999)
    results = list(gen)
    assert results == ["9999 9999 9999 9998", "9999 9999 9999 9999"]
