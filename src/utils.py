import json
import logging
import os
from typing import Any, Dict, List
from src.logger_config import get_logger

logger: logging.Logger = get_logger("utils")
""" Инициализируем логер для модуля utils """


def get_transactions_data(path: str) -> List[Dict[str, Any]]:
    """ Функция открывает файл, читает его и превращает в список транзакций. """
    logger.info(f"Запрос на чтение транзакций из файла: {path}")

    """ Проверка на наличие файла """
    if not os.path.exists(path):
        logger.error(f"Файл не найден по пути: {path}")
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        """ Проверка, что внутри именно список """
        if isinstance(data, list):
            logger.info(
                f"Файл успешно прочитан. Найдено транзакций: {len(data)}"
            )
            return data

        logger.error(
            f"Некорректный формат данных в файле {path}: ожидался список, получен {type(data).__name__}"
        )
        return []

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {path}: {e}")
        return []
    except Exception as e:
        logger.error(f"Непредвиденная ошибка при чтении файла {path}: {e}")
        return []


""" Код для проверки (запуска) программы """
if __name__ == "__main__":
    file_path = "data/operations.json"
    transactions = get_transactions_data(file_path)

    for transaction in transactions:
        print(transaction.get("description"))
