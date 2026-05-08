import unittest
from unittest.mock import MagicMock, patch

from src.external_api import get_transaction_amount_in_rub


class TestExternalAPI(unittest.TestCase):

    @patch('src.external_api.requests.get')
    def test_get_transaction_amount_usd(self, mock_get: MagicMock) -> None:
        """Тест успешной конвертации из USD."""
        # Настраиваем мок ответа API
        mock_response = MagicMock()
        mock_response.json.return_value = {'result': 7500.0}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        transaction = {'amount': 100, 'currency': 'USD'}
        result = get_transaction_amount_in_rub(transaction)

        self.assertEqual(result, 7500.0)
        self.assertIsInstance(result, float)

    def test_get_transaction_amount_rub(self) -> None:
        """Тест транзакции в рублях (запрос к API не должен выполняться)."""
        transaction = {'amount': 100.0, 'currency': 'RUB'}

        with patch('src.external_api.requests.get') as mock_get:
            result = get_transaction_amount_in_rub(transaction)
            self.assertEqual(result, 100.0)
            mock_get.assert_not_called()

    @patch('src.external_api.requests.get')
    def test_get_transaction_amount_api_error(self, mock_get: MagicMock) -> None:
        """Тест обработки ошибки API (timeout или ошибка сети)."""
        # Имитируем ошибку сети
        mock_get.side_effect = Exception("Network error")

        transaction = {'amount': 100, 'currency': 'EUR'}

        # Вызываем функцию
        result = get_transaction_amount_in_rub(transaction)

        # ПРОВЕРКА: Функция должна поймать исключение внутри себя и вернуть None
        self.assertIsNone(result)
