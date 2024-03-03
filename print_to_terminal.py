"""Orchestrate printing of cashflow totals to the terminal."""
from expense_class import Cashflow


def print_cashflow(cashflow_object: Cashflow) -> None:
    """Print dollar values of Cashflow objects to terminal."""
    print("   Ingoing:  $", cashflow_object.ingoing)
    print("   Outgoing: $", cashflow_object.outgoing)


def month_index_to_string(index: int) -> str:  # type: ignore
    """Return the month as a string based on the index."""
    assert 1 <= index <= 12, "Invalid month index."
    match index:
        case 1:
            return "January"
        case 2:
            return "February"
        case 3:
            return "March"
        case 4:
            return "April"
        case 5:
            return "May"
        case 6:
            return "June"
        case 7:
            return "July"
        case 8:
            return "August"
        case 9:
            return "September"
        case 10:
            return "October"
        case 11:
            return "November"
        case 12:
            return "December"


def print_main(monthly_totals: list[Cashflow], ytd_total: Cashflow) -> None:
    """Orchestrate printing monthly to terminal."""
    index_of_month: int = 1

    # Print YTD
    print("Year-to-Date:")
    print_cashflow(ytd_total)

    # Print monthly totals
    for month in monthly_totals:
        print(month_index_to_string(index_of_month), ":")
        print_cashflow(month)
