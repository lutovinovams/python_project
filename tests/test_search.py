import pytest

from src.search import count_operations_by_category, filter_operations_by_description


@pytest.fixture
def sample_transactions() -> list[dict]:
    """Фикстура с тестовым набором банковских операций."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01", "description": "Перевод организации"},
        {"id": 2, "state": "EXECUTED", "date": "2023-01-02", "description": "Перевод с карты на карту"},
        {"id": 3, "state": "CANCELED", "date": "2023-01-03", "description": "Открытие вклада"},
        {"id": 4, "state": "EXECUTED", "date": "2023-01-04", "description": "Покупка авиабилетов"},
        {"id": 5, "state": "EXECUTED", "date": "2023-01-05", "description": None},  # Битые данные
        {"id": 6, "state": "EXECUTED", "date": "2023-01-06"},  # Отсутствует поле description
    ]


# ТЕСТЫ ДЛЯ ФУНКЦИИ filter_operations_by_description


def test_filter_by_description_success(sample_transactions: list[dict]) -> None:
    """Тест успешного поиска операций по слову (без учета регистра)."""
    # Поиск слова в нижнем регистре
    result_lower = filter_operations_by_description(sample_transactions, "перевод")
    assert len(result_lower) == 2
    assert result_lower[0]["id"] == 1
    assert result_lower[1]["id"] == 2

    # Поиск того же слова с заглавной буквы
    result_capital = filter_operations_by_description(sample_transactions, "Перевод")
    assert len(result_capital) == 2


def test_filter_by_description_not_found(sample_transactions: list[dict]) -> None:
    """Тест ситуации, когда совпадений не найдено."""
    result = filter_operations_by_description(sample_transactions, "Оплата ЖКХ")
    assert result == []


def test_filter_by_description_empty_search(sample_transactions: list[dict]) -> None:
    """Тест с пустой строкой поиска (должен возвращать исходный список)."""
    result = filter_operations_by_description(sample_transactions, "")
    assert result == sample_transactions


def test_filter_by_description_special_characters(sample_transactions: list[dict]) -> None:
    """Тест работы с регулярными выражениями и спецсимволами (не должно падать)."""
    result = filter_operations_by_description(sample_transactions, "перевод.*")
    assert result == []  # re.escape экранирует точку и звездочку, поэтому точного совпадения нет


# ТЕСТЫ ДЛЯ ФУНКЦИИ count_operations_by_category


def test_count_by_category_success(sample_transactions: list[dict]) -> None:
    """Тест успешного подсчета категорий с использованием Counter."""
    categories = ["Перевод с карты на карту", "Открытие вклада", "Несуществующая категория"]
    result = count_operations_by_category(sample_transactions, categories)

    assert result == {
        "Перевод с карты на карту": 1,
        "Открытие вклада": 1,
        "Несуществующая категория": 0,
    }


def test_count_by_category_empty_data() -> None:
    """Тест подсчета категорий на пустом списке транзакций."""
    categories = ["Перевод с карты на карту"]
    result = count_operations_by_category([], categories)
    assert result == {"Перевод с карты на карту": 0}


def test_count_by_category_empty_categories(sample_transactions: list[dict]) -> None:
    """Тест передачи пустого списка категорий."""
    result = count_operations_by_category(sample_transactions, [])
    assert result == {}
