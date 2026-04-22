data = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]


def filter_by_state(data: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Фильтрует список словарей по значению ключа state."""
    return [item for item in data if item.get("state") == state]


filtered_transactions = filter_by_state(data)
print(filtered_transactions)


def sort_by_date(data: list[dict], reverse: bool = True) -> list[dict]:
    """Сортирует список словарей по ключу 'date'.
    :param data: Список словарей для сортировки.
    :param reverse: Порядок сортировки (True — убывание, False — возрастание).
    :return: Новый отсортированный список.
    """
    return sorted(data, key=lambda x: x.get("date", ""), reverse=reverse)


sorted_transactions = sort_by_date(data)
print(sorted_transactions)
