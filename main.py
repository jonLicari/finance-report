#!/usr/bin/env/python3

# ---------------------------------------------------------------------- #
# Author: Jonathan Licari                                                #
# File: main.py                                                          #
# Organizes financial data from xlsx files and                           #
# generates financial reports and graphic summaries                      #
#                                                                        #
# Input: Raw expense data xlsx file                                      #
# Output: none                                                           #
# ---------------------------------------------------------------------- #
"""Report main file."""
import pandas as pd

from expense_class import Expense
from get_input_dataset import read_data_file
from publish_report import create_report

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
    """Calculate sum for each category/ sub-category & prints to terminal."""
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


def main():
    """File Main method."""
    # Read input data file
    raw_data = read_data_file()

    # Format data
    refined_data = format_object_list(raw_data)

    # Calculate categorical totals
    categorical_total(refined_data)

    # Publish graphs to PDF
    create_report(refined_data)


if __name__ == "__main__":
    main()
