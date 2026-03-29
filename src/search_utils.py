"""
Module for searching transactions using regular expressions.
"""

import re
from typing import Any, Dict, List


def search_transactions(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """
    Search transactions by description using regular expression.

    Args:
        transactions: List of transaction dictionaries
        search_string: String to search in description

    Returns:
        List of transactions where description contains the search string

    Examples:
        >>> data = [{"description": "Перевод организации"}, {"description": "Перевод со счета"}]
        >>> search_transactions(data, "организации")
        [{"description": "Перевод организации"}]
    """
    if not transactions or not search_string:
        return []

    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    result = []

    for transaction in transactions:
        description = transaction.get("description", "")
        if pattern.search(str(description)):
            result.append(transaction)

    return result
