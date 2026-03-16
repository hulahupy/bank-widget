"""Модуль для работы с виджетом банковских операций."""

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер карты или счета в зависимости от типа.

    Аргументы:
        account_info (str): Строка с типом и номером карты или счета.
            Например: "Visa Platinum 7000792289606361" или "Счет 73654108430135874305"

    Возвращает:
        str: Строка с замаскированным номером.

    Примеры:
        >>> mask_account_card("Visa Platinum 7000792289606361")
        'Visa Platinum 7000 79** **** 6361'
        >>> mask_account_card("Счет 73654108430135874305")
        'Счет **4305'
    """
    # Разделяем строку на части
    parts = account_info.rsplit(" ", 1)

    if len(parts) != 2:
        raise ValueError("Неверный формат строки. Ожидается: 'Тип Номер'")

    account_type, account_number = parts

    # Определяем, карта это или счет
    if account_type.lower() == "счет":
        # Для счета используем маскировку счета
        masked_number = get_mask_account(account_number)
    else:
        # Для карты используем маскировку карты
        masked_number = get_mask_card_number(account_number)

    return f"{account_type} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ.

    Аргументы:
        date_string (str): Дата в формате "2024-03-11T02:26:18.671407"

    Возвращает:
        str: Дата в формате "ДД.ММ.ГГГГ"

    Примеры:
        >>> get_date("2024-03-11T02:26:18.671407")
        '11.03.2024'
    """
    # Извлекаем только дату (первые 10 символов)
    date_part = date_string[:10]

    # Разбиваем на год, месяц, день
    year, month, day = date_part.split("-")

    # Возвращаем в нужном формате
    return f"{day}.{month}.{year}"
