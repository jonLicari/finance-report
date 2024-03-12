"""Calculate the total money ins & outs and category totals."""
from decimal import Decimal

from expense_class import Cashflow, Expense


def calculate_category_totals(
    monthly_list: list[Expense], labels: dict[str, list[str]]
) -> tuple[dict[str, Decimal], dict[str, dict[str, Decimal]]]:
    """Calculate sum for each category and sub-category."""

    # Initialization
    primary: dict[str, Decimal] = {key: Decimal(0) for key in labels.keys()}

    secondary: dict[str, dict[str, Decimal]] = {
        key: {sub_key: Decimal(0) for sub_key in labels[key]} for key in labels.keys()
    }

    # Calculation
    for expense in monthly_list:
        # add to the tally of that primary
        primary[expense.category] += expense.amount

        # add to the tally of that secondary
        secondary[expense.category][expense.subcat] += expense.amount

    return primary, secondary


def calculate_total_incoming(expense_list: list[Expense]) -> Decimal:
    """Calculate the total sum of items tagged as Income."""
    total_income: Decimal = Decimal("0")

    for expense in expense_list:
        if expense.exp_type == "Income":
            total_income = total_income + expense.amount

    return total_income


def calculate_total_outgoing(expense_list: list[Expense]) -> Decimal:
    """Calculate the total sum of items tagged as Expense."""
    total_outgoing: Decimal = Decimal("0")

    for expense in expense_list:
        if expense.exp_type == "Expense":
            total_outgoing = total_outgoing + expense.amount

    return total_outgoing


def monthly_inout_sums(sorted_ytd_list: list[list[Expense]]) -> list[Cashflow]:
    """Calculate total inouts for each month."""
    monthly_inouts: list[Cashflow] = []

    for month in sorted_ytd_list:
        inouts = Cashflow(
            calculate_total_incoming(month), calculate_total_outgoing(month)
        )
        monthly_inouts.append(inouts)

    return monthly_inouts


def calculate_ytd_inout(monthly_inouts: list[Cashflow]) -> Cashflow:
    """Calculate the YTD total ins and outs."""
    ytd_total = Cashflow(Decimal(0), Decimal(0))

    for month in monthly_inouts:
        ytd_total.ingoing += month.ingoing
        ytd_total.outgoing += month.outgoing

    return ytd_total
