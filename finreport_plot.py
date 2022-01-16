# ---------------------------------------------------------------------- #
# Author: Jonathan Licari                                                #
# File: finreport_plot.py                                                #          
# Plots data to create graphic financial summaries                       #
# ---------------------------------------------------------------------- #
from cProfile import label
from decimal import *

from matplotlib import pyplot as plt

def income_bkdwn( ):
    income = []

def expense_bkdwn( expenses ):
    exp = []
    
    

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
    fig1.legend(x,loc="best")
    fig1.show()   



