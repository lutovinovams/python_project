def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты, если он корректной длины."""
    if len(card_number) != 16 or not card_number.isdigit():
        return "Invalid card number"

    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счета, если он корректной длины."""
    if len(account_number) < 4 or not account_number.isdigit():
        return "Invalid account number"

    return f"**{account_number[-4:]}"
