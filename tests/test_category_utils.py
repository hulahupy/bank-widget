"""
Tests for category_utils module.
"""

from src.category_utils import count_transactions_by_category


def test_count_transactions_by_category() -> None:
    """Test counting transactions by categories."""
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Перевод со счета на счет"},
        {"description": "Оплата услуг"},
    ]
    categories = ["Перевод организации", "Перевод со счета на счет", "Оплата услуг"]
    result = count_transactions_by_category(transactions, categories)
    assert result["Перевод организации"] == 2
    assert result["Перевод со счета на счет"] == 1
    assert result["Оплата услуг"] == 1


def test_count_transactions_by_category_empty_list() -> None:
    """Test counting with empty transactions list."""
    categories = ["Перевод организации", "Оплата услуг"]
    result = count_transactions_by_category([], categories)
    assert result == {"Перевод организации": 0, "Оплата услуг": 0}


def test_count_transactions_by_category_empty_categories() -> None:
    """Test counting with empty categories list."""
    transactions = [{"description": "Перевод организации"}]
    result = count_transactions_by_category(transactions, [])
    assert result == {}


def test_count_transactions_by_category_case_insensitive() -> None:
    """Test case-insensitive counting."""
    transactions = [{"description": "перевод организации"}]
    categories = ["Перевод организации"]
    result = count_transactions_by_category(transactions, categories)
    assert result["Перевод организации"] == 1


def test_count_transactions_by_category_missing_description() -> None:
    """Test counting with missing description field."""
    transactions = [{"id": 1}, {"description": "Перевод организации"}]
    categories = ["Перевод организации", "Оплата"]
    result = count_transactions_by_category(transactions, categories)
    assert result["Перевод организации"] == 1
    assert result["Оплата"] == 0
