"""
Module for logging configuration.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional


def setup_logger(module_name: str, log_file: Optional[str] = None) -> logging.Logger:
    """
    Setup logger for a module.

    Args:
        module_name: Name of the module (e.g., 'masks', 'utils')
        log_file: Path to log file (default: logs/{module_name}.log)

    Returns:
        Configured logger instance
    """
    # Create logs directory if not exists
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Set log file path
    if log_file is None:
        log_file = os.path.join(log_dir, f"{module_name}.log")

    # Create logger
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    # Remove existing handlers to avoid duplicates
    if logger.handlers:
        logger.handlers.clear()

    # Create file handler
    file_handler = RotatingFileHandler(log_file, mode="w", maxBytes=10485760, backupCount=5, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(file_handler)

    return logger
