"""
Module with generators for processing bank transactions.
"""

from typing import Any, Dict, Generator, List


def filter_by_currency(
    transactions: List[Dict[str, Any]], currency: str = "USD"
) -> Generator[Dict[str, Any], None, None]:
    """
    Filter transactions by currency and return iterator.

    Args:
        transactions: List of transaction dictionaries
        currency: Currency code to filter by (default: "USD")

    Returns:
        Iterator yielding transactions with specified currency

    Yields:
        Transaction dictionary where operation currency matches specified currency

    Examples:
        >>> transactions = [
        ...     {"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
        ...     {"id": 2, "operationAmount": {"currency": {"code": "RUB"}}}
        ... ]
        >>> usd_transactions = list(filter_by_currency(transactions, "USD"))
        >>> len(usd_transactions)
        1
    """
    for transaction in transactions:
        try:
            currency_code = transaction["operationAmount"]["currency"]["code"]
            if currency_code == currency:
                yield transaction
        except (KeyError, TypeError):
            continue


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """
    Generator that yields description of each transaction.

    Args:
        transactions: List of transaction dictionaries

    Returns:
        Generator yielding transaction descriptions

    Yields:
        Description string of each transaction

    Examples:
        >>> transactions = [
        ...     {"description": "Перевод организации"},
        ...     {"description": "Перевод со счета на счет"}
        ... ]
        >>> descriptions = list(transaction_descriptions(transactions))
        >>> len(descriptions)
        2
    """
    for transaction in transactions:
        try:
            yield transaction["description"]
        except KeyError:
            continue


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """
    Generate bank card numbers in format XXXX XXXX XXXX XXXX.

    Args:
        start: Starting number (1-9999999999999999)
        stop: Ending number (inclusive)

    Returns:
        Generator yielding formatted card numbers

    Yields:
        Formatted card number string

    Examples:
        >>> for card in card_number_generator(1, 3):
        ...     print(card)
        0000 0000 0000 0001
        0000 0000 0000 0002
        0000 0000 0000 0003
    """
    for number in range(start, stop + 1):
        card_str = str(number).zfill(16)
        formatted = f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"
        yield formatted
