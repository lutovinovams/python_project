import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number() -> None:
    @pytest.fixture
    def card_number_sample() -> str:
        """Фикстура, возвращающая корректный номер карты для тестов."""
        return "7000792289606361"

    def test_get_mask_card_number_correct(card_number_sample: str) -> None:
        """Тест на правильность маскирования корректного номера."""
        result = get_mask_card_number(card_number_sample)
        assert result == "7000 79** **** 6361"

    @pytest.mark.parametrize("invalid_number", [
        "123",  # Слишком короткий
        "12345678901234567",  # Слишком длинный
        "1234abcd5678efgh",  # Содержит буквы
        ""  # Пустая строка
    ])
    def test_get_mask_card_number_invalid(invalid_number: str) -> None:
        """Параметризованный тест для проверки обработки некорректных входных данных."""
        # Если ваша функция возвращает ошибку или сообщение, проверьте это:
        assert get_mask_card_number(invalid_number) == "Invalid card number"

    def test_get_mask_card_number_return_type(card_number_sample: str) -> None:
        """Проверка, что функция всегда возвращает строку."""
        assert isinstance(get_mask_card_number(card_number_sample), str)


def test_get_mask_account() -> None:
    @pytest.fixture
    def account_number() -> str:
        """Фикстура для стандартного номера счета."""
        return "73654108430135874305"

    def test_get_mask_account_standard(account_number: str) -> None:
        """Тест на стандартный номер счета (20 знаков)."""
        assert get_mask_account(account_number) == "**4305"

    @pytest.mark.parametrize("value, expected", [
        ("73654108430135874305", "**4305"),
        ("12345678901234567890", "**7890"),
        ("00000000000000000001", "**0001"),
    ])
    def test_get_mask_account_variants(value: str , expected: str) -> None:
        """Параметризованный тест для проверки разных номеров."""
        assert get_mask_account(value) == expected

    def test_get_mask_account_empty() -> None:
        """Проверка обработки пустой строки (зависит от логики функции)."""
        # Если функция должна возвращать пустую строку или ошибку
        assert get_mask_account("") == ""
