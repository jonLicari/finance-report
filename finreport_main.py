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

import matplotlib.pyplot as plt
import pandas as pd

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


def data_resource():
    """Return the path to the data resource."""
    data_path = os.getcwd() + "/data"
    extension = ".xlsx"

    data = [file for file in os.listdir(data_path) if file.endswith(extension)]

    if len(data) == 0:
        print("No xlsx files found.")
    elif len(data) > 1:
        print("Multiple xlsx files found.")
    else:
        file_path = os.path.join(data_path, data[0])

    return file_path


def read_data_file():
    """Input data from xlsx file and store in a pandas dataframe."""
    raw_data_file_df = pd.read_excel(data_resource())

    # Number data stored as float64 by default.
    # Convert to string to avoid floating point operations
    raw_data_file_df['Amount'] = raw_data_file_df['Amount'].astype(str)

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
        new_expense.categorize(
            input_df.iloc[i][CAT],
            input_df.iloc[i][SCAT]
        )
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

        # If the category and subcategory combination is not in the dictionary, add it
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

    plot_net_savings(expense_list)
    plot_income(expense_list)


def plot_income(expense_list: list[Expense]) -> None:
    """Plot a pie chart of all subcategories of Primary and Secondary combined."""
    primary_total = 0
    secondary_total = 0
    primary_subtotals = {}
    secondary_subtotals = {}

    for expense in expense_list:
        if expense.category == "Primary":
            if expense.subcat not in primary_subtotals:
                primary_subtotals[expense.subcat] = expense.amount
            else:
                primary_subtotals[expense.subcat] += expense.amount
            primary_total += expense.amount
        elif expense.category == "Secondary":
            if expense.subcat not in secondary_subtotals:
                secondary_subtotals[expense.subcat] = expense.amount
            else:
                secondary_subtotals[expense.subcat] += expense.amount
            secondary_total += expense.amount

    # Combine subtotals for Primary and Secondary into one dictionary
    combined_subtotals = {**primary_subtotals, **secondary_subtotals}

    # Calculate percentages for each subcategory
    percentages = [value / (primary_total + secondary_total) * 100 for value in combined_subtotals.values()]

    # Create a list of labels for the legend
    subcat_labels = [f"{label} (${value:.2f}, {percent:.2f}%)" for label, value, percent in zip(combined_subtotals.keys(), combined_subtotals.values(), percentages)]

    # Plot the pie chart
    plt.pie(combined_subtotals.values(), labels=None, startangle=90, autopct='')
    plt.legend(subcat_labels, loc='best', bbox_to_anchor=(1.0, 0.5))

    # Set the title of the chart
    plt.title("Primary and Secondary Subcategory Expenses")
    plt.show()


def plot_net_savings(expense_list: list[Expense]) -> None:
    """Plot net savings."""
    total_income = 0
    total_expenses = 0

    for expense in expense_list:
        category = expense.category
        amount = expense.amount

        if category in ["Primary", "Secondary"]:
            total_income += amount
        else:
            total_expenses += amount

    total_savings = total_income - total_expenses
    savings_percent = round((total_savings / total_income) * 100, 2)
    expenses_percent = round((total_expenses / total_income) * 100, 2)

    labels = ["Savings", "Expenses"]
    sizes = [total_savings, total_expenses]
    percent_sizes = [savings_percent, expenses_percent]
    explode = (0.1, 0)

    _, axis = plt.subplots()
    axis.pie(
        sizes,
        explode=explode,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90
    )

    axis.set_title("Net Savings")

    # Add dollar amounts to labels
    labels = [f"{label}\n${size:,} ({percent}%)"
              for label, size, percent in zip(labels, sizes, percent_sizes)]
    axis.legend(labels=labels, loc="best")

    plt.show()


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
