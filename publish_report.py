"""File publishes calculations in a PDF report."""

import tempfile

import matplotlib.pyplot as plt
from fpdf import FPDF

from expense_class import Expense


def plot_category_expenses(expense_list):
    """Plot expense categories as a pie chart."""
    # Initialize dictionary to store category totals
    category_totals = {}
    for exp in expense_list:
        # Check if expense is of type "Expense"
        if exp.exp_type == "Expense":
            # If category is not already a key in dictionary, add it
            if exp.category not in category_totals:
                category_totals[exp.category] = 0
            # Add expense amount to category total
            category_totals[exp.category] += exp.amount
    # Plot pie chart
    fig, _ = plt.subplots()
    plt.pie(
        list(category_totals.values()),
        labels=list(category_totals.keys()),
        autopct="%1.1f%%",
    )
    plt.title("Expense Categories")
    plt.show(block=False)  # since we have the pdf is there any point to these?
    return fig


def plot_income(expense_list: list[Expense]):
    """Plot all Income subcategories combined."""
    income_total = 0
    non_salary_total = 0
    income_subtotals = {}

    for expense in expense_list:
        if expense.category == "Income":
            income_total += expense.amount

            if expense.subcat not in income_subtotals:
                if expense.subcat == "":
                    income_subtotals["Other"] = expense.amount
                else:
                    income_subtotals[expense.subcat] = expense.amount
            else:
                income_subtotals[expense.subcat] += expense.amount

    # Calculate percentages for each subcategory
    percentages = [
        value / (income_total + non_salary_total) * 100
        for value in income_subtotals.values()
    ]

    # Create a list of labels for the legend
    subcat_labels = [
        f"{label} (${value:.2f}, {percent:.2f}%)"
        for label, value, percent in zip(
            income_subtotals.keys(), income_subtotals.values(), percentages
        )
    ]

    # Plot the pie chart
    fig, _ = plt.subplots()
    plt.pie(
        income_subtotals.values(),
        labels=None,  # type: ignore
        startangle=90,
        autopct="",
    )
    plt.legend(subcat_labels, loc="best", bbox_to_anchor=(1.0, 0.5))

    # Set the title of the chart
    plt.title("Income Distribution")
    # plt.show(block=False)
    return fig


def plot_net_savings(expense_list: list[Expense]):
    """Plot net savings."""
    total_income = 0
    total_expenses = 0

    for expense in expense_list:
        category = expense.category
        amount = expense.amount

        if category in ["Income"]:
            total_income += amount
        else:
            total_expenses += amount

    total_savings = total_income - total_expenses

    if total_income != 0:
        savings_percent = round((total_savings / total_income) * 100, 2)
        expenses_percent = round((total_expenses / total_income) * 100, 2)
    else:
        savings_percent = 0
        expenses_percent = 100

    labels = ["Savings", "Expenses"]
    sizes = [total_savings, total_expenses]
    percent_sizes = [savings_percent, expenses_percent]
    explode = (0.1, 0)

    fig, axis = plt.subplots()
    axis.pie(sizes, explode=explode, labels=labels, autopct="%1.1f%%", startangle=90)

    axis.set_title("Net Savings")

    # Add dollar amounts to labels
    labels = [
        f"{label}\n${size:,} ({percent}%)"
        for label, size, percent in zip(labels, sizes, percent_sizes)
    ]
    axis.legend(labels=labels, loc="best")

    # plt.show(block=False)
    return fig


def plot_to_image(fig: plt.Figure):  # type: ignore
    """Convert a Matplotlib figure to a PIL Image and return it."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
        fig.savefig(f, format="png")
        return f.name


def create_report(expense_list):
    """Create pdf report of all figures."""
    # Create the figures
    fig1 = plot_net_savings(expense_list)
    fig2 = plot_income(expense_list)
    fig3 = plot_category_expenses(expense_list)

    # Convert the figures to images
    img1 = plot_to_image(fig1)
    img2 = plot_to_image(fig2)
    img3 = plot_to_image(fig3)

    # Create the PDF document
    pdf = FPDF()
    pdf.add_page()

    # Add the figures to the PDF document
    pdf.image(img1, w=200)
    pdf.add_page()
    pdf.image(img2, w=200)
    pdf.add_page()
    pdf.image(img3, w=200)

    # Save the PDF document
    pdf.output("expense_report.pdf")
