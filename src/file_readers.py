import os
import pandas as pd


def get_financial_transactions(file_path: str) -> list[dict]:
    """Считывает финансовые транзакции из CSV или XLSX файла.

    Возвращает список словарей. Если файл пустой или не найден, возвращает
    пустой список.
    """
    # 1. Проверяем, существует ли файл по указанному пути
    if not os.path.exists(file_path):
        return []

    # 2. Получаем расширение файла для определения его формата
    _, ext = os.path.splitext(file_path.lower())

    try:
        # 3. Читаем файл в DataFrame в зависимости от расширения
        if ext == ".csv":
            # sep=None и engine='python' автоматически определяют разделитель (, или ;)
            df = pd.read_csv(file_path, sep=None, engine="python")
        elif ext in [".xlsx", ".xls"]:
            df = pd.read_excel(file_path)
        else:
            return []  # Неподдерживаемый формат

        # 4. Если файл оказался пустым, возвращаем пустой список
        if df.empty:
            return []

        # 5. Очищаем данные от NaN (пустых ячеек), заменяя их на None (аналог null в JSON)
        df = df.astype(object).replace({pd.NA: None, float("nan"): None})
        # 6. Конвертируем DataFrame в список словарей
        return list(df.to_dict(orient="records"))

    except (
            FileNotFoundError,
            pd.errors.EmptyDataError,
            pd.errors.ParserError,
            ValueError,
    ) as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")

        return []
