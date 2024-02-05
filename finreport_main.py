#!/usr/bin/env/python3

# ---------------------------------------------------------------------- #
# Author: Jonathan Licari                                                #
# File: finreport_main.py                                                #
# Organizes financial data from xlsx files and                           #
# generates financial reports and graphic summaries                      #
#                                                                        #
# Input: Raw expense data xlsx file                                      #
# Output: none                                                           #
# ---------------------------------------------------------------------- #
"""Report main file."""

import os
import tempfile

import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF

from utils.expense_class import Expense

# ---------------------------------------------------------------------- #
# Constant Declarations
# ---------------------------------------------------------------------- #
TYPE = 0
NAME = 1
AMT = 2
DATE = 3
CAT = 4
SCAT = 5
NOTE = 6


def user_datset_selection(limit: int) -> int:
    """Prompt user to select index of the datset they want to use."""
    while True:
        try:
            raw_input = int(input("Select dataset to be processed: "))

            # validate iuser input
            if 0 <= raw_input <= limit:
                return raw_input

            print("Selection not valid. Please try again.")

        except ValueError:
            print("Invalid input. Please enter a valid integer index.")


def data_resource() -> str:
    """Return the path to the data resource."""
    base_path = os.getcwd() + "/data"
    sample_dataset_path = os.getcwd() + "/data/sample/sample.xlsx"
    extension = ".xlsx"
    file_path = ""
    file_list = [file for file in os.listdir(base_path) if file.endswith(extension)]

    if len(file_list) == 0:
        print("No user data found. Using sample dataset...")
        file_path = sample_dataset_path

    elif len(file_list) > 1:
        print("Multiple user datasets found. Select the dataset to be used:")

        # list file selection options
        count = 0
        for i, name in enumerate(file_list):
            print(f"File {i}: {name}")
            count = i
        count = count + 1
        print(f"File {count}: sample.xlsx")

        # take user input
        dataset_selection = user_datset_selection(count)

        if dataset_selection == count:
            print("Selecting sample dataset")
            file_path = sample_dataset_path

        elif dataset_selection < count:
            file_path = os.path.join(base_path, file_list[dataset_selection])
            print("Selecting ", file_list[dataset_selection])

        else:
            print("You fucked it all up.")

    else:
        file_path = os.path.join(base_path, file_list[0])

    return file_path


def read_data_file():
    """Input data from xlsx file and store in a pandas dataframe."""
    raw_data_file_df = pd.read_excel(data_resource())

    # Number data stored as float64 by default.
    # Convert to string to avoid floating point operations
    raw_data_file_df["Amount"] = raw_data_file_df["Amount"].astype(str)

    return raw_data_file_df


def format_object_list(input_df: pd.DataFrame):
    """Convert pandas dataframe to an object list."""
    # The object list will be populated from the raw_data_file_df
    expense_list = []

    # Find number of entries in the dataframe
    num_expense_entries = len(input_df)

    # Populate the object list
    for i in range(num_expense_entries):
        # Read each row of the dataframe into an instance of the Expense object
        new_expense = Expense(
            input_df.iloc[i][TYPE],
            input_df.iloc[i][NAME],
            input_df.iloc[i][AMT],
            input_df.iloc[i][DATE],
        )
        new_expense.categorize(input_df.iloc[i][CAT], input_df.iloc[i][SCAT])
        new_expense.add_notes(input_df.iloc[i][NOTE])

        # add new Expense item to the expense object list
        expense_list.append(new_expense)

    # Remove unwanted header data
    expense_list.remove(expense_list[0])

    return expense_list


def categorical_total(expense_list: list[Expense]) -> None:
    """Calculate total sum for each category and sub-category."""
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

    # plot_net_savings(expense_list)
    # plot_income(expense_list)
    # plot_secondary_subcat(expense_list)
    # plot_category_expenses(expense_list)
    create_report(expense_list)


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
    plt.show(block=False)
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


def main():
    """File Main method."""
    # Read input data file
    raw_data = read_data_file()

    # Format data
    refined_data = format_object_list(raw_data)

    # Calculate categorical totals
    categorical_total(refined_data)


if __name__ == "__main__":
    main()
