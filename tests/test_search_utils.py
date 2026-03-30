"""
Tests for search_utils module.
"""

from src.search_utils import search_transactions


def test_search_transactions_found() -> None:
    """Test searching with found results."""
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Перевод со счета на счет"},
        {"description": "Оплата услуг"},
    ]
    result = search_transactions(transactions, "Перевод")
    assert len(result) == 2
    assert all("Перевод" in t["description"] for t in result)


def test_search_transactions_not_found() -> None:
    """Test searching with no results."""
    transactions = [{"description": "Перевод организации"}, {"description": "Перевод со счета на счет"}]
    result = search_transactions(transactions, "Оплата")
    assert result == []


def test_search_transactions_empty_list() -> None:
    """Test searching with empty list."""
    result = search_transactions([], "Перевод")
    assert result == []


def test_search_transactions_case_insensitive() -> None:
    """Test case-insensitive search."""
    transactions = [{"description": "перевод организации"}]
    result = search_transactions(transactions, "ПЕРЕВОД")
    assert len(result) == 1


def test_search_transactions_missing_description() -> None:
    """Test searching with missing description field."""
    transactions = [{"id": 1}, {"description": "Перевод организации"}]
    result = search_transactions(transactions, "Перевод")
    assert len(result) == 1


def test_search_transactions_empty_search_string() -> None:
    """Test searching with empty search string."""
    transactions = [{"description": "Перевод организации"}]
    result = search_transactions(transactions, "")
    assert result == []
