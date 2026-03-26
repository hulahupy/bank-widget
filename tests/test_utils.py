"""
Tests for utils module.
"""

import json
import os
import tempfile
from typing import Any, Dict, List

from src.utils import read_json_file


def test_read_json_file_valid() -> None:
    """Test reading valid JSON file."""
    test_data: List[Dict[str, Any]] = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]

    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as tmp:
        json.dump(test_data, tmp)
        tmp_path = tmp.name

    try:
        result = read_json_file(tmp_path)
        assert result == test_data
    finally:
        os.unlink(tmp_path)


def test_read_json_file_empty() -> None:
    """Test reading empty JSON file."""
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as tmp:
        tmp.write("")
        tmp_path = tmp.name

    try:
        result = read_json_file(tmp_path)
        assert result == []
    finally:
        os.unlink(tmp_path)


def test_read_json_file_not_list() -> None:
    """Test reading JSON file with non-list data."""
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as tmp:
        json.dump({"key": "value"}, tmp)
        tmp_path = tmp.name

    try:
        result = read_json_file(tmp_path)
        assert result == []
    finally:
        os.unlink(tmp_path)


def test_read_json_file_not_found() -> None:
    """Test reading non-existent JSON file."""
    result = read_json_file("nonexistent.json")
    assert result == []


def test_read_json_file_invalid_json() -> None:
    """Test reading invalid JSON file."""
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as tmp:
        tmp.write("{invalid json}")
        tmp_path = tmp.name

    try:
        result = read_json_file(tmp_path)
        assert result == []
    finally:
        os.unlink(tmp_path)
