
import csv
from prettytable import PrettyTable
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd

# Function to add an expense
def add_expense(date, category, amount, description):
    with open("expenses.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])
    print("Expense added successfully!")

# Function to display all expenses in a tabular format
def display_expenses():
    print("\nCurrent Expenses:")
    try:
        with open("expenses.csv", mode="r") as file:
            reader = csv.reader(file)
            table = PrettyTable()
            table.field_names = ["Date", "Category", "Amount", "Description"]
            next(reader, None)
            for row in reader:
                if len(row) < 4:
                    print(f"Skipping invalid row: {row}")
                    continue
                table.add_row(row)
            print(table)
    except FileNotFoundError:
        print("No expenses found! Please add some first.")

# Function to filter data based on time period
def filter_data(period, start_date=None, month=None, year=None):
    try:
        df = pd.read_csv('expenses.csv')
        df['Date'] = pd.to_datetime(df['Date'], format="%d-%m-%Y", dayfirst=True)  # Correct date format

        if period == "daily":
            return df[df['Date'] == start_date]
        elif period == "weekly":
            end_date = start_date + timedelta(days=6)
            return df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        elif period == "monthly" and month and year:
            return df[(df['Date'].dt.year == year) & (df['Date'].dt.month == month)]
        elif period == "yearly" and year:
            return df[df['Date'].dt.year == year]
        else:
            return df
    except FileNotFoundError:
        print("No expenses found! Please add some first.")
        return None

# Function to display graph based on filtered data
def display_graph(period):
    try:
        if period == "weekly":
            start_date = input("Enter the start date of the week (DD-MM-YYYY): ")
            try:
                start_date = datetime.strptime(start_date, "%d-%m-%Y")
            except ValueError:
                print("Invalid date format! Please try again.")
                return
            filtered_df = filter_data(period, start_date=start_date)
        elif period == "monthly":
            month = int(input("Enter the month (1-12): "))
            year = int(input("Enter the year (YYYY): "))
            filtered_df = filter_data(period, month=month, year=year)
        elif period == "yearly":
            year = int(input("Enter the year (YYYY): "))
            filtered_df = filter_data(period, year=year)
        else:
            today = datetime.now()
            filtered_df = filter_data(period, start_date=today)

        if filtered_df is not None and not filtered_df.empty:
            plt.bar(filtered_df['Date'].astype(str), filtered_df['Amount'])
            plt.xlabel('Date')
            plt.ylabel('Amount')
            plt.title(f"{period.capitalize()} Expenditure")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        else:
            print(f"No data available for the selected {period} period.")
    except Exception as e:
        print(f"An error occurred while displaying the graph: {e}")

# Function to calculate expenditure summaries
def calculate_summary(period):
    try:
        if period == "weekly":
            start_date = input("Enter the start date of the week (DD-MM-YYYY): ")
            try:
                start_date = datetime.strptime(start_date, "%d-%m-%Y")
            except ValueError:
                print("Invalid date format! Please try again.")
                return
            filtered_df = filter_data(period, start_date=start_date)
        elif period == "monthly":
            month = int(input("Enter the month (1-12): "))
            year = int(input("Enter the year (YYYY): "))
            filtered_df = filter_data(period, month=month, year=year)
        elif period == "yearly":
            year = int(input("Enter the year (YYYY): "))
            filtered_df = filter_data(period, year=year)
        else:
            today = datetime.now()
            filtered_df = filter_data(period, start_date=today)

        if filtered_df is not None and not filtered_df.empty:
            table = PrettyTable()
            table.field_names = ["Date", "Total Expenditure"]
            grouped_data = filtered_df.groupby(filtered_df['Date'].dt.date)['Amount'].sum()
            for date, total in grouped_data.items():
                table.add_row([date, f"{total:.2f}"])
            print(table)
        else:
            print(f"No data available for the selected {period} period.")
    except Exception as e:
        print(f"An error occurred while calculating the summary: {e}")

# Function to display the menu and get user input
def main_menu():
    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Graph")
        print("4. View Summary (Daily, Weekly, Monthly, Yearly)")
        print("5. Exit")

        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == "1":
            date = input("Enter the date (DD-MM-YYYY): ")
            category = input("Enter the category (e.g., Food, Transport, etc.): ")
            amount = input("Enter the amount: ")
            description = input("Enter a brief description: ")
            add_expense(date, category, amount, description)
        elif choice == "2":
            display_expenses()
        elif choice == "3":
            print("\nChoose a graph period:")
            print("1. Daily")
            print("2. Weekly")
            print("3. Monthly")
            print("4. Yearly")
            period_choice = input("Enter your choice (1/2/3/4): ")
            period_map = {
                "1": "daily",
                "2": "weekly",
                "3": "monthly",
                "4": "yearly",
            }
            if period_choice in period_map:
                display_graph(period_map[period_choice])
            else:
                print("Invalid choice! Please try again.")
        elif choice == "4":
            print("\nChoose a summary period:")
            print("1. Daily")
            print("2. Weekly")
            print("3. Monthly")
            print("4. Yearly")
            period_choice = input("Enter your choice (1/2/3/4): ")
            period_map = {
                "1": "daily",
                "2": "weekly",
                "3": "monthly",
                "4": "yearly",
            }
            if period_choice in period_map:
                calculate_summary(period_map[period_choice])
            else:
                print("Invalid choice! Please try again.")
        elif choice == "5":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

# Run the program
if __name__ == "__main__":
    main_menu()
