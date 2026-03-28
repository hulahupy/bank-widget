"""
Tests for external_api module.
"""

import os
from unittest.mock import MagicMock, patch

import pytest

from src.external_api import convert_to_rubles, get_exchange_rate


def test_get_exchange_rate_success() -> None:
    """Test successful exchange rate retrieval."""
    with patch("src.external_api.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"rates": {"RUB": 91.50}}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {"EXCHANGE_RATES_API_KEY": "test_key"}, clear=True):
            rate = get_exchange_rate("USD")
            assert rate == 91.50


def test_get_exchange_rate_no_api_key() -> None:
    """Test error when API key is missing."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="API key not found"):
            get_exchange_rate("USD")


def test_get_exchange_rate_api_error() -> None:
    """Test API request failure."""
    with patch("src.external_api.requests.get") as mock_get:
        # Симулируем ошибку сети
        mock_get.side_effect = Exception("Connection error")

        with patch.dict(os.environ, {"EXCHANGE_RATES_API_KEY": "test_key"}, clear=True):
            with pytest.raises(ValueError, match="API request failed"):
                get_exchange_rate("USD")


def test_get_exchange_rate_http_error() -> None:
    """Test HTTP error response."""
    with patch("src.external_api.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 500
        # raise_for_status выбрасывает исключение
        mock_response.raise_for_status.side_effect = Exception("500 Server Error")
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {"EXCHANGE_RATES_API_KEY": "test_key"}, clear=True):
            with pytest.raises(ValueError, match="API request failed"):
                get_exchange_rate("USD")


def test_convert_to_rubles_rub() -> None:
    """Test conversion when currency is RUB."""
    transaction = {"operationAmount": {"amount": "1000.00", "currency": {"code": "RUB"}}}
    result = convert_to_rubles(transaction)
    assert result == 1000.00


def test_convert_to_rubles_usd() -> None:
    """Test conversion from USD to RUB."""
    with patch("src.external_api.get_exchange_rate") as mock_rate:
        mock_rate.return_value = 91.50

        transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}
        result = convert_to_rubles(transaction)
        assert result == 9150.00


def test_convert_to_rubles_eur() -> None:
    """Test conversion from EUR to RUB."""
    with patch("src.external_api.get_exchange_rate") as mock_rate:
        mock_rate.return_value = 98.50

        transaction = {"operationAmount": {"amount": "50.00", "currency": {"code": "EUR"}}}
        result = convert_to_rubles(transaction)
        assert result == 4925.00


def test_convert_to_rubles_missing_currency() -> None:
    """Test conversion when currency is missing."""
    transaction = {"operationAmount": {"amount": "100.00"}}
    result = convert_to_rubles(transaction)
    assert result == 100.00


def test_convert_to_rubles_unknown_currency() -> None:
    """Test conversion with unknown currency."""
    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "GBP"}}}
    result = convert_to_rubles(transaction)
    assert result == 100.00
