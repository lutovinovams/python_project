from src.processing import filter_by_state, sort_by_date
from src.search import filter_operations_by_description
from src.widget import mask_account_card


def main() -> None:

    # 1. Приветствие и выбор формата файла
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла\n")

    while True:
        choice = input("Пользователь: ").strip()
        if choice == "1":
            print("\nПрограмма: Для обработки выбран JSON-файл.")
            from src.utils import get_transactions_data
            data = get_transactions_data("data/operations.json")
            break
        elif choice == "2":
            print("\nПрограмма: Для обработки выбран CSV-файл.")
            from src.file_readers import get_financial_transactions
            data = get_financial_transactions("data/transactions.csv")
            break
        elif choice == "3":
            print("\nПрограмма: Для обработки выбран XLSX-файл.")
            from src.file_readers import get_financial_transactions
            data = get_financial_transactions("data/transactions_excel.xlsx")
            break
        else:
            print("Программа: Неверный пункт меню. Выберите 1, 2 или 3.")

    """ 2. Выбор статуса с валидацией ввода и приведением регистра """
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        print('\nПрограмма: Введите статус, по которому необходимо выполнить фильтрацию.')
        print('Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n')

        status_input = input("Пользователь: ").strip().upper()

        if status_input in valid_statuses:
            print(f'\nПрограмма: Операции отфильтрованы по статусу "{status_input}"')
            data = filter_by_state(data, status_input)
            break
        else:
            print(f'\nПрограмма: Статус операции "{status_input}" недоступен.')

    """ 3. Сортировка по дате с валидацией """
    while True:
        print('\nПрограмма: Отсортировать операции по дате? Да/Нет\n')
        sort_choice = input("Пользователь: ").strip().lower()
        if sort_choice in ["да", "нет"]:
            break
        print("Программа: Пожалуйста, введите 'Да' или 'Нет'.")

    if sort_choice == "да":
        while True:
            print('\nПрограмма: Отсортировать по возрастанию или по убыванию?\n')
            direction_choice = input("Пользователь: ").strip().lower()
            if direction_choice in ["по возрастанию", "по убыванию", "возрастанию", "убыванию"]:
                break
            print("Программа: Пожалуйста, введите 'по возрастанию' или 'по убыванию'.")

        reverse = True if "убыван" in direction_choice else False
        data = sort_by_date(data, reverse=reverse)

    """ 4. Фильтрация по валюте (универсальный безопасный парсинг JSON/CSV/XLSX) """
    while True:
        print('\nПрограмма: Выводить только рублевые транзакции? Да/Нет\n')
        rub_choice = input("Пользователь: ").strip().lower()
        if rub_choice in ["да", "нет"]:
            break
        print("Программа: Пожалуйста, введите 'Да' или 'Нет'.")

    if rub_choice == "да":
        rub_data = []
        for op in data:
            # Безопасно проверяем вложенную структуру (JSON)
            currency_json = op.get("operationAmount", {}).get("currency", {}).get("code")
            # Безопасно проверяем плоскую структуру (CSV/XLSX)
            currency_csv = op.get("currency_code")

            if currency_json == "RUB" or currency_csv == "RUB":
                rub_data.append(op)
        data = rub_data

    """ 5. Фильтрация по ключевому слову в описании """
    while True:
        print('\nПрограмма: Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n')
        word_choice = input("Пользователь: ").strip().lower()
        if word_choice in ["да", "нет"]:
            break
        print("Программа: Пожалуйста, введите 'Да' или 'Нет'.")

    if word_choice == "да":
        print('\nПрограмма: Введите слово для поиска:\n')
        search_string = input("Пользователь: ").strip()
        data = filter_operations_by_description(data, search_string)

    """ 6. Вывод итоговых результатов в нужном формате """
    print('\nПрограмма: Распечатываю итоговый список транзакций...\n')

    if not data:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Программа:\nВсего банковских операций в выборке: {len(data)}\n")

    for op in data:
        # Форматирование даты из ISO формата (2019-12-08T...) в ДД.ММ.ГГГГ
        date_raw = op.get("date", "")
        if isinstance(date_raw, str) and len(date_raw) >= 10:
            parts = date_raw[:10].split("-")
            date_formatted = f"{parts[2]}.{parts[1]}.{parts[0]}" if len(parts) == 3 else date_raw[:10]
        else:
            date_formatted = "Дата неизвестна"

        description = op.get("description", "Без описания")

        """ Получение и маскирование отправителя и получателя """
        from_info = op.get("from", "")
        to_info = op.get("to", "")

        """ Вызов функции маскировки карт/счетов """
        from_masked = mask_account_card(from_info) if from_info else ""
        to_masked = mask_account_card(to_info) if to_info else ""

        transfer_route = ""
        if from_masked and to_masked:
            transfer_route = f"{from_masked} -> {to_masked}"
        elif to_masked:
            transfer_route = f"{to_masked}"

        """ Извлечение суммы и валюты для разных типов файлов """
        amount = op.get("amount")
        currency = op.get("currency_code")

        if not amount:  # Если структура вложенная (JSON)
            amount = op.get("operationAmount", {}).get("amount", "0")
            currency = op.get("operationAmount", {}).get("currency", {}).get("name", "руб.")

        if currency in ["RUB", "руб."]:
            currency = "руб."

        """ Печать транзакции """
        print(f"{date_formatted} {description}")
        if transfer_route:
            print(transfer_route)
        print(f"Сумма: {amount} {currency}\n")


if __name__ == "__main__":
    main()
