"""
Module for reading financial transactions from CSV and Excel files.
"""

from typing import Any, Dict, List
from zipfile import BadZipFile

import pandas as pd


def read_csv_file(file_path: str) -> List[Dict[Any, Any]]:
    """
    Read financial transactions from CSV file.

    Args:
        file_path: Path to CSV file

    Returns:
        List of dictionaries with transaction data.
        Returns empty list if file not found or empty.

    Examples:
        >>> transactions = read_csv_file("data/transactions.csv")
        >>> len(transactions)
        100
    """
    try:
        df = pd.read_csv(file_path, sep=";", encoding="utf-8")
    except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError):
        return []

    if df.empty:
        return []

    return df.to_dict(orient="records")


def read_excel_file(file_path: str) -> List[Dict[Any, Any]]:
    """
    Read financial transactions from Excel file.

    Args:
        file_path: Path to Excel file (.xlsx)

    Returns:
        List of dictionaries with transaction data.
        Returns empty list if file not found or empty.

    Examples:
        >>> transactions = read_excel_file("data/transactions_excel.xlsx")
        >>> len(transactions)
        100
    """
    try:
        df = pd.read_excel(file_path, engine="openpyxl")
    except (FileNotFoundError, ValueError, OSError, BadZipFile):
        return []

    if df.empty:
        return []

    return df.to_dict(orient="records")
