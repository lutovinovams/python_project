from unittest.mock import MagicMock, Mock, patch
import pandas as pd
import pytest

""" Импорт функции get_financial_transactions """
from src.file_readers import get_financial_transactions


@pytest.fixture
def mock_transaction_df() -> pd.DataFrame:
    """Фикстура для создания тестового DataFrame со значениями NaN."""
    data = [
        {"id": 1, "amount": 100.5, "currency": "RUB", "description": "Покупка"},
        {"id": 2, "amount": 200.0, "currency": "USD", "description": float("nan")},
    ]
    return pd.DataFrame(data)


# === ТЕСТЫ ДЛЯ CSV ===


@patch("os.path.exists")
@patch("pandas.read_csv")
def test_get_transactions_csv_success(
        mock_read_csv: MagicMock, mock_exists: MagicMock, mock_transaction_df: pd.DataFrame
) -> None:
    """Тест успешного чтения CSV с использованием mock и patch."""
    mock_exists.return_value = True
    mock_read_csv.return_value = mock_transaction_df

    result = get_financial_transactions("data/transactions.csv")

    mock_exists.assert_called_once_with("data/transactions.csv")
    mock_read_csv.assert_called_once()

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["description"] is None


# === ТЕСТЫ ДЛЯ EXCEL ===


@patch("os.path.exists")
@patch("pandas.read_excel")
def test_get_transactions_excel_success(
        mock_read_excel: MagicMock, mock_exists: MagicMock, mock_transaction_df: pd.DataFrame
) -> None:
    """Тест успешного чтения Excel с использованием mock и patch."""
    mock_exists.return_value = True
    mock_read_excel.return_value = mock_transaction_df

    result = get_financial_transactions("data/transactions_excel.xlsx")

    mock_exists.assert_called_once_with("data/transactions_excel.xlsx")
    mock_read_excel.assert_called_once()

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["currency"] == "RUB"


# === ТЕСТЫ НА КРАЕВЫЕ СЛУЧАИ И ИСКЛЮЧЕНИЯ ===


@patch("os.path.exists")
def test_get_transactions_file_not_found(mock_exists: MagicMock) -> None:
    """Тест ситуации, когда os.path.exists возвращает False."""
    mock_exists.return_value = False

    result = get_financial_transactions("data/missing.csv")

    assert result == []


@patch("os.path.exists")
def test_get_transactions_unsupported_extension(mock_exists: MagicMock) -> None:
    """Тест ситуации с неверным расширением файла (ветка else)."""
    mock_exists.return_value = True

    result = get_financial_transactions("data/transactions.txt")

    assert result == []


@patch("os.path.exists")
@patch("pandas.read_csv")
def test_get_transactions_empty_dataframe(
        mock_read_csv: MagicMock, mock_exists: MagicMock
) -> None:
    """Тест ситуации, когда DataFrame пустой (df.empty == True)."""
    mock_exists.return_value = True
    mock_read_csv.return_value = pd.DataFrame()

    result = get_financial_transactions("data/empty.csv")

    assert result == []


@patch("os.path.exists")
@patch("pandas.read_csv")
def test_get_transactions_parser_error(
        mock_read_csv: MagicMock, mock_exists: MagicMock
) -> None:
    """Тест обработки исключения ParserError (блок except)."""
    mock_exists.return_value = True
    mock_read_csv.side_effect = pd.errors.ParserError("Ошибка структуры CSV")

    result = get_financial_transactions("data/corrupted.csv")

    assert result == []


@patch("os.path.exists")
@patch("pandas.read_excel")
def test_get_transactions_value_error(
        mock_read_excel: MagicMock, mock_exists: MagicMock
) -> None:
    """Тест обработки исключения ValueError при чтении Excel (блок except)."""
    mock_exists.return_value = True

    mock_error = Mock(side_effect=ValueError("Неверный формат Excel"))
    mock_read_excel.side_effect = mock_error

    result = get_financial_transactions("data/bad_excel.xlsx")

    assert result == []
