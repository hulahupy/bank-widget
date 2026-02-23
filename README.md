# Банковский виджет операций

Проект для маскировки и обработки банковских операций клиента.

## Описание

Проект предоставляет набор функций для:
- Маскировки номеров банковских карт и счетов
- Обработки информации о банковских операциях
- Фильтрации и сортировки операций по различным критериям

## Установка

```bash
# Клонировать репозиторий
git clone https://github.com/your-username/bank-widget.git
cd bank-widget

# Установить зависимости через Poetry
poetry install
poetry install --only lint
```
## Использование

### Маскировка карт и счетов
```python
from src.masks import get_mask_card_number, get_mask_account
from src.widget import mask_account_card, get_date

# Маскировка номера карты
print(get_mask_card_number("7000792289606361"))  # "7000 79** **** 6361"

# Маскировка номера счета
print(get_mask_account("73654108430135874305"))  # "**4305"

# Универсальная функция для карт и счетов
print(mask_account_card("Visa Platinum 7000792289606361"))  # "Visa Platinum 7000 79** **** 6361"
print(mask_account_card("Счет 73654108430135874305"))  # "Счет **4305"

# Форматирование даты
print(get_date("2024-03-11T02:26:18.671407"))  # "11.03.2024"
```
## Лицензия

Проект создан в учебных целях.