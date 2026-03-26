"""Module for masking bank card numbers and account numbers."""


def get_mask_card_number(card_number: int | str) -> str:
    """
    Mask a bank card number showing only first 6 and last 4 digits.

    Args:
        card_number: Card number as integer or string

    Returns:
        Masked card number in format 'XXXX XX** **** XXXX'

    Examples:
        >>> get_mask_card_number(7000792289606361)
        '7000 79** **** 6361'
        >>> get_mask_card_number("7000792289606361")
        '7000 79** **** 6361'

    Raises:
        ValueError: If card number is not 16 digits
    """
    card_str = str(card_number)

    if len(card_str) != 16:
        raise ValueError("Card number must be 16 digits")

    return f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"


def get_mask_account(account_number: int | str) -> str:
    """
    Mask a bank account number showing only last 4 digits.

    Args:
        account_number: Account number as integer or string

    Returns:
        Masked account number in format '**XXXX'

    Examples:
        >>> get_mask_account(73654108430135874305)
        '**4305'
        >>> get_mask_account("73654108430135874305")
        '**4305'

    Raises:
        ValueError: If account number has less than 4 digits
    """
    account_str = str(account_number)

    if len(account_str) < 4:
        raise ValueError("Account number must be at least 4 digits")

    return f"**{account_str[-4:]}"
