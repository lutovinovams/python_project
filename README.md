Проект: "Банковские опеации"
Описание:
"Этот проект представляет собой виджет для обработки банковских операций, позволяющий фильтровать и сортировать транзакции по определённым критериям."

Установка:
клонируйте репозиторий: git clone https://github.com/lutovinovams/python_project.git
перейдите в директорию проекта: python_project
Использование:
* Функция filter_by_state:
Фильтрует список словарей по значению ключа state.

data: список словарей.
state****: строка для фильтрации (по умолчанию 'EXECUTED').
* Функция sort_by_date
Сортирует список словарей по ключу date.

data: список словарей.
reverse: порядок (по умолчанию True — от новых к старым).
Пример использования:
data = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]

Фильтрация:
filtered_transactions = filter_by_state(data)

print(filtered_transactions)

Выход: [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]
Сортировка:
sorted_transactions = sort_by_date(data)

print(sorted_transactions)

Выход: [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]

## Тестирование:

В проекте используются `pytest` для проведения тестов и `mypy` для проверки типизации.

### Запуск тестов
Чтобы запустить все тесты, выполните команду в корне проекта:

pytest

    *выход:
======================== test session starts ========================
platform win32 -- Python 3.14.3, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\Admin\Desktop\project\python_project
configfile: pyproject.toml
plugins: cov-7.1.0
collected 15 items                                                   

tests\test_masks.py ..                                         [ 13%]
tests\test_processing.py .....                                 [ 46%]
tests\test_widget.py ........                                  [100%] 

======================== 15 passed in 0.06s ========================= 
