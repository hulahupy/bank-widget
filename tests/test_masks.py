"""Тесты для функций маскировки."""

import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number() -> None:
    """Тестирует маскировку номера карты."""
    # Проверка с числом
    assert get_mask_card_number(7000792289606361) == "7000 79** **** 6361"
    # Проверка со строкой
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"


def test_get_mask_account() -> None:
    """Тестирует маскировку номера счета."""
    # Проверка с числом
    assert get_mask_account(73654108430135874305) == "**4305"
    # Проверка со строкой
    assert get_mask_account("73654108430135874305") == "**4305"


def test_get_mask_card_number_invalid_length() -> None:
    """Тестирует обработку неверной длины номера карты."""
    with pytest.raises(ValueError):
        get_mask_card_number("12345")  # Слишком короткий номер


def test_get_mask_account_invalid_length() -> None:
    """Тестирует обработку неверной длины номера счета."""
    with pytest.raises(ValueError):
        get_mask_account("123")  # Слишком короткий номер
