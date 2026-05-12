import os

import requests
from typing import Any, Dict, Optional
from dotenv import load_dotenv

""" Загружаем переменные из .env """
load_dotenv()


def get_transaction_amount_in_rub(transaction: Dict[str, Any]) -> Optional[float]:
    amount = float(transaction.get('amount', 0))
    currency = transaction.get('currency')

    if currency == 'RUB':
        return amount

    if currency in ['USD', 'EUR']:
        """ Получаем API_KEY из переменных окружения """
        api_key = os.getenv('API_KEY')

        if not api_key:
            print("Ошибка: API_KEY не найден в переменных окружения.")
            return None

        url = "https://apilayer.com"
        headers = {"apikey": api_key}
        params = {"to": "RUB", "from": currency, "amount": amount}

        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            return float(data.get('result', 0.0))
        except Exception:  # Перехватываем все ошибки, чтобы функция вернула None
            return None

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при обращении к API: {e}")
            return None

    return amount
