import re
from collections import Counter


def filter_operations_by_description(data: list[dict], search_string: str) -> list[dict]:
    """Фильтрует список транзакций по ключевой строке в описании с использованием re (регистронезависимо)."""
    if not search_string:
        return data

    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    filtered_data = []

    for operation in data:
        description = operation.get("description")
        if isinstance(description, str) and pattern.search(description):
            filtered_data.append(operation)

    return filtered_data


def count_operations_by_category(data: list[dict], categories: list[str]) -> dict[str, int]:
    """Подсчитывает количество операций для заданных категорий с использованием Counter."""
    descriptions = [
        op.get("description") for op in data if isinstance(op.get("description"), str)
    ]
    counts = Counter(descriptions)
    return {category: counts[category] for category in categories}
