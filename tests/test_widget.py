"""Тесты для модуля widget."""

import pytest

from src.widget import get_date, mask_account_card


def test_mask_account_card_visa() -> None:
    """Тестирует маскировку Visa Platinum."""
    result = mask_account_card("Visa Platinum 7000792289606361")
    assert result == "Visa Platinum 7000 79** **** 6361"


def test_mask_account_card_maestro() -> None:
    """Тестирует маскировку Maestro."""
    result = mask_account_card("Maestro 1596837868705199")
    assert result == "Maestro 1596 83** **** 5199"


def test_mask_account_card_mastercard() -> None:
    """Тестирует маскировку MasterCard."""
    result = mask_account_card("MasterCard 7158300734726758")
    assert result == "MasterCard 7158 30** **** 6758"


def test_mask_account_card_account() -> None:
    """Тестирует маскировку счета."""
    result = mask_account_card("Счет 73654108430135874305")
    assert result == "Счет **4305"


def test_mask_account_card_account_with_number() -> None:
    """Тестирует маскировку счета с номером."""
    result = mask_account_card("Счет 35383033474447895560")
    assert result == "Счет **5560"


def test_get_date() -> None:
    """Тестирует преобразование даты."""
    result = get_date("2024-03-11T02:26:18.671407")
    assert result == "11.03.2024"


def test_get_date_new_year() -> None:
    """Тестирует преобразование даты на новый год."""
    result = get_date("2025-01-01T00:00:00.000000")
    assert result == "01.01.2025"


def test_mask_account_card_invalid_format() -> None:
    """Тестирует обработку неверного формата."""
    with pytest.raises(ValueError):
        mask_account_card("НеправильныйФормат")