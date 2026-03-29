# Банковский виджет операций

Проект для маскировки и обработки банковских операций клиента. Реализует функциональность виджета личного кабинета для отображения последних успешных операций.

## Описание проекта

Проект предоставляет набор функций для:
- Маскировки номеров банковских карт и счетов
- Форматирования дат в удобный для отображения формат
- Обработки информации о банковских операциях
- Фильтрации и сортировки операций по различным критериям
- Генерации данных для работы с транзакциями
- Логирования вызовов функций с помощью декоратора
- Чтения данных из JSON, CSV и Excel файлов
- Конвертации валют (USD, EUR) в рубли через внешнее API
- Поиска транзакций по описанию с использованием регулярных выражений
- Подсчёта операций по категориям
- Интерактивного меню для работы с транзакциями

## Структура проекта
mask_card_number_9_2/
├── data/ # Данные
│ ├── operations.json # Банковские операции (JSON)
│ ├── transactions.csv # Банковские операции (CSV)
│ └── transactions_excel.xlsx # Банковские операции (Excel)
├── logs/ # Логи (создаётся автоматически)
│ ├── masks.log # Логи модуля masks
│ └── utils.log # Логи модуля utils
├── src/ # Исходный код
│ ├── masks.py # Маскировка карт и счетов
│ ├── widget.py # Функции для виджета
│ ├── processing.py # Обработка списков операций
│ ├── generators.py # Генераторы для транзакций
│ ├── decorators.py # Декораторы для логирования
│ ├── utils.py # Утилиты (чтение JSON)
│ ├── external_api.py # Работа с внешним API
│ ├── logger_config.py # Настройка логирования
│ ├── file_reader.py # Чтение CSV и Excel файлов
│ ├── search_utils.py # Поиск транзакций
│ └── category_utils.py # Подсчёт по категориям
├── tests/ # Тесты
│ ├── conftest.py # Общие фикстуры
│ ├── test_masks.py
│ ├── test_widget.py
│ ├── test_processing.py
│ ├── test_generators.py
│ ├── test_decorators.py
│ ├── test_utils.py
│ ├── test_external_api.py
│ ├── test_logging.py
│ ├── test_file_reader.py
│ ├── test_search_utils.py
│ └── test_category_utils.py
├── htmlcov/ # Отчет о покрытии (генерируется)
├── main.py # Главный модуль с интерфейсом
├── pyproject.toml
├── poetry.lock
├── .flake8
├── .gitignore
├── .env.example
└── README.md

text

## Установка и настройка

### Предварительные требования
- Python 3.14 или выше
- Poetry (менеджер зависимощений)

### Установка

```
# Клонировать репозиторий
git clone https://github.com/your-username/bank-widget.git
cd bank-widget

# Установить зависимости через Poetry
poetry install
poetry install --only lint
poetry install --only test

# Создать файл с переменными окружения
cp .env.example .env
# Добавьте ваш API ключ в .env
Настройка API ключа
Для работы конвертации валют необходим API ключ:

Зарегистрируйтесь на apilayer.com/exchangerates_data-api

Получите бесплатный API ключ

Добавьте его в файл .env:


EXCHANGE_RATES_API_KEY=your_api_key_here
Использование
1. Маскировка номеров карт и счетов

from src.masks import get_mask_card_number, get_mask_account

# Маскировка номера карты (16 цифр)
card_number = "7000792289606361"
masked_card = get_mask_card_number(card_number)
print(masked_card)  # "7000 79** **** 6361"

# Маскировка номера счета (минимум 4 цифры)
account_number = "73654108430135874305"
masked_account = get_mask_account(account_number)
print(masked_account)  # "**4305"
2. Универсальная функция для карт и счетов

from src.widget import mask_account_card, get_date

# Автоматическое определение типа (карта или счет)
card_info = "Visa Platinum 7000792289606361"
masked_card_info = mask_account_card(card_info)
print(masked_card_info)  # "Visa Platinum 7000 79** **** 6361"

account_info = "Счет 73654108430135874305"
masked_account_info = mask_account_card(account_info)
print(masked_account_info)  # "Счет **4305"

# Форматирование даты
date_str = "2024-03-11T02:26:18.671407"
formatted_date = get_date(date_str)
print(formatted_date)  # "11.03.2024"
3. Обработка списка операций

from src.processing import filter_by_state, sort_by_date

operations = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
]

# Фильтрация по статусу
executed_operations = filter_by_state(operations)  # только EXECUTED
sorted_ops = sort_by_date(operations)  # по убыванию (сначала новые)
4. Генераторы для работы с транзакциями

from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

# Фильтрация по валюте
usd_transactions = list(filter_by_currency(transactions, "USD"))

# Описания транзакций
for desc in transaction_descriptions(transactions):
    print(desc)

# Генерация номеров карт
for card in card_number_generator(1, 5):
    print(card)  # 0000 0000 0000 0001, 0000 0000 0000 0002, ...
5. Декоратор логирования (log)

from src.decorators import log

# Логирование в консоль
@log()
def add(a: int, b: int) -> int:
    return a + b

add(2, 3)  # "2024-01-01 12:00:00 - add ok"

# Логирование в файл
@log(filename="mylog.txt")
def divide(a: int, b: int) -> float:
    return a / b

divide(10, 2)  # В файл: "2024-01-01 12:00:00 - divide ok"
divide(10, 0)  # В файл: "2024-01-01 12:00:00 - divide error: ZeroDivisionError. Inputs: (10, 0), {}"
6. Чтение JSON-файлов

from src.utils import read_json_file

# Чтение транзакций из JSON-файла
transactions = read_json_file("data/operations.json")
print(f"Загружено {len(transactions)} транзакций")
7. Чтение CSV и Excel файлов

from src.file_reader import read_csv_file, read_excel_file

# Чтение из CSV
csv_transactions = read_csv_file("data/transactions.csv")
print(f"Загружено {len(csv_transactions)} транзакций из CSV")

# Чтение из Excel
excel_transactions = read_excel_file("data/transactions_excel.xlsx")
print(f"Загружено {len(excel_transactions)} транзакций из Excel")
8. Конвертация валют

from src.external_api import convert_to_rubles

# Конвертация суммы в рубли
transaction_usd = {
    "operationAmount": {
        "amount": "100.00",
        "currency": {"code": "USD"}
    }
}
amount_rub = convert_to_rubles(transaction_usd)
9. Поиск транзакций по описанию

from src.search_utils import search_transactions

# Поиск транзакций, содержащих слово "Перевод"
found = search_transactions(transactions, "Перевод")
print(f"Найдено {len(found)} транзакций")
10. Подсчёт операций по категориям

from src.category_utils import count_transactions_by_category

categories = ["Перевод организации", "Перевод с карты на карту", "Открытие вклада"]
counts = count_transactions_by_category(transactions, categories)
for category, count in counts.items():
    print(f"{category}: {count}")
11. Интерактивный режим (main.py)

poetry run python main.py
Программа предоставляет меню для:

Выбора источника данных (JSON, CSV, XLSX)

Фильтрации по статусу

Сортировки по дате

Фильтрации рублевых транзакций

Поиска по описанию

Логирование
В проекте реализовано логирование для модулей masks и utils с использованием библиотеки logging.

Настройка логов
Логи записываются в папку logs/ в корне проекта:

logs/masks.log — логи для модуля masks

logs/utils.log — логи для модуля utils

Формат логов

2024-03-26 19:30:00 - masks - DEBUG - Processing card number: 7000...6361
2024-03-26 19:30:00 - masks - INFO - Successfully masked card number: 7000 79** **** 6361
2024-03-26 19:30:01 - utils - ERROR - JSON decode error in data/operations.json
Тестирование
Запуск тестов

# Запуск всех тестов
poetry run pytest

# Запуск с подробным выводом
poetry run pytest -v

# Запуск конкретного тестового файла
poetry run pytest tests/test_search_utils.py -v
Покрытие кода

# Запуск с измерением покрытия
poetry run pytest --cov=src tests/

# Генерация HTML-отчета
poetry run pytest --cov=src --cov-report=html tests/
Результаты тестирования
✅ 80 тестов успешно проходят

✅ Покрытие кода > 80%

✅ Все функции протестированы

Покрытие по модулям

Name                 Stmts   Miss  Cover
----------------------------------------
src/masks.py            18      0   100%
src/processing.py       12      0   100%
src/widget.py           18      0   100%
src/generators.py       20      0   100%
src/decorators.py       20      0   100%
src/utils.py            12      0   100%
src/external_api.py     20      0   100%
src/logger_config.py    20      0   100%
src/file_reader.py      15      0   100%
src/search_utils.py     10      0   100%
src/category_utils.py   12      0   100%
----------------------------------------
TOTAL                  177      0   100%
Линтинг и форматирование

# Проверка стиля
poetry run flake8 src/ tests/

# Форматирование
poetry run black src/ tests/
poetry run isort src/ tests/

# Проверка типов
poetry run mypy src/
Требования к окружению
Python: 3.14 или выше

Poetry: 1.4.0 или выше

Зависимости: pandas, openpyxl, requests, python-dotenv

Разработка
Проект использует GitFlow:

main - стабильная версия

develop - основная ветка разработки

feature/* - ветки для новой функциональности

Автор
Студент курса Python-разработки

Лицензия
Проект создан в учебных целях.