"""Модуль для маскировки номеров банковских карт и счетов."""


def get_mask_card_number(card_number: int | str) -> str:
    """
    Маскирует номер банковской карты, показывая только первые 6 и последние 4 цифры.

    Аргументы:
        card_number (int | str): Номер карты в виде целого числа или строки

    Возвращает:
        str: Замаскированный номер карты в формате 'XXXX XX** **** XXXX'

    Примеры:
        >>> get_mask_card_number(7000792289606361)
        '7000 79** **** 6361'
        >>> get_mask_card_number("7000792289606361")
        '7000 79** **** 6361'

    Исключения:
        ValueError: Если номер карты не содержит 16 цифр
    """
    card_str = str(card_number)

    if len(card_str) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    return f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"


def get_mask_account(account_number: int | str) -> str:
    """
    Маскирует номер банковского счета, показывая только последние 4 цифры.

    Аргументы:
        account_number (int | str): Номер счета в виде целого числа или строки

    Возвращает:
        str: Замаскированный номер счета в формате '**XXXX'

    Примеры:
        >>> get_mask_account(73654108430135874305)
        '**4305'
        >>> get_mask_account("73654108430135874305")
        '**4305'

    Исключения:
        ValueError: Если номер счета содержит менее 4 цифр
    """
    account_str = str(account_number)

    if len(account_str) < 4:
        raise ValueError("Номер счета должен содержать минимум 4 цифры")

    return f"**{account_str[-4:]}"
