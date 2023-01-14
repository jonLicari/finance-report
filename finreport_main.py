#!/usr/bin/env/ python3

# ---------------------------------------------------------------------- #
# Author: Jonathan Licari                                                #
# File: finreport_main.py                                                #
# Organizes financial data from xlsx files and                           #
# generates financial reports and graphic summaries                      #
#                                                                        #
# Input: Raw expense data xlsx file                                      #
# Output: none                                                           #
# ---------------------------------------------------------------------- #
import decimal

import pandas as pd

import config
import finreport_functions

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


def read_data_file():
    """Input data from xlsx file and store in a pandas dataframe."""
    raw_data_file_df = pd.read_excel(config.rawDataFile)

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
            input_df.iloc[i][CAT],
            input_df.iloc[i][SCAT],
            input_df.iloc[i][NOTE]
        )
        # add new Expense item to the expense object list
        expense_list.append(new_expense)

    # Remove unwanted header data
    expense_list.remove(expense_list[0])

    return expense_list


def compute_report(expenses: list):
    """Compute the financial report using the populated expense list."""
    # Executions List
    finreport_functions.report(expenses)


class Expense:
    """Object containing Expense item details"""

    def __init__(self, type, name, amount, date, category, subcat, notes):
        self.type = type
        self.name = name
        self.amount = decimal.Decimal(amount)
        self.date = date
        self.category = category
        self.subcat = subcat
        self.notes = notes


def main():
    """File Main method."""
    # Read input data file
    raw_data = read_data_file()

    # Format data
    refined_data = format_object_list(raw_data)

    # Perform financial computations
    compute_report(refined_data)
