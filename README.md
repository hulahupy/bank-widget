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

## Структура проекта
mask_card_number_9_2/
├── src/ # Исходный код
│ ├── masks.py # Маскировка карт и счетов
│ ├── widget.py # Функции для виджета
│ ├── processing.py # Обработка списков операций
│ ├── generators.py # Генераторы для транзакций
│ └── decorators.py # Декораторы для логирования
├── tests/ # Тесты
│ ├── conftest.py # Общие фикстуры для тестов
│ ├── test_masks.py
│ ├── test_widget.py
│ ├── test_processing.py
│ ├── test_generators.py
│ └── test_decorators.py
├── htmlcov/ # Отчет о покрытии (генерируется автоматически)
├── main.py # Демонстрация работы
├── pyproject.toml # Конфигурация Poetry и линтеров
├── poetry.lock # Зафиксированные версии зависимостей
├── .flake8 # Конфигурация Flake8
└── README.md # Документация


## Установка и настройка

### Предварительные требования
- Python 3.14 или выше
- Poetry (менеджер зависимостей)

### Установка


# Клонировать репозиторий
git clone https://github.com/your-username/bank-widget.git
cd bank-widget

# Установить зависимости через Poetry
poetry install
poetry install --only lint
poetry install --only test
Использование
1. Маскировка номеров карт и счетов
python
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
python
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
python
from src.processing import filter_by_state, sort_by_date

# Исходные данные
operations = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

# Фильтрация по статусу EXECUTED (по умолчанию)
executed_operations = filter_by_state(operations)
print("EXECUTED:", executed_operations)

# Фильтрация по статусу CANCELED
canceled_operations = filter_by_state(operations, 'CANCELED')
print("CANCELED:", canceled_operations)

# Сортировка по дате (по убыванию - сначала новые)
sorted_desc = sort_by_date(operations)
print("По убыванию:", sorted_desc)

# Сортировка по дате (по возрастанию - сначала старые)
sorted_asc = sort_by_date(operations, descending=False)
print("По возрастанию:", sorted_asc)
4. Генераторы для работы с транзакциями
Фильтрация по валюте (filter_by_currency)
Генератор, который фильтрует транзакции по заданной валюте и возвращает итератор.

from src.generators import filter_by_currency

# Пример данных
transactions = [
    {"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
    {"id": 2, "operationAmount": {"currency": {"code": "RUB"}}},
    {"id": 3, "operationAmount": {"currency": {"code": "USD"}}}
]

# Получить все USD-транзакции
usd_transactions = list(filter_by_currency(transactions, "USD"))
print(len(usd_transactions))  # 2

# Использование как итератора
usd_iter = filter_by_currency(transactions, "USD")
print(next(usd_iter))  # первая USD-транзакция
print(next(usd_iter))  # вторая USD-транзакция
Описания транзакций (transaction_descriptions)
Генератор, который возвращает описания всех транзакций по очереди.

from src.generators import transaction_descriptions

transactions = [
    {"description": "Перевод организации"},
    {"description": "Перевод со счета на счет"},
    {"description": "Перевод с карты на карту"}
]

for desc in transaction_descriptions(transactions):
    print(desc)
# Перевод организации
# Перевод со счета на счет
# Перевод с карты на карту

# Можно также преобразовать в список
descriptions = list(transaction_descriptions(transactions))
print(descriptions)  # ['Перевод организации', 'Перевод со счета на счет', 'Перевод с карты на карту']
Генератор номеров карт (card_number_generator)
Генератор, который создает номера банковских карт в заданном диапазоне в формате XXXX XXXX XXXX XXXX.

from src.generators import card_number_generator

# Сгенерировать номера карт с 1 по 5
for card in card_number_generator(1, 5):
    print(card)


# Сгенерировать один номер
cards = list(card_number_generator(999, 999))
print(cards[0])  # 0000 0000 0000 0999

# Работа с большими числами
for card in card_number_generator(9999999999999995, 9999999999999997):
    print(card)

5. Декоратор логирования (log)
Декоратор log автоматически логирует вызовы функций, их результаты и ошибки.

from src.decorators import log

# Логирование в консоль (по умолчанию)
@log()
def add(a: int, b: int) -> int:
    return a + b

add(2, 3)  # В консоль выведется: "2024-01-01 12:00:00 - add ok"

# Логирование в файл
@log(filename="mylog.txt")
def divide(a: int, b: int) -> float:
    return a / b

divide(10, 2)  # В файл запишется: "2024-01-01 12:00:00 - divide ok"
divide(10, 0)  # В файл запишется: "2024-01-01 12:00:00 - divide error: ZeroDivisionError. Inputs: (10, 0), {}"
Параметры декоратора:
filename (необязательный) - имя файла для записи логов. Если не указан, логи выводятся в консоль.

Формат логов:
Успех: {timestamp} - {func_name} ok

Ошибка: {timestamp} - {func_name} error: {error_type}. Inputs: {args}, {kwargs}

Тестирование
Запуск тестов

# Запуск всех тестов
poetry run pytest

# Запуск с подробным выводом
poetry run pytest -v

# Запуск конкретного тестового файла
poetry run pytest tests/test_decorators.py -v
Покрытие кода

# Запуск с измерением покрытия
poetry run pytest --cov=src tests/

# Генерация HTML-отчета о покрытии
poetry run pytest --cov=src --cov-report=html tests/

# Открыть отчет в браузере (Windows)
start htmlcov/index.html

# Открыть отчет в браузере (Mac/Linux)
open htmlcov/index.html
Фикстуры и параметризация
В проекте используются современные подходы к тестированию:

Фикстуры (conftest.py)
Общие фикстуры вынесены в файл tests/conftest.py:

sample_operations - тестовые данные для обработки операций

sample_transactions - тестовые данные для генераторов

sample_card_numbers - примеры номеров карт

sample_account_numbers - примеры номеров счетов

sample_dates - примеры дат для тестирования

Специальные фикстуры для декораторов:
capsys - встроенная фикстура pytest для перехвата вывода в консоль

Пример параметризации тестов

@pytest.mark.parametrize("start,stop,expected", [
    (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
    (999, 1000, ["0000 0000 0000 0999", "0000 0000 0000 1000"]),
])
def test_card_number_generator(start, stop, expected):
    result = list(card_number_generator(start, stop))
    assert result == expected
Результаты тестирования
На данный момент в проекте:

Более 60 тестов успешно проходят

Покрытие кода > 80% (декораторы: 100%)

Все функции протестированы (маскировка, виджет, обработка, генераторы, декораторы)

Использованы фикстуры и параметризация

Покрытие по модулям
После запуска тестов с покрытием можно увидеть детальную статистику:

Name                 Stmts   Miss  Cover
----------------------------------------
src/masks.py            15      0   100%
src/processing.py       12      0   100%
src/widget.py           18      0   100%
src/generators.py       20      0   100%
src/decorators.py       25      0   100%
----------------------------------------
TOTAL                   90      0   100%
Линтинг и форматирование
Проверка стиля (Flake8)

poetry run flake8 src/ tests/ main.py
Форматирование (Black)

# Проверка форматирования
poetry run black --check src/ tests/ main.py

# Применение форматирования
poetry run black src/ tests/ main.py
Сортировка импортов (isort)

# Проверка сортировки
poetry run isort --check-only src/ tests/ main.py

# Применение сортировки
poetry run isort src/ tests/ main.py
Проверка типов (MyPy)

poetry run mypy src/ tests/ main.py
Требования к окружению
Python: 3.14 или выше

Poetry: 1.4.0 или выше

Зависимости:

flake8 - линтер

black - форматер

isort - сортировка импортов

mypy - проверка типов

pytest - тестирование

pytest-cov - измерение покрытия

Разработка
GitFlow
Проект использует GitFlow:

main - стабильная версия

develop - основная ветка разработки

feature/* - ветки для новой функциональности

Создание новой функциональности

# Создать feature-ветку от develop
git checkout develop
git pull origin develop
git checkout -b feature/new-functionality

# Внести изменения
git add .
git commit -m "feat: add new functionality"

# Запушить на GitHub
git push origin feature/new-functionality

# Создать Pull Request в ветку develop
Автор
Студент курса Python-разработки

Лицензия
Проект создан в учебных целях.