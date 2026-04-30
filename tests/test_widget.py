import pytest

from src.widget import get_date, mask_account_card


# Тесты для функции mask_account_card
@pytest.mark.parametrize("value, expected", [
    ("Visa Gold 7000792289606361", "Visa Gold 7000 79** **** 6361"),
    ("MasterCard 7158300714707589", "MasterCard 7158 30** **** 7589"),
    ("Счет 73654108430135874305", "Счет **4305"),
    ("Maestro 1596837493215786", "Maestro 1596 83** **** 5786"),
])
def test_mask_account_card_variants(value: str, expected: str) -> None:
    """Проверка различных типов карт и счетов."""
    assert mask_account_card(value) == expected


# Тесты для функции get_date
@pytest.mark.parametrize("date_raw, expected", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2023-12-31T23:59:59.999999", "31.12.2023"),
    ("2025-01-01T00:00:00.000000", "01.01.2025"),
])
def test_get_date_variants(date_raw: str, expected: str) -> None:
    """Проверка корректного форматирования даты."""
    assert get_date(date_raw) == expected


def test_get_date_empty() -> None:
    """Пример теста без аргументов (если нужно проверить специфику)."""
    assert get_date("2018-07-11T02:26:18.671407") == "11.07.2018"
    