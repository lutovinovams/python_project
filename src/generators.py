from typing import Any, Dict, Generator, Iterable


def filter_by_currency(transactions: Iterable[Dict[str, Any]], currency: str) -> Generator[Dict[str, Any], None, None]:
    """Фильтрует транзакции по коду валюты."""
    for transaction in transactions:
        if transaction.get("operation_amount", {}).get("currency", {}).get("code") == currency:
            yield transaction


def transaction_descriptions(transactions: Iterable[Dict[str, Any]]) -> Generator[str, None, None]:
    """Возвращает описание каждой транзакции."""
    for transaction in transactions:
        yield transaction.get("description", "Описание отсутствует")


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """Генерирует номера карт в формате XXXX XXXX XXXX XXXX в заданном диапазоне."""
    for number in range(start, end + 1):
        # Форматируем число в строку из 16 цифр с ведущими нулями
        card_str = f"{number:016d}"
        # Разбиваем строку на группы по 4 цифры через пробел
        formatted_card = f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"
        yield formatted_card
