"""Orchestrate printing of cashflow totals to the terminal."""
from decimal import Decimal
from expense_class import Cashflow


def print_category_sums(
    primary: dict[str, Decimal], secondary: dict[str, dict[str, Decimal]]
) -> None:
    """Print category & subcategory breakdown."""
    print("Primary", primary)
    print("Secondary", secondary)


def print_cashflow(cashflow_object: Cashflow) -> None:
    """Print dollar values of Cashflow objects to terminal."""
    print("   Ingoing:  $", cashflow_object.ingoing)
    print("   Outgoing: $", cashflow_object.outgoing)


def print_main(monthly_totals: dict[str, Cashflow], ytd_total: Cashflow) -> None:
    """Orchestrate printing monthly to terminal."""

    # Print YTD
    print("--------------------")
    print("Year-to-Date:")
    print_cashflow(ytd_total)
    print("--------------------")

    # Print monthly totals
    for month in monthly_totals:
        print(month + ":")
        print_cashflow(monthly_totals[month])
