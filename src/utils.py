"""
Module for utility functions.
"""

import json
import os
from typing import Any, Dict, List


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Read JSON file and return list of transactions.

    Args:
        file_path: Path to JSON file

    Returns:
        List of dictionaries with transaction data.
        Returns empty list if file not found, empty, or not containing a list.

    Examples:
        >>> transactions = read_json_file("data/operations.json")
        >>> len(transactions)
        5
    """
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data
        return []

    except (json.JSONDecodeError, IOError):
        return []
