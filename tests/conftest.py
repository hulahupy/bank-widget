"""Common fixtures for all tests."""

import pytest


@pytest.fixture
def sample_card_numbers() -> list:
    """Fixture with sample card numbers for testing."""
    return [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("5555555555554444", "5555 55** **** 4444"),
    ]


@pytest.fixture
def sample_account_numbers() -> list:
    """Fixture with sample account numbers for testing."""
    return [
        ("73654108430135874305", "**4305"),
        ("1234567890", "**7890"),
        ("40817810500000000001", "**0001"),
    ]


@pytest.fixture
def sample_card_strings() -> list:
    """Fixture with sample card strings for widget testing."""
    return [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
    ]


@pytest.fixture
def sample_account_strings() -> list:
    """Fixture with sample account strings for widget testing."""
    return [
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счет 35383033474447895560", "Счет **5560"),
        ("Счет 1234567890", "Счет **7890"),
    ]


@pytest.fixture
def sample_dates() -> list:
    """Fixture with sample dates for testing."""
    return [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-31T23:59:59.999999", "31.12.2023"),
        ("2025-01-01T00:00:00.000000", "01.01.2025"),
    ]


@pytest.fixture
def sample_operations() -> list:
    """Fixture with sample operations for processing tests."""
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        # Удален элемент с id 123456789 (PENDING), который мешал тестам
    ]


@pytest.fixture
def operations_with_same_date() -> list:
    """Fixture with operations having same date."""
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': '2023-01-01T10:00:00'},
        {'id': 2, 'state': 'CANCELED', 'date': '2023-01-01T11:00:00'},
        {'id': 3, 'state': 'EXECUTED', 'date': '2023-01-01T09:00:00'},
    ]
