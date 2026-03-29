"""
Main module for bank transactions widget.
"""
from typing import Any, Dict, List

from src.category_utils import count_transactions_by_category
from src.file_reader import read_csv_file, read_excel_file
from src.processing import filter_by_state, sort_by_date
from src.search_utils import search_transactions
from src.utils import read_json_file
from src.widget import get_date, mask_account_card


def get_valid_status() -> str:
    """
    Get valid status from user input.
    """
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = input("\nВведите статус, по которому необходимо выполнить фильтрацию.\n"
                       "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n").strip().upper()
        if status in valid_statuses:
            print(f"Операции отфильтрованы по статусу \"{status}\"")
            return status
        print(f"Статус операции \"{status}\" недоступен.")


def get_sort_choice() -> bool:
    """
    Get sort choice from user.
    Returns True for descending (newest first), False for ascending.
    """
    while True:
        choice = input("\nОтсортировать операции по дате? Да/Нет\n").strip().lower()
        if choice in ["да", "нет"]:
            if choice == "нет":
                return None
            break
        print("Пожалуйста, введите 'Да' или 'Нет'")

    while True:
        order = input("\nОтсортировать по возрастанию или по убыванию?\n").strip().lower()
        if order in ["по возрастанию", "по убыванию"]:
            return order == "по убыванию"
        print("Пожалуйста, введите 'по возрастанию' или 'по убыванию'")


def get_ruble_filter() -> bool:
    """
    Get ruble filter choice from user.
    """
    while True:
        choice = input("\nВыводить только рублевые транзакции? Да/Нет\n").strip().lower()
        if choice in ["да", "нет"]:
            return choice == "да"
        print("Пожалуйста, введите 'Да' или 'Нет'")


def get_search_filter() -> str:
    """
    Get search filter from user.
    Returns search string or None.
    """
    while True:
        choice = input("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет\n").strip().lower()
        if choice in ["да", "нет"]:
            if choice == "нет":
                return None
            break
        print("Пожалуйста, введите 'Да' или 'Нет'")

    search_string = input("\nВведите слово для поиска в описании:\n").strip()
    return search_string if search_string else None


def filter_by_currency(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter transactions to show only RUB transactions if user wants.
    """
    rub_only = get_ruble_filter()
    if not rub_only:
        return transactions

    result = []
    for transaction in transactions:
        currency = transaction.get("operationAmount", {}).get("currency", {}).get("code", "")
        if currency == "RUB":
            result.append(transaction)
    return result


def print_transactions(transactions: List[Dict[str, Any]]) -> None:
    """
    Print transactions in a formatted way.
    """
    if not transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nВсего банковских операций в выборке: {len(transactions)}")
    print("-" * 50)

    for transaction in transactions:
        date = get_date(transaction.get("date", ""))
        description = transaction.get("description", "Нет описания")

        # Mask from and to accounts
        from_account = transaction.get("from", "")
        to_account = transaction.get("to", "")

        from_masked = mask_account_card(from_account) if from_account else "Нет данных"
        to_masked = mask_account_card(to_account) if to_account else "Нет данных"

        amount = transaction.get("operationAmount", {}).get("amount", "0")
        currency = transaction.get("operationAmount", {}).get("currency", {}).get("code", "RUB")

        print(f"\n{date} {description}")
        print(f"{from_masked} -> {to_masked}")
        print(f"Сумма: {amount} {currency}")
        print("-" * 30)


def main() -> None:
    """
    Main function to run the bank transactions widget.
    """
    print("\nПривет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("\nВаш выбор: ").strip()

    transactions = []

    if choice == "1":
        print("\nДля обработки выбран JSON-файл.")
        transactions = read_json_file("data/operations.json")
    elif choice == "2":
        print("\nДля обработки выбран CSV-файл.")
        transactions = read_csv_file("data/transactions.csv")
    elif choice == "3":
        print("\nДля обработки выбран XLSX-файл.")
        transactions = read_excel_file("data/transactions_excel.xlsx")
    else:
        print("\nНеверный выбор. Завершение программы.")
        return

    if not transactions:
        print("\nНе найдено ни одной транзакции в выбранном файле.")
        return

    # Filter by status
    status = get_valid_status()
    filtered_transactions = filter_by_state(transactions, status)

    if not filtered_transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Sort by date
    sort_desc = get_sort_choice()
    if sort_desc is not None:
        filtered_transactions = sort_by_date(filtered_transactions, sort_desc)

    # Filter by RUB currency
    filtered_transactions = filter_by_currency(filtered_transactions)

    if not filtered_transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Search by description
    search_string = get_search_filter()
    if search_string:
        filtered_transactions = search_transactions(filtered_transactions, search_string)

    if not filtered_transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Print results
    print("\nРаспечатываю итоговый список транзакций...")
    print_transactions(filtered_transactions)


if __name__ == "__main__":
    main()
