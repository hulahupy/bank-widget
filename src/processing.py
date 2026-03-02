"""Module for processing bank operations."""

from typing import Any, Dict, List


def filter_by_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Filter list of operations by given state.

    Args:
        operations: List of dictionaries with bank operations data
        state: State to filter by (default 'EXECUTED')

    Returns:
        New list containing only operations with specified state
    """
    return [op for op in operations if op.get("state") == state]


def sort_by_date(operations: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """
    Sort list of operations by date.

    Args:
        operations: List of dictionaries with bank operations data
        descending: Sort order. True - descending (newest first), False - ascending

    Returns:
        New sorted list
    """
    return sorted(operations, key=lambda x: x.get("date", ""), reverse=descending)
