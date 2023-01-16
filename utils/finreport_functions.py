# ---------------------------------------------------------------------- #
# Author: Jonathan Licari                                                #
# File: finreport_functions.py                                           #
# Defines functions used to compute annual and                           #
# monthly expense and income based on different metrics                  #
# ---------------------------------------------------------------------- #
"""Report financial computations."""

import decimal

from utils.expense_class import Expense

# Months lookup table
months = {
    0: "NULL",
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}


def beautify(value: decimal.Decimal):
    """
    Format larger sums for easier readability.

    Parameters
    -----------
    value : decimal.Decimal

    Returns
    -----------
    result : String
    """
    try:
        if value < 0:
            raise ValueError("Value entered", value)
    except ValueError:
        print("Only positive values are accepted.")
        raise

    value = str(value)
    size = len(value)
    result = ""

    for index in range(0, size):
        if ((index == size - 6) and ((size - 6) != 0)):
            result += "'"
            result += value[index]
        else:
            result += value[index]

    return result


def annual_income(object_list: Expense):
    """
    Calculate total annual income across all sources.

    Parameters
    -----------
    object_list : Expense

    Returns
    -----------
    result : decimal.Decimal
    """
    primary = 0
    secondary = 0
    freelance, investment, taxcred, creditreward = 0, 0, 0, 0

    for index in range(len(object_list)):
        if object_list[index].type == "Income":
            if object_list[index].category == "Primary":
                primary += object_list[index].amount
            else:
                secondary += object_list[index].amount
                match (object_list[index].subcat):
                    case("Freelance"):
                        freelance += object_list[index].amount
                    case("Investment Returns"):
                        investment += object_list[index].amount
                    case("Tax Credit"):
                        taxcred += object_list[index].amount
                    case("Credit Rewards"):
                        creditreward += object_list[index].amount

    print("\nYearly Income = $", beautify(primary + secondary))
    print("-- Income from Primary Sources= $", beautify(primary))
    print("-- Income from Secondary Sources = $", beautify(secondary))
    print("---- Freelance income = $", beautify(freelance))
    print("---- Investment Returns = $", beautify(investment))
    print("---- Tax Credits = $", beautify(taxcred))
    print("---- Credit Card Rewards = $", beautify(creditreward))

    result = (primary + secondary)
    return result


def annual_expenses(object_list: Expense):
    """
    Calculate total annual outgoing expenses.

    Parameters
    -----------
    object_list : Expense

    Returns
    -----------
    total_expense : decimal.Decimal
    """
    total_expense = 0
    for index in range(len(object_list)):
        if object_list[index].type == "Expense":
            total_expense += object_list[index].amount

    print("\nYearly expenses = $", beautify(total_expense))

    return total_expense


def monthly_income(object_list, month_id):
    """
    Calculate total income from all streams of income for a given month.

    Parameters
    -----------
    object_list : Expense
    month_id : int

    Returns
    -----------
    total_expense : decimal.Decimal

    Usage
    -----------
    monthly_income(expenseList, "-10-")
    """
    monthly_income_total = 0

    for index in range(len(object_list)):
        month_string = str(object_list[index].date)

        if (
            (month_id in month_string) and
            (object_list[index].type == "Income")
        ):
            monthly_income_total += object_list[index].amount

    month_id = months[int(month_id.replace("-", ""))]
    print("-- Income for", month_id, "= $", beautify(monthly_income_total))

    return monthly_income_total


def annual_transportation(object_list: Expense):
    """
    Calculate total annual transportation expenses.

    Parameters
    -----------
    object_list : Expense

    Returns
    -----------
    total : decimal.Decimal
    """
    total = 0
    gas, presto, ins, car, ride = 0, 0, 0, 0, 0

    for index in range(len(object_list)):
        if object_list[index].category == "Transportation":
            total += object_list[index].amount
            match (object_list[index].subcat):
                case("Gas"):
                    gas += object_list[index].amount
                case("Presto"):
                    presto += object_list[index].amount
                case("Insurance"):
                    ins += object_list[index].amount
                case("Car"):
                    car += object_list[index].amount
                case("Rideshare"):
                    ride += object_list[index].amount

    print("\nTransportation Costs = $", beautify(total))
    print("-- Gas = $", beautify(gas))
    print("-- Presto = $", beautify(presto))
    print("-- Insurance = $", beautify(ins))
    print("-- Car = $", beautify(car))
    print("-- Rideshare = $", beautify(ride))

    return total


def subscriptions_cost(object_list: Expense):
    """
    Calculate total expenditures for subscription services.

    Parameters
    -----------
    object_list : Expense

    Returns
    -----------
    total : decimal.Decimal
    """
    total = 0
    entertainment, gym, tech = 0, 0, 0

    for index in range(len(object_list)):
        if object_list[index].category == "Subscriptions":
            total += object_list[index].amount

            match (object_list[index].subcat):
                case("Entertainment"):
                    entertainment += object_list[index].amount
                case("Gym"):
                    gym += object_list[index].amount
                case("Tech"):
                    tech += object_list[index].amount

    print("\nSubscription Costs = $", beautify(total))
    print("-- Entertainment = $", beautify(entertainment))
    print("-- Gym Memberships = $", beautify(gym))
    print("-- Tech = $", beautify(tech))

    return total


def utilities_cost(object_list: Expense):
    """
    Calculate total expenditures for utilities.

    Parameters
    -----------
    object_list : Expense

    Returns
    -----------
    total : decimal.Decimal
    """
    total = 0
    phone, internet, hydro = 0, 0, 0

    for index in range(len(object_list)):
        if object_list[index].category == "Utilities":
            total += object_list[index].amount

            match (object_list[index].subcat):
                case("Phone"):
                    phone += object_list[index].amount
                case("Internet"):
                    internet += object_list[index].amount
                case("Hydro"):
                    hydro += object_list[index].amount

    print("\nUtilities Costs = $", beautify(total))
    print("-- Phone = $", beautify(phone))
    print("-- Internet = $", beautify(internet))
    print("-- Hydro = $", beautify(hydro))

    return total


def food_cost(object_list: Expense):
    """
    Calculate total expenditures for food.

    Parameters
    -----------
    object_list : Expense

    Returns
    -----------
    total : decimal.Decimal
    """
    total = 0
    rest, grocery, alcohol = 0, 0, 0

    for index in range(len(object_list)):
        if object_list[index].category == "Food":
            total += object_list[index].amount

            match (object_list[index].subcat):
                case("Restaurant"):
                    rest += object_list[index].amount
                case("Grocery"):
                    grocery += object_list[index].amount
                case("Alcohol"):
                    alcohol += object_list[index].amount

    print("\nFood Costs = $", beautify(total))
    print("-- Restaurants = $", beautify(rest))
    print("-- Grocery = $", beautify(grocery))
    print("-- Alcohol = $", beautify(alcohol))

    return total


def entertainment_cost(object_list: Expense):
    """
    Calculate total expenditures for entertainment and activities.

    Parameters
    -----------
    object_list : Expense

    Returns
    -----------
    total : decimal.Decimal
    """
    total = 0
    tech, movies, gaming, events = 0, 0, 0, 0

    for index in range(len(object_list)):
        if object_list[index].category == "Entertainment":
            total += object_list[index].amount

            match (object_list[index].subcat):
                case("Tech"):
                    tech += object_list[index].amount
                case("Movies"):
                    movies += object_list[index].amount
                case("Gaming"):
                    gaming += object_list[index].amount
                case("Events"):
                    events += object_list[index].amount

    print("\nEntertainment Costs = $", beautify(total))
    print("-- Tech = $", beautify(tech))
    print("-- Movies = $", beautify(movies))
    print("-- Gaming = $", beautify(gaming))
    print("-- Events = $", beautify(events))

    return total


def home_cost(object_list: Expense):
    """
    Calculate total expenditures for home and office items.

    Parameters
    -----------
    object_list : Expense

    Returns
    -----------
    total : decimal.Decimal
    """
    total = 0
    fur, clean, office = 0, 0, 0

    for index in range(len(object_list)):
        if object_list[index].category == "Home":
            total += object_list[index].amount

            match (object_list[index].subcat):
                case("Furnishing"):
                    fur += object_list[index].amount
                case("Cleaning"):
                    clean += object_list[index].amount
                case("Office"):
                    office += object_list[index].amount

    print("\nHome and Office Costs = $", beautify(total))
    print("-- Furnishing = $", beautify(fur))
    print("-- Cleaning Supplies = $", beautify(clean))
    print("-- Office Supplies = $", beautify(office))

    return total


def report(object_list):
    """
    Print income and expenditure report.

    Parameters
    -----------
    object_list : Expense
    """
    value = 0
    income, expenditures = 0, 0
    trans, subs, util, eat, ent, hmof = 0, 0, 0, 0, 0, 0

    # 1. Annual Income
    income = annual_income(object_list)

    # 2. Annual Expenses
    expenditures = annual_expenses(object_list)

    # 3. Monthly Income
    # monthly_income(expenseList, "-10-")

    # 5. Annual Transportation
    trans = annual_transportation(object_list)

    # 6. Annual Subscriptions
    subs = subscriptions_cost(object_list)

    # 7. Annual Utilities
    util = utilities_cost(object_list)

    # 8. Annual Food
    eat = food_cost(object_list)

    # 9. Annual Entertainment
    ent = entertainment_cost(object_list)

    # 10. Annual Home and Office
    hmof = home_cost(object_list)

    # Calculate Savings
    value = income - expenditures
    print("\n\nSavings = $", beautify(value))

    # Expenditure to Income
    # value = "{:.2f}".format((expenditures / income) * 100)
    value = f'{(expenditures / income) * 100}'
    print("Spent ", value, "% of income")
    value = "{:.2f}".format((1 - (expenditures / income)) * 100)
    print("Saved ", value, "% of income")

    # Expenditure breakdown
    print("\nExpenditures")

    value = "{:.2f}".format((trans / expenditures) * 100)
    print("-- Transportation = %", value, "of Expenditures")

    value = "{:.2f}".format((subs / expenditures) * 100)
    print("-- Subscriptions = %", value, "of Expenditures")

    value = "{:.2f}".format((util / expenditures) * 100)
    print("-- Utilities = %", value, "of Expenditures")

    value = "{:.2f}".format((hmof / expenditures) * 100)
    print("-- Home and Office = %", value, "of Expenditures")

    value = "{:.2f}".format((eat / expenditures) * 100)
    print("-- Food = %", value, "of Expenditures")

    value = "{:.2f}".format((ent / expenditures) * 100)
    print("-- Entertainment = %", value, "of Expenditures")

    value = trans + subs + util + hmof + eat + ent
    value = "{:.2f}".format(((expenditures - value) / expenditures) * 100)
    print("-- Other = %", value, "of Expenditures")
