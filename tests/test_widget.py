"""Tests for widget module."""

import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
    ],
)
def test_mask_account_card_card(input_string, expected):
    """Test card number masking in widget."""
    assert mask_account_card(input_string) == expected


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счет 35383033474447895560", "Счет **5560"),
        ("Счет 1234567890", "Счет **7890"),
    ],
)
def test_mask_account_card_account(input_string, expected):
    """Test account number masking in widget."""
    assert mask_account_card(input_string) == expected


@pytest.mark.parametrize(
    "invalid_input",
    [
        "Visa Platinum",  # no number
        "Счет",  # no number
        "",  # empty string
        "1234567890",  # no type
    ],
)
def test_mask_account_card_invalid(invalid_input):
    """Test widget function with invalid inputs."""
    with pytest.raises(ValueError):
        mask_account_card(invalid_input)


@pytest.mark.parametrize(
    "input_date, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-31T23:59:59.999999", "31.12.2023"),
        ("2025-01-01T00:00:00.000000", "01.01.2025"),
    ],
)
def test_get_date_valid(input_date, expected):
    """Test date formatting with valid inputs."""
    assert get_date(input_date) == expected


@pytest.mark.parametrize(
    "invalid_date",
    [
        "2024-03-11",  # no time part
        "11.03.2024",  # wrong format
        "",  # empty string
        "abcd",  # garbage
    ],
)
def test_get_date_invalid(invalid_date):
    """Test date formatting with invalid inputs."""
    with pytest.raises(ValueError):
        get_date(invalid_date)
