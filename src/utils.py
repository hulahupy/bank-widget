"""
Module for utility functions.
"""

import json
import os
from typing import Any, Dict, List

from src.logger_config import setup_logger

# Setup logger for utils module
logger = setup_logger("utils")


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
    logger.debug(f"Attempting to read JSON file: {file_path}")

    if not os.path.exists(file_path):
        logger.warning(f"File not found: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.debug(f"Successfully loaded JSON data from {file_path}")

        if isinstance(data, list):
            logger.info(f"Successfully read {len(data)} transactions from {file_path}")
            return data
        else:
            logger.warning(f"JSON file {file_path} does not contain a list (type: {type(data).__name__})")
            return []

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in {file_path}: {e}")
        return []
    except IOError as e:
        logger.error(f"IO error reading {file_path}: {e}")
        return []
