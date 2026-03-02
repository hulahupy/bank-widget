"""Tests for masks module."""

import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "input_card, expected",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("5555555555554444", "5555 55** **** 4444"),
        (7000792289606361, "7000 79** **** 6361"),
    ],
)
def test_get_mask_card_number_valid(input_card, expected):
    """Test card number masking with valid inputs."""
    assert get_mask_card_number(input_card) == expected


@pytest.mark.parametrize(
    "invalid_card",
    [
        "12345",  # too short
        "12345678901234567",  # too long
        "abcd123456789012",  # non-digit chars
        "",  # empty string
    ],
)
def test_get_mask_card_number_invalid(invalid_card):
    """Test card number masking with invalid inputs."""
    with pytest.raises(ValueError):
        get_mask_card_number(invalid_card)


@pytest.mark.parametrize(
    "input_account, expected",
    [
        ("73654108430135874305", "**4305"),
        ("1234567890", "**7890"),
        ("40817810500000000001", "**0001"),
        (73654108430135874305, "**4305"),
    ],
)
def test_get_mask_account_valid(input_account, expected):
    """Test account number masking with valid inputs."""
    assert get_mask_account(input_account) == expected


@pytest.mark.parametrize(
    "invalid_account",
    [
        "123",  # too short
        "abcd1234",  # non-digit chars
        "",  # empty string
    ],
)
def test_get_mask_account_invalid(invalid_account):
    """Test account number masking with invalid inputs."""
    with pytest.raises(ValueError):
        get_mask_account(invalid_account)
