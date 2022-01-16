# ---------------------------------------------------------------------- #
# Author: Jonathan Licari                                                #
# File: finreport_functions.py                                           #          
# Defines functions used to compute annual and                           #
# monthly expense and income based on different metrics                  #
# ---------------------------------------------------------------------- #
import finreport_plot 

# Definitions
INIT = 0.00
months = {0: "NULL", 1: "January", 2: "February", 3: "March", 4: "April", 
        5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 
        10: "October", 11: "November", 12: "December"}

# ---------------------------------------------------------------------- #
# Function: Beautify                                                     #
# Parameters: (decimal.Decimal) value                                    #
# Return: (String) result                                                #
# Description: Formats larger sums for easier readability.               #
# ---------------------------------------------------------------------- #
def beautify( value ):
    try:
        if ( value < 0 ):
            raise ValueError("Value entered", value)
    except ValueError:
        print("Only positive values are accepted.")
        raise

    value = str(value)
    size = len(value)
    result = ""

    for x in range(0, size):
        if ( (x == size-6) and ((size-6) != 0) ):
            result += "'"
            result += value[x]
        else:
            result += value[x]
    
    return result

# ---------------------------------------------------------------------- #
# Function: Annual Income                                                #
# Parameters: (Expense) objectList                                       #
# Return: (decimal.Decimal) (primary + secondary)                        #
# Description: Calculates total annual income across all sources         #
# ---------------------------------------------------------------------- #
def annualIncome( objectList ):
    primary = 0
    secondary = 0
    freelance, investment, taxcred, creditreward = 0, 0, 0, 0 

    for x in range(len(objectList)):
        if (objectList[x].type == "Income"):
            if (objectList[x].category == "Primary"):
                primary += objectList[x].amount
            else:
                secondary += objectList[x].amount
                match (objectList[x].subcat):
                    case("Freelance"):
                        freelance += objectList[x].amount
                    case("Investment Returns"):
                        investment += objectList[x].amount
                    case("Tax Credit"):
                        taxcred += objectList[x].amount
                    case("Credit Rewards"):
                        creditreward += objectList[x].amount
    
    print("\nYearly Income = $", beautify(primary + secondary) )
    print("-- Income from Primary Sources= $", beautify(primary))
    print("-- Income from Secondary Sources = $", beautify(secondary))
    print("---- Freelance income = $", beautify(freelance))
    print("---- Investment Returns = $", beautify(investment))
    print("---- Tax Credits = $", beautify(taxcred))
    print("---- Credit Card Rewards = $", beautify(creditreward))

    return (primary + secondary)

# ---------------------------------------------------------------------- #
# Function: Annual Expenses                                              #
# Parameters: (Expense) objectList                                       #
# Return: (decimal.Decimal) sum                                          #
# Description: Calculates total annual outgoing expenses                 #
# ---------------------------------------------------------------------- #
def annualExpenses( objectList ):
    sum = 0
    for x in range(len(objectList)):
        if (objectList[x].type == "Expense"):
            sum += objectList[x].amount

    print("\nYearly expenses = $", beautify(sum))

    return sum

# ---------------------------------------------------------------------- #
# Function: Monthly Income                                               #
# Parameters: (Expense) objectList, (int) monthID                        #
# Return: (decimal.Decimal) sum                                          #
# Description: Calculates total income from all streams of income for a  #
# given month, specified by the monthID                                  #
# ---------------------------------------------------------------------- #
def monthlyIncome( objectList, monthID ):
    sum = 0

    for x in range(len(objectList)):
        monthString = str(objectList[x].date)

        if ( monthID in monthString ) and ( objectList[x].type == "Income" ):
            sum += objectList[x].amount

    monthID = months[int(monthID.replace("-", ""))]
    print("-- Income for", monthID, "= $", beautify(sum))
    
    return sum
# test call for October
# monthlyIncome(expenseList, "-10-")

# ---------------------------------------------------------------------- #
# Function: Annual Transportation Costs                                  #
# Parameters: (Expense) objectList                                       #
# Return: (decimal.Decimal) total                                        #
# Description: Calculates total sum of all expenditures related to       #
# transportation, namely, gas, Presto, parking, vehicle costs, service,  #
# fees, and maintenance.                                                 #
# ---------------------------------------------------------------------- #
def annualTransportation( objectList ):
    total = 0
    gas, presto, ins, car, ride = 0, 0, 0, 0, 0

    for x in range( len(objectList) ):
        if ( objectList[x].category == "Transportation" ):
            total += objectList[x].amount
            match (objectList[x].subcat):
                case("Gas"):
                    gas += objectList[x].amount
                case("Presto"):
                    presto += objectList[x].amount
                case("Insurance"):
                    ins += objectList[x].amount
                case("Car"):
                    car += objectList[x].amount
                case("Rideshare"):
                    ride += objectList[x].amount

    print("\nTransportation Costs = $", beautify(total))
    print("-- Gas = $", beautify(gas))
    print("-- Presto = $", beautify(presto))
    print("-- Insurance = $", beautify(ins))
    print("-- Car = $", beautify(car))
    print("-- Rideshare = $", beautify(ride))

    return total

# ---------------------------------------------------------------------- #
# Function: Subscriptions                                                #
# Parameters: (Expense) objectList                                       #
# Return: (decimal.Decimal) total                                        #
# Description: Calculates total expenditures for subscription services   #
# ---------------------------------------------------------------------- #
def subscriptions( objectList ):
    total = 0
    entertainment, gym, tech = 0, 0, 0

    for x in range( len(objectList) ):
        if ( objectList[x].category == "Subscriptions" ):
            total += objectList[x].amount

            match (objectList[x].subcat):
                case("Entertainment"):
                    entertainment += objectList[x].amount
                case("Gym"):
                    gym += objectList[x].amount
                case("Tech"):
                    tech += objectList[x].amount

    print("\nSubscription Costs = $", beautify(total))
    print("-- Entertainment = $", beautify(entertainment))
    print("-- Gym Memberships = $", beautify(gym))
    print("-- Tech = $", beautify(tech))

    return total

# ---------------------------------------------------------------------- #
# Function: Utilities                                                    #
# Parameters: (Expense) objectList                                       #
# Return: (decimal.Decimal) total                                        #
# Description: Calculates total expenditures for utilities               #
# ---------------------------------------------------------------------- #
def utilities( objectList ):
    total = 0
    phone, internet, hydro = 0, 0, 0

    for x in range( len(objectList) ):
        if ( objectList[x].category == "Utilities" ):
            total += objectList[x].amount

            match (objectList[x].subcat):
                case("Phone"):
                    phone += objectList[x].amount
                case("Internet"):
                    internet += objectList[x].amount
                case("Hydro"):
                    hydro += objectList[x].amount

    print("\nUtilities Costs = $", beautify(total))
    print("-- Phone = $", beautify(phone))
    print("-- Internet = $", beautify(internet))
    print("-- Hydro = $", beautify(hydro))

    return total

# ---------------------------------------------------------------------- #
# Function: Food                                                         #
# Parameters: (Expense) objectList                                       #
# Return: (decimal.Decimal) total                                        #
# Description: Calculates total expenditures for food                    #
# ---------------------------------------------------------------------- #
def food( objectList ):
    total = 0
    rest, grocery, alcohol = 0, 0, 0

    for x in range( len(objectList) ):
        if ( objectList[x].category == "Food" ):
            total += objectList[x].amount

            match (objectList[x].subcat):
                case("Restaurant"):
                    rest += objectList[x].amount
                case("Grocery"):
                    grocery += objectList[x].amount
                case("Alcohol"):
                    alcohol += objectList[x].amount

    print("\nFood Costs = $", beautify(total))
    print("-- Restaurants = $", beautify(rest))
    print("-- Grocery = $", beautify(grocery))
    print("-- Alcohol = $", beautify(alcohol))

    return total

# ---------------------------------------------------------------------- #
# Function: Entertainment                                                #
# Parameters: (Expense) objectList                                       #
# Return: (decimal.Decimal) total                                        #
# Description: Calculates total expenditures for entertainment and       #
# activities                                                             #
# ---------------------------------------------------------------------- #
def entertainment( objectList ):
    total = 0
    tech, movies, gaming, events = 0, 0, 0, 0

    for x in range( len(objectList) ):
        if ( objectList[x].category == "Entertainment" ):
            total += objectList[x].amount

            match (objectList[x].subcat):
                case("Tech"):
                    tech += objectList[x].amount
                case("Movies"):
                    movies += objectList[x].amount
                case("Gaming"):
                    gaming += objectList[x].amount
                case("Events"):
                    events += objectList[x].amount

    print("\nEntertainment Costs = $", beautify(total))
    print("-- Tech = $", beautify(tech))
    print("-- Movies = $", beautify(movies))
    print("-- Gaming = $", beautify(gaming))
    print("-- Events = $", beautify(events))  

    return total

# ---------------------------------------------------------------------- #
# Function: Home                                                         #
# Parameters: (Expense) objectList                                       #
# Return: (decimal.Decimal) total                                        #
# Description: Calculates total expenditures for home and office items   #
# ---------------------------------------------------------------------- #
def home( objectList ):
    total = 0
    fur, clean, office = 0, 0, 0

    for x in range( len(objectList) ):
        if ( objectList[x].category == "Home" ):
            total += objectList[x].amount

            match (objectList[x].subcat):
                case("Furnishing"):
                    fur += objectList[x].amount
                case("Cleaning"):
                    clean += objectList[x].amount
                case("Office"):
                    office += objectList[x].amount

    print("\nHome and Office Costs = $", beautify(total))
    print("-- Furnishing = $", beautify(fur))
    print("-- Cleaning Supplies = $", beautify(clean))
    print("-- Office Supplies = $", beautify(office))

    return total

# ---------------------------------------------------------------------- #
# Function: Report                                                       #
# Parameters: (Expense) objectList                                       #
# Return: none                                                           #
# Description: Prints income and expenditure report                      #
# ---------------------------------------------------------------------- #
def report( objectList ):
    value = 0
    income , expenditures = 0, 0
    trans, subs, util, eat, ent, hmof, other = 0, 0, 0, 0, 0, 0, 0 
    
    # Used for passing arguments to plot function parameters
    outgoing = {
        "Transportation":INIT,
        "Subscriptions":INIT,
        "Utilities":INIT,
        "Food":INIT,
        "Entertainment":INIT,
        "Home & Office":INIT,
        "Other":INIT 
    }

    incoming = {
        "Salary":INIT,
        "Freelance":INIT,
        "Investment Returns":INIT,
        "Tax Credits":INIT,
        "Credit Rewards":INIT
    }
    
    ratio = {
        "Savings": INIT,
        "Expenditures": INIT
    }

    # 1. Annual Income
    income = annualIncome(objectList)

    # 2. Annual Expenses
    expenditures = annualExpenses(objectList)

    # 3. Monthly Income
    #monthlyIncome(expenseList, "-10-")

    # 5. Annual Transportation
    trans = annualTransportation(objectList)
    outgoing["Transportation"] = trans

    # 6. Annual Subscriptions
    subs = subscriptions(objectList)
    outgoing["Subscriptions"] = subs

    # 7. Annual Utilities
    util = utilities(objectList)
    outgoing["Utilities"] = util

    # 8. Annual Food
    eat = food(objectList)
    outgoing["Food"] = eat 

    # 9. Annual Entertainment
    ent = entertainment(objectList)
    outgoing["Entertainment"] = ent

    # 10. Annual Home and Office
    hmof = home(objectList)
    outgoing["Home & Office"] = hmof 

    # 11. Other
    other = expenditures - (trans + subs + util + hmof + eat + ent)
    outgoing["Other"] = other

    # ------------------------------------------------------------------ #
    # Calculate Savings
    # ------------------------------------------------------------------ #
    value = income - expenditures
    print("\n\nSavings = $", beautify(value))

    ratio["Savings"] = value
    ratio["Expenditures"] = expenditures
    
    # ------------------------------------------------------------------ #
    # Expenditure to Income
    # ------------------------------------------------------------------ #
    value = "{:.2f}".format( (expenditures / income ) * 100 )
    print("Spent ", value, "% of income" )
    value = "{:.2f}".format( ( 1 - (expenditures/income) ) * 100 )
    print("Saved ", value, "% of income" )
    
    # ------------------------------------------------------------------ #
    # Expenditure Breakdown
    # ------------------------------------------------------------------ #
    print("\nExpenditures")

    value = "{:.2f}".format((trans/expenditures)*100)
    print("-- Transportation =", value, "% of Expenditures")

    value = "{:.2f}".format((subs/expenditures)*100)
    print("-- Subscriptions =", value, "% of Expenditures")

    value = "{:.2f}".format((util/expenditures)*100)
    print("-- Utilities =", value, "% of Expenditures")

    value = "{:.2f}".format((hmof/expenditures)*100)
    print("-- Home and Office =", value, "% of Expenditures")

    value = "{:.2f}".format((eat/expenditures)*100)
    print("-- Food =", value, "% of Expenditures")

    value = "{:.2f}".format((ent/expenditures)*100)
    print("-- Entertainment =", value, "% of Expenditures")

    value = trans + subs + util + hmof + eat + ent
    value = "{:.2f}".format(((expenditures - value)/expenditures)*100)
    print("-- Other =", value, "% of Expenditures")

    # ------------------------------------------------------------------ #
    # Plotting Functions
    # ------------------------------------------------------------------ #
    finreport_plot.income_bkdwn( incoming )
    finreport_plot.expense_bkdwn( outgoing )
    finreport_plot.ratio_bkdwn( ratio )
