"""
Tests for generators module.
"""

from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Fixture with sample transactions for testing."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


# ========== Тесты для filter_by_currency ==========


def test_filter_by_currency_usd(sample_transactions: List[Dict[str, Any]]) -> None:
    """Test filtering transactions by USD currency."""
    usd_transactions: List[Dict[str, Any]] = list(filter_by_currency(sample_transactions, "USD"))
    assert len(usd_transactions) == 3
    for transaction in usd_transactions:
        assert transaction["operationAmount"]["currency"]["code"] == "USD"


def test_filter_by_currency_rub(sample_transactions: List[Dict[str, Any]]) -> None:
    """Test filtering transactions by RUB currency."""
    rub_transactions: List[Dict[str, Any]] = list(filter_by_currency(sample_transactions, "RUB"))
    assert len(rub_transactions) == 2
    for transaction in rub_transactions:
        assert transaction["operationAmount"]["currency"]["code"] == "RUB"


def test_filter_by_currency_no_matches(sample_transactions: List[Dict[str, Any]]) -> None:
    """Test filtering with currency that has no matches."""
    eur_transactions: List[Dict[str, Any]] = list(filter_by_currency(sample_transactions, "EUR"))
    assert len(eur_transactions) == 0


def test_filter_by_currency_empty_list() -> None:
    """Test filtering empty list."""
    result: List[Dict[str, Any]] = list(filter_by_currency([]))
    assert len(result) == 0


def test_filter_by_currency_malformed_data() -> None:
    """Test filtering with malformed transaction data."""
    malformed_data: List[Dict[str, Any]] = [
        {"id": 1},  # Missing operationAmount
        {"id": 2, "operationAmount": {}},  # Missing currency
        {"id": 3, "operationAmount": {"currency": {}}},  # Missing code
    ]
    result: List[Dict[str, Any]] = list(filter_by_currency(malformed_data))
    assert len(result) == 0


# ========== Тесты для transaction_descriptions ==========


def test_transaction_descriptions(sample_transactions: List[Dict[str, Any]]) -> None:
    """Test generator yields correct descriptions."""
    descriptions: List[str] = list(transaction_descriptions(sample_transactions))
    expected: List[str] = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]
    assert descriptions == expected


def test_transaction_descriptions_empty_list() -> None:
    """Test generator with empty list."""
    descriptions: List[str] = list(transaction_descriptions([]))
    assert len(descriptions) == 0


def test_transaction_descriptions_missing_description() -> None:
    """Test generator with transactions missing description."""
    transactions: List[Dict[str, Any]] = [
        {"id": 1, "description": "Valid description"},
        {"id": 2},  # Missing description
        {"id": 3, "description": "Another valid"},
    ]
    descriptions: List[str] = list(transaction_descriptions(transactions))
    assert descriptions == ["Valid description", "Another valid"]


# ========== Тесты для card_number_generator ==========


@pytest.mark.parametrize(
    "start,stop,expected",
    [
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (9999999999999995, 9999999999999997, ["9999 9999 9999 9995", "9999 9999 9999 9996", "9999 9999 9999 9997"]),
        (0, 2, ["0000 0000 0000 0000", "0000 0000 0000 0001", "0000 0000 0000 0002"]),
    ],
)
def test_card_number_generator_range(start: int, stop: int, expected: List[str]) -> None:
    """Test card number generator with different ranges."""
    result: List[str] = list(card_number_generator(start, stop))
    assert result == expected


def test_card_number_generator_single_number() -> None:
    """Test generating single card number."""
    result: List[str] = list(card_number_generator(42, 42))
    assert result == ["0000 0000 0000 0042"]


def test_card_number_generator_format() -> None:
    """Test card number format (groups of 4 digits separated by spaces)."""
    card_numbers: List[str] = list(card_number_generator(1, 3))
    for card in card_numbers:
        parts: List[str] = card.split()
        assert len(parts) == 4
        for part in parts:
            assert len(part) == 4
            assert part.isdigit()
