"""Orchestrate printing of cashflow totals to the terminal."""
from decimal import Decimal

from expense_class import Cashflow
from serialize_data import export_to_json


def print_category_sums(
    primary: dict[str, Decimal], secondary: dict[str, dict[str, Decimal]]
) -> None:
    """Print category & subcategory breakdown."""
    export_to_json(primary, secondary)
    # print("Primary", primary)
    # print("Secondary", secondary)


def print_cashflow(cashflow_object: Cashflow) -> None:
    """Print dollar values of Cashflow objects to terminal."""
    print("   Ingoing:  $", cashflow_object.ingoing)
    print("   Outgoing: $", cashflow_object.outgoing)


def month_index_to_string(index: int) -> str:  # type: ignore
    """Return the month as a string based on the index."""
    assert 1 <= index <= 12, "Invalid month index."
    month: str
    match index:
        case 1:
            month = "January"
        case 2:
            month = "February"
        case 3:
            month = "March"
        case 4:
            month = "April"
        case 5:
            month = "May"
        case 6:
            month = "June"
        case 7:
            month = "July"
        case 8:
            month = "August"
        case 9:
            month = "September"
        case 10:
            month = "October"
        case 11:
            month = "November"
        case 12:
            month = "December"
    return month


def print_main(monthly_totals: list[Cashflow], ytd_total: Cashflow) -> None:
    """Orchestrate printing monthly to terminal."""
    index_of_month: int = 1

    # Print YTD
    print("--------------------")
    print("Year-to-Date:")
    print_cashflow(ytd_total)
    print("--------------------")

    # Print monthly totals
    for month in monthly_totals:
        print(month_index_to_string(index_of_month))
        print_cashflow(month)
        index_of_month += 1
