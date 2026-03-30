"""
Tests for logging functionality.
"""

import os
import tempfile
from unittest.mock import patch

import pytest

from src.logger_config import setup_logger
from src.masks import get_mask_card_number
from src.utils import read_json_file


def test_masks_logger_success() -> None:
    """Test masks module logging on success."""
    # Временный файл для логов
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".log", delete=False) as tmp:
        log_file = tmp.name

    try:
        with patch("src.masks.logger.handlers", []):
            # Создаем новый логгер с временным файлом
            test_logger = setup_logger("masks", log_file)

            with patch("src.masks.logger", test_logger):
                result = get_mask_card_number("7000792289606361")
                assert result == "7000 79** **** 6361"

                # Проверяем, что лог записан
                with open(log_file, "r", encoding="utf-8") as f:
                    log_content = f.read()
                    assert "Processing card number: 7000...6361" in log_content
                    assert "Successfully masked card number: 7000 79** **** 6361" in log_content
    finally:
        if os.path.exists(log_file):
            os.unlink(log_file)


def test_masks_logger_error() -> None:
    """Test masks module logging on error."""
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".log", delete=False) as tmp:
        log_file = tmp.name

    try:
        with patch("src.masks.logger.handlers", []):
            test_logger = setup_logger("masks", log_file)

            with patch("src.masks.logger", test_logger):
                with pytest.raises(ValueError):
                    get_mask_card_number("12345")

                # Проверяем, что ошибка залогирована
                with open(log_file, "r", encoding="utf-8") as f:
                    log_content = f.read()
                    assert "Invalid card number length: 5 (expected 16)" in log_content
                    assert "ERROR" in log_content
    finally:
        if os.path.exists(log_file):
            os.unlink(log_file)


def test_utils_logger_success() -> None:
    """Test utils module logging on success."""
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as tmp_json:
        tmp_json.write('[{"id": 1, "amount": 100}]')
        json_path = tmp_json.name

    with tempfile.NamedTemporaryFile(mode="w+", suffix=".log", delete=False) as tmp_log:
        log_file = tmp_log.name

    try:
        with patch("src.utils.logger.handlers", []):
            test_logger = setup_logger("utils", log_file)

            with patch("src.utils.logger", test_logger):
                result = read_json_file(json_path)
                assert len(result) == 1

                # Проверяем, что лог записан
                with open(log_file, "r", encoding="utf-8") as f:
                    log_content = f.read()
                    assert "Successfully read 1 transactions" in log_content
    finally:
        if os.path.exists(json_path):
            os.unlink(json_path)
        if os.path.exists(log_file):
            os.unlink(log_file)


def test_utils_logger_file_not_found() -> None:
    """Test utils module logging when file not found."""
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".log", delete=False) as tmp:
        log_file = tmp.name

    try:
        with patch("src.utils.logger.handlers", []):
            test_logger = setup_logger("utils", log_file)

            with patch("src.utils.logger", test_logger):
                result = read_json_file("nonexistent.json")
                assert result == []

                # Проверяем, что предупреждение залогировано
                with open(log_file, "r", encoding="utf-8") as f:
                    log_content = f.read()
                    assert "File not found: nonexistent.json" in log_content
                    assert "WARNING" in log_content
    finally:
        if os.path.exists(log_file):
            os.unlink(log_file)


def test_utils_logger_invalid_json() -> None:
    """Test utils module logging on invalid JSON."""
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as tmp_json:
        tmp_json.write("{invalid json}")
        json_path = tmp_json.name

    with tempfile.NamedTemporaryFile(mode="w+", suffix=".log", delete=False) as tmp_log:
        log_file = tmp_log.name

    try:
        with patch("src.utils.logger.handlers", []):
            test_logger = setup_logger("utils", log_file)

            with patch("src.utils.logger", test_logger):
                result = read_json_file(json_path)
                assert result == []

                # Проверяем, что ошибка залогирована
                with open(log_file, "r", encoding="utf-8") as f:
                    log_content = f.read()
                    assert "JSON decode error" in log_content
                    assert "ERROR" in log_content
    finally:
        if os.path.exists(json_path):
            os.unlink(json_path)
        if os.path.exists(log_file):
            os.unlink(log_file)
