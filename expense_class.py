"""File defines the Expense class to be used."""

import decimal
from enum import Enum


class ExpenseFormat(Enum):
    """Indices of Expense object"""

    TYPE = 0
    NAME = 1
    AMT = 2
    DATE = 3
    CAT = 4
    SCAT = 5
    NOTE = 6


class Expense:
    """Object containing Expense item details."""

    def __init__(self, exp_type, name, amount, date):
        """Expense object constructor."""
        self.exp_type = exp_type
        self.name = name
        self.amount = decimal.Decimal(amount)
        self.date = date
        self.category = ""
        self.subcat = ""
        self.notes = ""

    def categorize(self, primary, secondary):
        """Categorize the expense item."""
        self.category = primary
        self.subcat = secondary

    def add_notes(self, notes):
        """Add optional notes to expense item."""
        self.notes = notes
