"""File defines the Expense class to be used."""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from datetime import datetime


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
        self.exp_type: str = exp_type
        self.name: str = name
        self.amount = Decimal(amount)
        formatted_date = datetime.strptime(date, "%Y-%m-%d")
        self.date: str = datetime.strftime(formatted_date, "%Y-%m-%d")
        self.category: str = ""
        self.subcat: str = ""
        self.notes: str = ""

    def categorize(self, primary, secondary):
        """Categorize the expense item."""
        self.category = primary
        self.subcat = secondary

    def add_notes(self, notes):
        """Add optional notes to expense item."""
        self.notes = notes


@dataclass
class Cashflow:
    """Total incoming and outgoing expenditures for a month."""

    ingoing: Decimal
    outgoing: Decimal


@dataclass
class SerializedCashflow:
    """Cashflow object with standard datatypes for exporting to JSON."""

    ingoing: str | float
    outgoing: str | float
