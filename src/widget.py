"""Импортируем функции get_mask_card_number и get_mask_account из модуля masks.py"""

from .masks import get_mask_account, get_mask_card_number


def mask_account_card(data: str) -> str:
    """Объединяет название и замаскированный номер через импортированные функции"""
    parts = data.split()
    name = " ".join(parts[:-1])
    number = parts[-1]

    if name.lower().startswith("счет"):
        masked = get_mask_account(number)
    else:
        masked = get_mask_card_number(number)

    return f"{name} {masked}"


# Проверка:
print(mask_account_card("Visa Platinum 7000792289606361"))
print(mask_account_card("Счет 73654108430135874305"))


def get_date(date_str: str) -> str:
    """Принимает строку с датой в формате ISO и возвращает дату в формате ДД.ММ.ГГГГ"""
    # Извлекаем год, месяц и день с помощью срезов
    year = date_str[:4]
    month = date_str[5:7]
    day = date_str[8:10]

    return f"{day}.{month}.{year}"


# Проверка:
print(get_date("2024-03-11T02:26:18.671407"))  # 11.03.2024
