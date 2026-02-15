"""Главный модуль для демонстрации работы функций маскировки."""

from src.widget import get_date, mask_account_card


def main() -> None:
    """Демонстрирует работу функций маскировки."""
    # Демонстрация функции mask_account_card
    print("=== Функция mask_account_card ===\n")

    test_cards = [
        "Visa Platinum 7000792289606361",
        "Maestro 1596837868705199",
        "MasterCard 7158300734726758",
        "Visa Classic 6831982476737658",
        "Счет 73654108430135874305",
        "Счет 35383033474447895560"
    ]

    for card in test_cards:
        result = mask_account_card(card)
        print(f"Вход:  {card}")
        print(f"Выход: {result}")
        print()

    # Демонстрация функции get_date
    print("=== Функция get_date ===\n")

    test_dates = [
        "2024-03-11T02:26:18.671407",
        "2023-12-31T23:59:59.999999",
        "2025-01-01T00:00:00.000000"
    ]

    for date in test_dates:
        result = get_date(date)
        print(f"Вход:  {date}")
        print(f"Выход: {result}")
        print()


if __name__ == "__main__":
    main()
