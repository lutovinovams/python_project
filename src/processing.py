def filter_by_state(data: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """Фильтрует список словарей по значению ключа state."""
    return [item for item in data if item.get('state') == state]


def sort_by_date(data: list[dict], reverse: bool = True) -> list[dict]:
    """
    Сортирует список словарей по ключу 'date'.

    :param data: Список словарей для сортировки.
    :param reverse: Порядок сортировки (True — убывание, False — возрастание).
    :return: Новый отсортированный список.
    """
    return sorted(data, key=lambda x: x.get('date', ''), reverse=reverse)

