"""
Tests for masks module.
"""

import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number() -> None:
    """Test card number masking with valid inputs."""
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"
    assert get_mask_card_number(7000792289606361) == "7000 79** **** 6361"


def test_get_mask_account() -> None:
    """Test account number masking with valid inputs."""
    assert get_mask_account("73654108430135874305") == "**4305"
    assert get_mask_account(73654108430135874305) == "**4305"


def test_get_mask_card_number_invalid_length() -> None:
    """Test card number masking with invalid length."""
    with pytest.raises(ValueError):
        get_mask_card_number("12345")  # too short


def test_get_mask_account_invalid_length() -> None:
    """Test account number masking with invalid length."""
    with pytest.raises(ValueError):
        get_mask_account("123")  # too short
