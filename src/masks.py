import logging
from src.logger_config import get_logger  # Точка означает "ищи в этой же папке"

logger: logging.Logger = get_logger("masks")
""" Инициализируем логер для модуля masks """


def get_mask_card_number(card_number: str) -> str:
    """ Маскирует номер карты, если он корректной длины. """
    logger.info("Начало маскирования номера карты")

    if len(card_number) != 16 or not card_number.isdigit():
        logger.error(
            f"Некорректный номер карты: '{card_number}'. Ожидалось 16 цифр."
        )
        return "Invalid card number"

    masked_card = (
        f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    )
    logger.info("Номер карты успешно замаскирован")
    return masked_card


def get_mask_account(account_number: str) -> str:
    """ Маскирует номер счета, если он корректной длины. """
    logger.info("Начало маскирования номера счета")

    if len(account_number) < 4 or not account_number.isdigit():
        logger.error(
            f"Некорректный номер счета: '{account_number}'. Ожидалось от 4 цифр."
        )
        return "Invalid account number"

    masked_account = f"**{account_number[-4:]}"
    logger.info("Номер счета успешно замаскирован")
    return masked_account
