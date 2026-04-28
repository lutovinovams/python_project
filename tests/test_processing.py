import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_data() -> list[dict]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
        {"id": 2, "state": "CANCELED", "date": "2023-12-31T23:59:59.999999"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-01T00:00:00.000000"},
    ]


def test_filter_by_state_executed(sample_data: list[dict]) -> None:
    """Тест фильтрации по статусу EXECUTED."""
    result = filter_by_state(sample_data, "EXECUTED")
    assert len(result) == 2
    assert all(item["state"] == "EXECUTED" for item in result)


def test_filter_by_state_canceled(sample_data: list[dict]) -> None:
    """Тест фильтрации по статусу CANCELED."""
    result = filter_by_state(sample_data, "CANCELED")
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_filter_by_state_empty_result(sample_data: list[dict]) -> None:
    """Тест фильтрации с несуществующим статусом."""
    result = filter_by_state(sample_data, "PENDING")
    assert result == []


def test_sort_by_date_descending(sample_data: list[dict]) -> None:
    """Тест сортировки по дате (по убыванию — по умолчанию)."""
    result = sort_by_date(sample_data)
    assert result[0]["id"] == 1  # Самая свежая дата (март 2024)
    assert result[-1]["id"] == 2  # Самая старая дата (декабрь 2023)


def test_sort_by_date_ascending(sample_data: list[dict]) -> None:
    """Тест сортировки по дате (по возрастанию)."""
    result = sort_by_date(sample_data, reverse=False)
    assert result[0]["id"] == 2  # Сначала старая
    assert result[-1]["id"] == 1  # В конце свежая
