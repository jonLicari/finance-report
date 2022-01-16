# ---------------------------------------------------------------------- #
# Author: Jonathan Licari                                                #
# File: finreport_plot.py                                                #          
# Plots data to create graphic financial summaries                       #
# ---------------------------------------------------------------------- #
from cProfile import label
from matplotlib import pyplot as plt

# ---------------------------------------------------------------------- #
# Function: Income Breakdown                                             #
# Parameters: (dict) ratio                                               #
# Return: none                                                           #
# Description: Plots distribution of income of respective categories     #
# ---------------------------------------------------------------------- #
def income_bkdwn( ):
    income = []

# ---------------------------------------------------------------------- #
# Function: Expense Breakdown                                            #
# Parameters: (dict) ratio                                               #
# Return: none                                                           #
# Description: Plots distribution of expenses of respective categories   #
# ---------------------------------------------------------------------- #
def expense_bkdwn( expenses: dict ):
    exp = plt

    # Sort categories based on dollar amount
    expenses = dict(
        sorted( 
            expenses.items(), 
            key=lambda item: item[1],
            reverse=True
        )
    )

    # Unpack dictionary keys and values into separate tuples
    x, y = (zip(*expenses.items())) 
    
    # Build bar chart
    exp.bar(
        x,
        y
    )

    # Label chart
    exp.title("Categorical Expense Breakdown")
    exp.xlabel("Category of Expense Item")
    exp.ylabel("Amount ($)")

    # Display chart
    exp.tight_layout()
    exp.show()

# ---------------------------------------------------------------------- #
# Function: Ratio Breakdown                                              #
# Parameters: (dict) ratio                                               #
# Return: none                                                           #
# Description: Plots comparison of income spent versus income saved      #
# ---------------------------------------------------------------------- #
def ratio_bkdwn( ratio: dict ):
    fig1 = plt

    # Unpack dictionary keys and values into separate tuples
    x, y = (zip(*ratio.items())) 

    # Build pie chart
    fig1.pie(
        y, 
        radius=0.8,
        autopct='%1.2f%%',
        wedgeprops={'edgecolor': 'black'}
    )

    # Labelling chart
    fig1.legend(x,loc="best")
    fig1.title("Savings to Spending Ratio")
    
    # Display chart
    #fig1.style.use("fivethirtyeight")
    fig1.tight_layout()
    fig1.show()   



