from tabulate import tabulate

added_expenses = []


def openFile():
    try:
        with open('expenses.txt', 'r', encoding='utf-8') as file:  # Specify UTF-8 encoding for Unicode support
            added_expenses.clear()  # Clear any existing data in the list
            for line in file:
                # Assume the format is: date, category, amount, description
                # Example line: "2024-01-01, Food, 200.00, Lunch"
                parts = line.strip().split(', ')  # Split by comma and space
                if len(parts) == 4:  # Ensure the line has all 4 components
                    date, category, amount_str, description = parts
                    amount = float(amount_str.replace('₹', '').strip())  # Convert amount to float and remove the ₹ symbol if present
                    added_expenses.append({
                        'date': date,
                        'category': category,
                        'amount': amount,
                        'description': description
                    })
    except FileNotFoundError:
        print("The file 'expenses.txt' was not found.")
    except Exception as e:
        print(f"Error reading file: {e}")

def show_menu():
    print("\nExpense Tracker Menu:")
    print("1. Add expense")
    print("2. View expenses")
    print("3. Track budget")
    print("4. Save expenses")
    print("5. Exit")

    selected_menu = input("Select an option (1-5): ")

    if selected_menu == "1":
        add_expense()
    elif selected_menu == "2":
        view_expenses()
    elif selected_menu == "3":
        set_budget()
    elif selected_menu == "4":
        save_expenses()
    elif selected_menu == "5":
        print("Exiting...")
        return False
    else:
        print("Invalid option, try again.")

    return True


def add_expense():
    date_input = input("Enter date of the expense (YYYY-MM-DD): ")
    if not check_the_date_if_vald(date_input):
        print("Invalid date format.")
        return

    category = input("Category: ")
    if not category.strip():
        print("Category cannot be empty.")
        return

    amount_input = input("Amount: ")
    if not is_valid_amount(amount_input):
        print("Invalid amount. Please enter a valid number.")
        return
    amount = float(amount_input)

    desc = input("Description: ")
    if not desc.strip():
        print("Description cannot be empty!")
        return

    added_expenses.append({
        'date': date_input,
        'category': category,
        'amount': amount,
        'description': desc
    })
    print("Expense added.")


def view_expenses():
    if added_expenses:
        table_data = []
        for expense in added_expenses:
            table_data.append(
                [expense['date'], expense['category'], f"Rupee {expense['amount']:.2f}", expense['description']]
            )
        headers = ["Date", "Category", "Amount", "Description"]
        print("\nExpenses:")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    else:
        print("No expenses recorded yet.")


def set_budget():
    budget = input("Enter your monthly budget: ")
    if not is_valid_amount(budget):
        print("Invalid budget. Please enter a valid number.")
        return
    budget = float(budget)
    track_expenses(budget)


def track_expenses(budget):
    total_expenses = sum(expense['amount'] for expense in added_expenses)
    print(f"Current total expenses: Rupee {total_expenses:.2f}")

    while True:
        expense_input = input("Enter an additional expense or type 'done' to finish: ")
        if expense_input.lower() == 'done':
            break
        if not is_valid_amount(expense_input):
            print("Invalid amount! Please enter a valid number.")
            continue
        expense = float(expense_input)
        total_expenses += expense

    if total_expenses > budget:
        print(f"Warning! You've exceeded your budget. Total expenses: Rupee {total_expenses:.2f}, Budget: Rupee {budget:.2f}")
    else:
        remaining_balance = budget - total_expenses
        print(f"Total expenses: Rupee {total_expenses:.2f}. You have Rupee {remaining_balance:.2f} left in your budget.")


def save_expenses():
    if added_expenses:
        with open('expenses.txt', 'w') as file:
            file.write(str(added_expenses))
        print("Expenses saved to file.")
    else:
        print("No expenses to save.")


def check_the_date_if_vald(date_str):
    if len(date_str) != 10:
        return False
    year, month, day = date_str.split('-')

    if not (year.isdigit() and month.isdigit() and day.isdigit()):
        return False

    year, month, day = int(year), int(month), int(day)

    if month < 1 or month > 12:
        return False

    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if month == 2 and (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
        days_in_month[1] = 29

    if day < 1 or day > days_in_month[month - 1]:
        return False

    return True


def is_valid_amount(amount_str):
    if amount_str.count('.') > 1:
        return False
    if not amount_str.replace('.', '', 1).isdigit():
        return False
    amount = float(amount_str)
    return amount >= 0


def main():
    openFile()
    while show_menu():
        pass  # Continue looping until user exits


if __name__ == "__main__":
    main()
