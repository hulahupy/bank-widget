"""Tests for processing module."""

import pytest
from src.processing import filter_by_state, sort_by_date


def test_filter_by_state_default(sample_operations):
    """Test filtering with default state EXECUTED."""
    result = filter_by_state(sample_operations)
    assert len(result) == 2
    assert all(item['state'] == 'EXECUTED' for item in result)


def test_filter_by_state_canceled(sample_operations):
    """Test filtering with CANCELED state."""
    result = filter_by_state(sample_operations, 'CANCELED')
    assert len(result) == 2
    assert all(item['state'] == 'CANCELED' for item in result)


def test_filter_by_state_no_matches(sample_operations):
    """Test filtering with non-existent state."""
    result = filter_by_state(sample_operations, 'NONEXISTENT')
    assert result == []


def test_filter_by_state_empty_list():
    """Test filtering empty list."""
    assert filter_by_state([]) == []


@pytest.mark.parametrize("descending, expected_first, expected_last", [
    (True, 41428829, 939719570),  # descending: newest first
    (False, 939719570, 41428829),  # ascending: oldest first
])
def test_sort_by_date_order(sample_operations, descending, expected_first, expected_last):
    """Test sorting by date in different orders."""
    result = sort_by_date(sample_operations, descending)
    assert result[0]['id'] == expected_first
    assert result[-1]['id'] == expected_last


def test_sort_by_date_same_date(operations_with_same_date):
    """Test sorting when dates are the same."""
    result = sort_by_date(operations_with_same_date, descending=True)
    # Should maintain relative order for same dates
    assert result[0]['id'] == 2  # newest time
    assert result[1]['id'] == 1
    assert result[2]['id'] == 3  # oldest time


def test_sort_by_date_empty_list():
    """Test sorting empty list."""
    assert sort_by_date([]) == []


def test_sort_by_date_invalid_dates():
    """Test sorting with invalid dates."""
    invalid_data = [
        {'id': 1, 'date': 'invalid'},
        {'id': 2, 'date': '2023-01-01'},
        {'id': 3},  # missing date
    ]
    # Should handle gracefully - invalid dates go to end
    result = sort_by_date(invalid_data)
    assert result[-1]['id'] in [1, 3]  # invalid dates at end
