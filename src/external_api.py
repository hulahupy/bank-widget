"""
Module for external API calls.
"""

import os
from typing import Any, Dict

import requests


def get_exchange_rate(currency_code: str) -> float:
    """
    Get exchange rate for currency to RUB from external API.

    Args:
        currency_code: Currency code (USD, EUR)

    Returns:
        Exchange rate to RUB

    Raises:
        ValueError: If API key not found or rate unavailable
    """
    api_key = os.getenv("EXCHANGE_RATES_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Set EXCHANGE_RATES_API_KEY in .env file")

    url = "https://api.apilayer.com/exchangerates_data/latest"
    headers = {"apikey": api_key}
    params = {"base": currency_code, "symbols": "RUB"}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        rate = data.get("rates", {}).get("RUB")
        if rate is None:
            raise ValueError(f"Exchange rate for {currency_code} to RUB not available")

        return float(rate)

    except Exception as e:
        # Ловим любые исключения (и requests.RequestException, и обычные Exception)
        raise ValueError(f"API request failed: {e}") from e


def convert_to_rubles(transaction: Dict[str, Any]) -> float:
    """
    Convert transaction amount to rubles.

    Args:
        transaction: Transaction dictionary with operationAmount field

    Returns:
        Amount in rubles as float

    Examples:
        >>> transaction = {
        ...     "operationAmount": {
        ...         "amount": "100.00",
        ...         "currency": {"code": "USD"}
        ...     }
        ... }
        >>> convert_to_rubles(transaction)  # Returns amount * USD rate
    """
    operation_amount = transaction.get("operationAmount", {})
    amount_str = operation_amount.get("amount", "0")
    amount = float(amount_str)
    currency_code = operation_amount.get("currency", {}).get("code", "RUB")

    if currency_code == "RUB":
        return amount

    if currency_code in ("USD", "EUR"):
        rate = get_exchange_rate(currency_code)
        return round(amount * rate, 2)

    return amount
