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

from expense_class import Expense, ExpenseFormat
from get_input_dataset import read_data_file


def format_object_list(input_df: pd.DataFrame) -> list[Expense]:
    """Convert pandas dataframe to an object list."""
    # The object list will be populated from the raw_data_file_df
    expense_list: list[Expense] = []

    # Find number of entries in the dataframe
    num_expense_entries = len(input_df)

    # Populate the object list
    for i in range(num_expense_entries):
        # Read each row of the dataframe into an instance of the Expense object
        new_expense = Expense(
            input_df.iloc[i, ExpenseFormat.TYPE.value],
            input_df.iloc[i, ExpenseFormat.NAME.value],
            input_df.iloc[i, ExpenseFormat.AMT.value],
            input_df.iloc[i, ExpenseFormat.DATE.value],
        )

        category = ""
        if pd.isnull(input_df.iloc[i, ExpenseFormat.CAT.value]):
            category = "Other"
        else:
            category = input_df.iloc[i, ExpenseFormat.CAT.value]

        subcategory = ""
        if pd.isnull(input_df.iloc[i, ExpenseFormat.SCAT.value]):
            subcategory = "Other"
        else:
            subcategory = input_df.iloc[i, ExpenseFormat.SCAT.value]

        new_expense.categorize(category, subcategory)
        new_expense.add_notes(input_df.iloc[i, ExpenseFormat.NOTE.value])

        # add new Expense item to the expense object list
        expense_list.append(new_expense)

    # Remove unwanted header data
    expense_list.remove(expense_list[0])

    return expense_list


def main():
    """File Main method."""
    # Read input data file
    raw_data = read_data_file()

    # Format data
    refined_data: list[Expense] = format_object_list(raw_data)

    # Calculate categorical totals
    # TODO

    # Publish graphs to PDF
    # TODO


if __name__ == "__main__":
    main()
