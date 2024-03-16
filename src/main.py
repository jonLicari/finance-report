#!/usr/bin/env/python3

"""Report main file."""
from datetime import datetime
import pandas as pd
from calculate_cashflow import (
    calculate_category_totals,
    calculate_ytd_inout,
    monthly_inout_sums,
)

from expense_class import Cashflow, Expense, ExpenseFormat
from get_input_dataset import read_data_file
from print_to_terminal import print_main, print_category_sums
from serialize_data import export_all_to_json


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


def sort_ytd_to_months(ytd_expenses: list[Expense]) -> list[list[Expense]]:
    """Sort YTD into monthly sets"""
    sorted_expense_list: list[list[Expense]] = []

    # O(n^2) - TODO improve this
    for month in range(1, 13):
        monthly_expense_list: list = []
        for expense in ytd_expenses:
            if datetime.strptime(expense.date, "%Y-%m-%d").month == month:
                monthly_expense_list.append(expense)
        sorted_expense_list.append(monthly_expense_list)

    return sorted_expense_list


def establish_categories(expenses: list[Expense]) -> dict[str, list[str]]:
    """Associate categories with respective subcategory lists."""
    categories: dict[str, list[str]] = {}
    primary: list[str] = []
    secondary: list[list[str]] = []

    for expense in expenses:
        if expense.category not in primary:
            primary.append(expense.category)

        idx = primary.index(expense.category)

        if len(secondary) <= idx:
            secondary.append([expense.subcat])

        if expense.subcat not in secondary[idx]:
            secondary[idx].append(expense.subcat)

    # pack dictionary
    categories = dict(zip(primary, secondary))
    # print(categories)
    return categories


def main():
    """File Main method."""
    # Read input data file
    raw_data = read_data_file()

    # Format raw data
    refined_data: list[Expense] = format_object_list(raw_data)

    # Sort data by month
    sorted_data: list[list[Expense]] = sort_ytd_to_months(refined_data)

    # Perform Calculations
    monthly_totals: list[Cashflow] = monthly_inout_sums(sorted_data)
    ytd_total: Cashflow = calculate_ytd_inout(monthly_totals)
    primary_sums, secondary_sums = calculate_category_totals(
        refined_data, establish_categories(refined_data)
    )

    # Save all calculations to file
    export_all_to_json(ytd_total, monthly_totals, primary_sums, secondary_sums)

    # Print calculated inout transactions to terminal
    print_main(monthly_totals, ytd_total)
    print_category_sums(primary_sums, secondary_sums)

    # Publish graphs to PDF
    # TODO in future PR


if __name__ == "__main__":
    main()
