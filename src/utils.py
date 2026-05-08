import json
import os
from typing import Any, Dict, List


def get_transactions_data(path: str) -> List[Dict[str, Any]]:
    """ Проверка на наличие файла """
    if not os.path.exists(path):
        return []

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            """ Проверка, что внутри именно список """
            if isinstance(data, list):
                return data
            return []

    except (json.JSONDecodeError, FileNotFoundError):
        """ Возврат пустого списка при ошибках или пустом файле """
        return []


""" Проверка """
file_path = 'data/operations.json'

""" Функция открывает файл, читает его и превращает в список транзакций """
transactions = get_transactions_data(file_path)

""" Теперь мы можем работать с данными """
for transaction in transactions:
    print(transaction.get('description'))
