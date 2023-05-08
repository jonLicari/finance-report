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


def categorical_total(expense_list: Expense):
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
        print(category)
        for subcat, total in subcats.items():
            print(f"  {subcat}: {total}")


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
