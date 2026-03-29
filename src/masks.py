def get_mask_card_number(card_number: str) -> str:
    """Функция маскировки банковской карты"""
    """Преобразуем в строку на случай, если передано число"""
    card_str = str(card_number)

    """Берем первые 6 и последние 4 цифры"""
    first_part = card_str[:6]
    last_part = card_str[-4:]

    """Формируем маску: 6 цифр + 6 звездочек (вместо скрытых) + 4 цифры"""
    masked: str = f"{first_part[:4]} {first_part[4:]}** **** {last_part}"

    return masked


print(get_mask_card_number("7000792289606361"))


def get_mask_account(account_number: str) -> str:
    """Функция маскировки номера банковского счета"""
    """Берем срез последних 4 символов и добавляем две звездочки в начале"""
    return f"**{account_number[-4:]}"


print(get_mask_account("73654108430135874305"))
