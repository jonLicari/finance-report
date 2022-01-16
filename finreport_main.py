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

import pandas as pd
from decimal import *

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

# Input data from xlsx file and store in a pandas dataframe
rawDataFile_df = pd.read_excel(config.rawDataFile)

# Number data stored as float64 by default. Convert to string to avoid 
# floating point operations
rawDataFile_df['Amount'] = rawDataFile_df['Amount'].astype(str)

# ---------------------------------------------------------------------- #
# Data Structure: Expense Item
# Description: Contains attributes describing the expense item 
# ---------------------------------------------------------------------- #
# | Type | Name | Amount | Date | Category | Sub-Category | Notes |
# ---------------------------------------------------------------------- #
# Type: Income, Expense
# Name: 
# Amount: $ CAD
# Date: mm-dd-yyyy
# Category (sub-category): 
#   Transportation: Gas, Presto, Insurance, Car, Rideshare
#   Primary: 
#   Secondary: Freelance, Investment Returns, Tax Credit, Credit Rewards 
#   Subscriptions: Entertainment, Gym, Tech, 
#   Utilities: Phone, Internet, Hydro,
#   Home: Furnishing, Cleaning, Office
#   Food: Restaurant, Grocery, Alcohol
#   Entertainment: Tech, Movies, Gaming, Events
#   
# ---------------------------------------------------------------------- #
class Expense:
    def __init__(self, type, name, amount, date, category, subcat, notes):
        self.type = type
        self.name = name
        self.amount = Decimal(amount)
        self.date = date
        self.category = category
        self.subcat = subcat
        self.notes = notes

# The object list will be populated from the rawDataFile_df
expenseList = []

# Find number of entries in the dataframe
numExpenseEntries = len(rawDataFile_df)

# Populate the object list 
for i in range(numExpenseEntries):
    # Read each row of the dataframe into an instance of the Expense object
    newExpense = Expense(
        rawDataFile_df.iloc[i][TYPE],
        rawDataFile_df.iloc[i][NAME],
        rawDataFile_df.iloc[i][AMT],
        rawDataFile_df.iloc[i][DATE],
        rawDataFile_df.iloc[i][CAT],
        rawDataFile_df.iloc[i][SCAT],
        rawDataFile_df.iloc[i][NOTE]
        )
    expenseList.append(newExpense)

# Remove unwanted header data
expenseList.remove(expenseList[0])

# Executions List 
finreport_functions.report(expenseList)


