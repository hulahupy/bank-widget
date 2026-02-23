"""Tests for processing module."""

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_operations() -> list:
    """Fixture with sample operations data for tests."""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


def test_filter_by_state_default(sample_operations: list) -> None:
    """Test filtering with default state (EXECUTED)."""
    result = filter_by_state(sample_operations)
    assert len(result) == 2
    assert all(op["state"] == "EXECUTED" for op in result)
    assert result[0]["id"] == 41428829
    assert result[1]["id"] == 939719570


def test_filter_by_state_canceled(sample_operations: list) -> None:
    """Test filtering with CANCELED state."""
    result = filter_by_state(sample_operations, "CANCELED")
    assert len(result) == 2
    assert all(op["state"] == "CANCELED" for op in result)
    assert result[0]["id"] == 594226727
    assert result[1]["id"] == 615064591


def test_sort_by_date_descending(sample_operations: list) -> None:
    """Test sorting by date in descending order (newest first)."""
    result = sort_by_date(sample_operations)
    assert result[0]["id"] == 41428829  # 2019
    assert result[1]["id"] == 615064591  # 2018-10
    assert result[2]["id"] == 594226727  # 2018-09
    assert result[3]["id"] == 939719570  # 2018-06


def test_sort_by_date_ascending(sample_operations: list) -> None:
    """Test sorting by date in ascending order (oldest first)."""
    result = sort_by_date(sample_operations, descending=False)
    assert result[0]["id"] == 939719570  # 2018-06
    assert result[1]["id"] == 594226727  # 2018-09
    assert result[2]["id"] == 615064591  # 2018-10
    assert result[3]["id"] == 41428829  # 2019
