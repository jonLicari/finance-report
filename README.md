# Cashflow Reporting

Organizes financial data from xlsx files and generates a report with graphic summaries

# Setup

1. Clone repo
2. Run `sh execute.sh` to do the following:<br>
  a. Setup virtual environemnt & install dependencies (`sh setup.sh`)<br>
  b. Lint the program (`sh lint.sh`)<br>
  c. Run the program<br>

Upload personal datasets or use public sample data

## Sample Data

| Type    | Name              | Amount  | Date       | Category       | Sub-category | Comments            |
| ------- | ----------------- | ------- | ---------- | -------------- | ------------ | ------------------- |
| Income  | Payroll           | 1800.00 | 01/01/2023 | Income         | Salary       | Monthly salary      |
| Expense | Rent              | 800.00  | 01/01/2023 | Utilities      | Rent         | Apartment rent      |
| Expense | Grocery Shopping  | 75.50   | 02/01/2023 | Food           | Grocery      | Weekly groceries    |
| Income  | Freelance Project | 300.00  | 03/01/2023 | Income         |              | Web development     |
| Expense | Gas Station       | 40.00   | 03/01/2023 | Transportation | Gas          | Fuel for the car    |
| Income  | Bonus             | 200.00  | 04/01/2023 | Income         |              | Performance bonus   |
| Expense | Online Shopping   | 150.00  | 05/01/2023 | Shopping       | Other        | Clothing purchase   |
| Income  | Side Gig          | 120.00  | 06/01/2023 | Income         |              | Consulting project  |
| Expense | Dining Out        | 60.00   | 07/01/2023 | Food           | Restaurant   | Dinner with friends |

## Expense Item Categories

| Food       | Shopping | Transportation   | Utilities        | Entertainment | Career | Health | Income |
| ---------- | -------- | ---------------- | ---------------- | ------------- | ------ | ------ | ------ |
| Restaurant | Clothing | Gas              | Phone            | Gaming        |        |        | Salary |
| Grocery    | Gifts    | Transit	         | Internet         | Events        |        |        | Other  |
| Alcohol    | Other    | Insurance        | Hydro            | Other         |        |        |        |
|            |          | Car              | Rent             |               |        |        |        |
|            |          |                  | Tenant Insurance |               |        |        |        |

## Cashflow Item

- Type:
  - Income
  - Expense
- Name
- Amount
- Date
  - mm-dd-yyyy
- Category
  - Income sources (e.g. salary, freelance)
  - Expense category (e.g. transportation)
- Sub-Category
  - Expense sub-category (e.g. transportation -> gas, transit)
- Notes
  - additional description of item
