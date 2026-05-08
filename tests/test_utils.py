import unittest
from unittest.mock import MagicMock, mock_open, patch

from src.utils import get_transactions_data


class TestUtils(unittest.TestCase):

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='[{"amount": 100}]')
    def test_get_transactions_data_success(self, mock_file: MagicMock, mock_exists: MagicMock) -> None:
        """ Тест успешного чтения корректного JSON-файла. """
        mock_exists.return_value = True

        result = get_transactions_data('data/test.json')

        self.assertEqual(result, [{"amount": 100}])
        mock_file.assert_called_once_with('data/test.json', 'r', encoding='utf-8')

    @patch('os.path.exists')
    def test_get_transactions_data_file_not_found(self, mock_exists: MagicMock) -> None:
        """ Тест возврата пустого списка, если файл не существует. """
        mock_exists.return_value = False

        result = get_transactions_data('non_existent.json')

        self.assertEqual(result, [])

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    def test_get_transactions_data_invalid_json(self, mock_file: MagicMock, mock_exists: MagicMock) -> None:
        """ Тест возврата пустого списка при битом JSON. """
        mock_exists.return_value = True

        result = get_transactions_data('bad.json')

        self.assertEqual(result, [])
