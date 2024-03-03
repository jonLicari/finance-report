"""Calculate the total money ins & outs and category totals."""
from decimal import Decimal

from expense_class import Cashflow, Expense


def print_cashflow_totals(expense_list: list[Expense]) -> None:
    """Calculate sum for each category/ sub-category & print to terminal."""
    category_totals = {}

    for expense in expense_list:
        category = expense.category
        subcat = expense.subcat
        amount = expense.amount

        # If the category & subcategory combo isnt in the dictionary, add it
        if category not in category_totals:
            category_totals[category] = {}
        if subcat not in category_totals[category]:
            category_totals[category][subcat] = 0

        # Add the amount to the category and subcategory total
        category_totals[category][subcat] += amount

    # Print the total sum for each category and subcategory
    for category, subcats in category_totals.items():
        cat_total = 0
        for subcat, total in subcats.items():
            cat_total += total
        print(f"{category} total = ${cat_total}")
        for subcat, total in subcats.items():
            print(f"  {subcat}: ${total}")


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
