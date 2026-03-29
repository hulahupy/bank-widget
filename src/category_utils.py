"""
Module for counting transactions by categories.
"""

from typing import Any, Dict, List


def count_transactions_by_category(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Count transactions by categories based on description field.

    Args:
        transactions: List of transaction dictionaries
        categories: List of category names to search for

    Returns:
        Dictionary with category names as keys and counts as values

    Examples:
        >>> data = [{"description": "Перевод организации"}, {"description": "Перевод организации"}]
        >>> count_transactions_by_category(data, ["Перевод организации"])
        {"Перевод организации": 2}
    """
    # Initialize result dictionary with zeros
    result: Dict[str, int] = {category: 0 for category in categories}

    if not transactions:
        return result

    for transaction in transactions:
        description = transaction.get("description", "")
        for category in categories:
            if category.lower() in description.lower():
                result[category] += 1

    return result
