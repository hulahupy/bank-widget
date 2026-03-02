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

    Raises:
        ValueError: If input string format is invalid
    """
    parts = account_info.rsplit(' ', 1)

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

    Raises:
        ValueError: If date format is invalid
    """
    # Check minimum length
    if len(date_string) < 10:
        raise ValueError("Date string is too short")

    # Check for date separator
    if '-' not in date_string:
        raise ValueError("Invalid date format. Expected ISO format with '-'")

    # Check for time part (must contain 'T')
    if 'T' not in date_string:
        raise ValueError("Invalid date format. Expected ISO format with time part (YYYY-MM-DDThh:mm:ss)")

    # Extract date part (first 10 characters)
    date_part = date_string[:10]

    # Split into components
    parts = date_part.split('-')
    if len(parts) != 3:
        raise ValueError("Invalid date format. Expected YYYY-MM-DD")

    year, month, day = parts

    # Check that all parts are digits
    if not (year.isdigit() and month.isdigit() and day.isdigit()):
        raise ValueError("Date must contain only digits")

    # Check reasonable ranges
    month_int = int(month)
    day_int = int(day)

    if not (1 <= month_int <= 12):
        raise ValueError("Month must be between 1 and 12")

    if not (1 <= day_int <= 31):
        raise ValueError("Day must be between 1 and 31")

    return f"{day}.{month}.{year}"
