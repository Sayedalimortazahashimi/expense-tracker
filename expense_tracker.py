from datetime import datetime
from models import Expense
from database import DatabaseManager

def calculate_total(price, quantity):
    return price * quantity

def is_valid_price(price):
    return price > 0

def is_valid_quantity(quantity):
    return quantity > 0
def is_valid_category(category):
    return category.strip().lower() in categories

def is_valid_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False

class ExpenseTracker:
    def __init__(self, database):
        self.database = database
    def view_expense(self):
        expenses = database.get_all_expenses()

        if not expenses:
            print("No expenses found.")
            return

        print("ID | Description | Category | Price | Qty | Total | Date")
        print("-" * 65)

        for expense in expenses:
            total = expense.calculate_total()

            print(
                f"{expense.id} | {expense.description} | "
                f"{expense.category} | {expense.price:.2f} € | "
                f"{expense.quantity} | {total:.2f} € | {expense.date}"
            )


    def show_total(self):
        expenses = self.database.get_all_expenses()

        if not expenses:
            print("No expense found!")
            return

        total = sum(
            expense.calculate_total() for expense in expenses
        )

        print(f"Total expenses: {total:.2f} €")


    def search_expenses(self):
        category = input("Enter category to search: ").strip().lower()

        if not is_valid_category(category):
            print("Invalid category.")
            return

        expenses = self.database.get_all_expenses()

        matching_expenses = [
            expense for expense in expenses
            if expense.category.strip().lower() == category
        ]

        if not matching_expenses:
            print("No expenses found in this category.")
            return

        for expense in matching_expenses:
            print(
                f"{expense.id} | {expense.description} | "
                f"{expense.category} | {expense.price:.2f} € | "
                f"{expense.quantity} | "
                f"{expense.calculate_total():.2f} € | {expense.date}"
            )

    def category_total(self):
        category = input("Enter category: ").strip().lower()

        if not is_valid_category(category):
            print("Invalid category.")
            return

        expenses = self.database.get_all_expenses()

        matching_expenses = [
            expense for expense in expenses
            if expense.category.strip().lower() == category
        ]

        if not matching_expenses:
            print("No expenses found in this category.")
            return

        total = sum(
            expense.calculate_total()
            for expense in matching_expenses
        )

        print(f"Total for {category}: {total:.2f} €")


    def sort_expenses(self):
        expenses = self.database.get_all_expenses()

        if not expenses:
            print("No expenses found.")
            return

        print("1. Ascending (lowest to highest)")
        print("2. Descending (highest to lowest)")

        choice = input("Choose sorting order: ")

        if choice == "1":
            reverse = False
        elif choice == "2":
            reverse = True
        else:
            print("Invalid choice.")
            return

        sorted_expenses = sorted(
            expenses,
            key=lambda expense: expense.calculate_total(),
            reverse=reverse
        )

        for expense in sorted_expenses:
            print(
                f"{expense.id} | {expense.description} | "
                f"{expense.category} | {expense.price:.2f} € | "
                f"{expense.quantity} | "
                f"{expense.calculate_total():.2f} € | {expense.date}"
            )


    def update_expenses(self):
        expense_id = input("Enter the ID of the expense to update: ").strip()

        expenses = self.database.get_all_expenses()

        expense_to_update = next(
            (expense for expense in expenses
             if str(expense.id) == expense_id),
            None
        )

        if expense_to_update is None:
            print("Expense not found.")
            return

        try:
            quantity = int(input("Enter the new quantity: "))

            if not is_valid_quantity(quantity):
                print("Quantity must be greater than zero.")
                return

        except ValueError:
            print("Please enter a valid whole number.")
            return

        expense_to_update.quantity = quantity
        self.database.update_expense(expense_to_update)

        print("Expense updated successfully.")


    def delete_expense(self):
        expense_id = input("Enter the ID of the expense to delete: ").strip()

        expenses = self.database.get_all_expenses()

        expense_to_delete = next(
            (expense for expense in expenses
             if str(expense.id) == expense_id),
            None
        )

        if expense_to_delete is None:
            print("Expense not found.")
            return

        self.database.delete_expense(expense_to_delete.id)

        print("Expense deleted successfully.")


    def add_expense(self):
        description = input("Enter expense description: ").strip()

        if not description:
            print("Description cannot be empty.")
            return

        
        category = input("Enter category: ").strip().lower()

        if not is_valid_category(category):
            print("Invalid category.")
            return

        category = categories[category]


        try:
            price = float(input("Enter price: "))

            if not is_valid_price(price):
                print("Price must be greater than zero.")
                return

            quantity = int(input("Enter quantity: "))

            if not is_valid_quantity(quantity):
                print("Quantity must be greater than zero.")
                return

        except ValueError:
            print("Please enter valid numeric values.")
            return

        date = input("Enter date (YYYY-MM-DD): ").strip()

        if not is_valid_date(date):
            print("Invalid date. Use YYYY-MM-DD.")
            return

        expense = Expense(
            description=description,
            category=category,
            price=price,
            quantity=quantity,
            date=date
        )

        self.database.add_expense(expense)

        print("Expense added successfully.")


    def run(self):
        while True:
            print("1. Add expenses")
            print("2. View expenses")
            print("3. Show total")
            print("4. Search expenses")
            print("5. Exit")
            print("6. Update expenses")
            print("7. Delete expenses")
            print("8. Category total")
            print("9. Sort expenses")

            choice = input("Choose an option: ")

            if choice == "1":
                self.add_expense()
            elif choice == "2":
                self.view_expense()
            elif choice == "3":
                self.show_total()
            elif choice == "4":
                self.search_expenses()
            elif choice == "5":
                print("Goodbye!")
                break
            elif choice == "6":
                self.update_expenses()
            elif choice == "7":
                self.delete_expense()
            elif choice == "8":
                self.category_total()
            elif choice == "9":
                self.sort_expenses()
            else:
                print("Invalid choice. Please choose 1-9.")


categories = {
    'food':"Food",
    'transport':"Transport",
    'clothing':"Clothing",
    'education':"Education",
    'entertainment':"Entertainment",
    'accessories':"Accessories",
    'electronics':"Electronics",
    'beauty':"Beauty",
    'other':"Other"
}


if __name__ == "__main__":
    database = DatabaseManager()
    database.create_table()

    tracker = ExpenseTracker(database)

    try:
        tracker.run()
    finally:
        database.close()
