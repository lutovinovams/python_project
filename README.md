platform win32 -- Python 3.14.3, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\Admin\Desktop\project\python_project
configfile: pyproject.toml
plugins: cov-7.1.0
collected 15 items                                                   

tests\test_masks.py ..                                         [ 13%]
tests\test_processing.py .....                                 [ 46%]
tests\test_widget.py ........                                  [100%] 

# Проект: "Банковские опеации"

##  Описание:

"Этот проект представляет собой виджет для обработки банковских операций, позволяющий фильтровать и сортировать транзакции по определённым критериям."

## Установка:
 * клонируйте репозиторий:
git clone https://github.com/lutovinovams/python_project.git
 * перейдите в директорию проекта:
python_project

# Использование:

### * Функция filter_by_state:

Фильтрует список словарей по значению ключа `state`.
- **data**: список словарей.
- **state******: строка для фильтрации (по умолчанию `'EXECUTED'`).

### * Функция sort_by_date

Сортирует список словарей по ключу `date`.
- **data**: список словарей.
- **reverse**: порядок (по умолчанию `True` — от новых к старым).

## Пример использования:
data = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]

 *  Фильтрация:

filtered_transactions = filter_by_state(data)

print(filtered_transactions)

 - Выход:
[{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]

 * Сортировка:

sorted_transactions = sort_by_date(data)

print(sorted_transactions)

 - Выход:
[{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]

## Тестирование:

В проекте используются `pytest` для проведения тестов и `mypy` для проверки типизации.

### Запуск тестов
Чтобы запустить все тесты, выполните команду в корне проекта:

pytest

    *выход:
==================== test session starts ====================
platform win32 -- Python 3.14.3, pytest-9.0.3, pluggy-1.6.0   
rootdir: C:\Users\Admin\Desktop\project\python_project
configfile: pyproject.toml
plugins: cov-7.1.0
collected 24 items                                           

tests\test_masks.py ...........                        [ 45%] 
tests\test_processing.py .....                         [ 66%]
tests\test_widget.py ........                          [100%]

==================== 24 passed in 0.14s ===================== 

## Модуль Generators

Модуль `src/generators.py` предназначен для эффективной фильтрации и генерации финансовых данных. Использование генераторов позволяет обрабатывать большие объемы данных с минимальным потреблением оперативной памяти.

### Основные возможности

*   **Фильтрация по валюте** (`filter_by_currency`): Позволяет получить все транзакции по конкретному коду валюты (USD, RUB и т.д.).
*   **Извлечение описаний** (`transaction_descriptions`): Генератор, возвращающий только текст описания для каждой операции.
*   **Генератор номеров карт** (`card_number_generator`): Создает номера карт в формате `XXXX XXXX XXXX XXXX` в заданном числовом диапазоне.

### Примеры использования
```python
from src.generators import filter_by_currency, card_number_generator

# Фильтрация транзакций
usd_transactions = filter_by_currency(transactions, "USD")

# Генерация номеров карт от 1 до 5
for card in card_number_generator(1, 5):
    print(card)
# Вывод: 0000 0000 0000 0001 ...
```


### Тестирование и качество кода

В проекте настроено автоматическое тестирование:

1.  **Запуск тестов**:
    ```bash
    pytest
    
2. **Выход**:

==================== test session starts ====================
platform win32 -- Python 3.14.3, pytest-9.0.3, pluggy-1.6.0   
rootdir: C:\Users\Admin\Desktop\project\python_project
configfile: pyproject.toml
plugins: cov-7.1.0
collected 31 items                                           

tests\test_generators.py .......                       [ 22%] 
tests\test_masks.py ...........                        [ 58%]
tests\test_processing.py .....                         [ 74%] 
tests\test_widget.py ........                          [100%]

==================== 31 passed in 0.08s ===================== 

## Описание функций

### 1. Загрузка данных о транзакциях (`utils.py`)
Функция `get_transactions_data(path)` отвечает за чтение истории операций из файла.
* **Что делает**: Принимает путь к JSON-файлу, проверяет его наличие и корректность.
* **Результат**: Возвращает список словарей с данными о транзакциях. Если файл пустой, поврежден или отсутствует, функция вернет пустой список `[]`.

### 2. Конвертация валюты (`external_api.py`)
Функция `get_transaction_amount_in_rub(transaction)` вычисляет итоговую сумму операции в рублях.
* **Логика**:
    - Если транзакция в **RUB**, возвращает сумму как есть.
    - Если транзакция в **USD** или **EUR**, обращается к *Exchange Rates Data API* для получения актуального курса и конвертирует сумму.
* **Тип данных**: Всегда возвращает число с плавающей точкой (`float`).
* **Безопасность**: API-ключ скрыт в переменных окружения (`.env`).

## Настройка и установка

1. **Установите зависимости**:
   
   pip install requests python-dotenv
  
2. **Создайте файл `.env`** в корне проекта и добавьте ваш ключ:
   ```env
   API_KEY=ваш_секретный_ключ_с_apilayer
   ```

## Использование

from src.utils import get_transactions_data
from src.external_api import get_transaction_amount_in_rub

# 1. Получаем данные из файла
transactions = get_transactions_data('data/operations.json')

# 2. Конвертируем сумму первой транзакции в рубли
if transactions:
    amount_in_rub = get_transaction_amount_in_rub(transactions[0])
    print(f"Сумма: {amount_in_rub} руб.")

## Тестирование

В проекте используется библиотека `unittest` и фреймворк `pytest` для автоматического тестирования функций. Все тесты реализованы с использованием **Mock-объектов**, что позволяет проверять код без обращения к реальному API и без создания физических файлов на диске.

### Что проверяют тесты:
1. **Конвертация валют**:
   - Успешный ответ от API при передаче USD/EUR.
   - Корректность возвращаемого типа данных (`float`).
   - Отсутствие запросов к API, если транзакция уже в рублях.
   - Обработка сетевых ошибок и тайм-аутов API (функция должна возвращать `None`).
2. **Работа с файлами (JSON)**:
   - Чтение корректного JSON-файла.
   - Обработка ситуации, когда файл отсутствует или поврежден (возврат пустого списка).

### Запуск тестов

Вы можете запустить тесты любым удобным способом:

**Через pytest (рекомендуется):**

pytest


**Через стандартный модуль unittest:**

python -m unittest discover tests
