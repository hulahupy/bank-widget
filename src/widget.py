"""Module for widget bank operations."""

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """
    Mask card or account number depending on the type.

    Args:
        account_info: String with type and number of card or account.
            Example: "Visa Platinum 7000792289606361" or "Счет 73654108430135874305"

    Returns:
        String with masked number.

    Examples:
        >>> mask_account_card("Visa Platinum 7000792289606361")
        'Visa Platinum 7000 79** **** 6361'
        >>> mask_account_card("Счет 73654108430135874305")
        'Счет **4305'
    """
    parts = account_info.rsplit(" ", 1)

    if len(parts) != 2:
        raise ValueError("Invalid string format. Expected: 'Type Number'")

    account_type, account_number = parts

    if account_type.lower() == "счет":
        masked_number = get_mask_account(account_number)
    else:
        masked_number = get_mask_card_number(account_number)

    return f"{account_type} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Convert date from ISO format to DD.MM.YYYY format.

    Args:
        date_string: Date in format "2024-03-11T02:26:18.671407"

    Returns:
        Date in format "DD.MM.YYYY"

    Examples:
        >>> get_date("2024-03-11T02:26:18.671407")
        '11.03.2024'
    """
    date_part = date_string[:10]
    year, month, day = date_part.split("-")
    return f"{day}.{month}.{year}"
