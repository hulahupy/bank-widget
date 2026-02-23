"""Main module for demonstrating masking functions."""

from src.processing import filter_by_state, sort_by_date
from src.widget import get_date, mask_account_card


def main() -> None:
    """Demonstrate masking and processing functions."""
    # Example 1: Mask card and account
    print("=== Mask account_card function ===")
    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(mask_account_card("Счет 73654108430135874305"))
    print()

    # Example 2: Format date
    print("=== Get date function ===")
    print(get_date("2024-03-11T02:26:18.671407"))
    print()

    # Example 3: Process operations
    print("=== Processing functions ===")
    operations = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    ]

    executed = filter_by_state(operations)
    print(f"Filtered EXECUTED: {executed}")

    sorted_ops = sort_by_date(operations)
    print(f"Sorted by date: {sorted_ops}")


if __name__ == "__main__":
    main()
