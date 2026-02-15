"""Главный модуль для демонстрации работы функций маскировки."""

from src.masks import get_mask_account, get_mask_card_number


def main() -> None:
    """Демонстрирует работу функций маскировки."""
    # Ввод данных от пользователя напрямую в код
    card_input = input()
    account_input = input()

    # Маскировка введенных данных
    masked_card = get_mask_card_number(card_input)
    masked_account = get_mask_account(account_input)

    # Вывод результатов
    print(masked_card)
    print(masked_account)


if __name__ == "__main__":
    main()
