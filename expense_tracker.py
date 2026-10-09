import sqlite3
from datetime import datetime

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

def insert_expense(connection, description, category, price, quantity, date):
    connection.execute("""
        INSERT INTO expenses
        (description, category, price, quantity, date)
        VALUES (?, ?, ?, ?, ?)
    """, (description, category, price, quantity, date))

    connection.commit()
connection = sqlite3.connect("expenses.db")

connection.execute("""
    CREATE TABLE IF NOT EXISTS expenses(
    id INTEGER PRIMARY KEY,
    description TEXT,
    category TEXT,
    price REAL,
    quantity INTEGER,
    date TEXT
    )
""")

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

def add_expense():
    description = input("Description: ")
    while True:
        category = input("Category: ").strip().lower()
        if is_valid_category(category):
            category = categories[category]
            break
        else:
            print("Invalid category")
    while True:
        try:
            price = float(input("Price: "))
            if not is_valid_price(price):
                print("Price must be greater than 0!")
                continue
            break
        except ValueError:
            print("Enter a valid number!")
    while True:
        try:
            quantity = int(input("Quantity: "))
            if not is_valid_quantity(quantity):
                print("Quantity must be greater than 0!")
                continue
            break
        except ValueError:
            print("Please enter a valid integer!")

    while True:
        date = input("Date: ")
        if is_valid_date(date):
            break
        else:
            print("Invalid date! Use YYYY-MM-DD.")


    insert_expense(
        connection,
        description,
        category,
        price,
        quantity,
        date
    )

def view_expense():
    result = connection.execute("""
        SELECT *
        FROM expenses
        """
      )
    rows = result.fetchall()
    if not rows:
        print("No expenses found.")
        return
    print("ID | Description | Category | Price | Qty | Total | Date")
    print("-" * 65)
    for row in rows:
        total = calculate_total(row[3],row[4])
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]:.2f} € | {row[4]} | {total:.2f} € | {row[5]}")


def show_total():
    result = connection.execute("""
        SELECT SUM( price * quantity) AS total
        FROM expenses
        """)
    row = result.fetchone()
    total = row[0]
    if total is None:
        print("No expense found!")
        return
    print(f"{total:.2f} €")

def search_expenses():
    while True:
        category = input("Category: ").strip().lower()

        if category in categories:
            category = categories[category]
            break
        else:
            print("Invalid category")
            
    result = connection.execute("""
        SELECT *
        FROM expenses
        WHERE category = ?
        """,(category,))
    rows = result.fetchall()
    if not rows:
        print("No expenses found!")
        return
    print("ID | Description | Category | Price | Qty | Total | Date")
    print("-" * 65)
    for row in rows:
        total = calculate_total(row[3], row[4])
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]:.2f} € | {row[4]} | {total:.2f} € | {row[5]}")

def update_expenses():
    
    expense_id = input("Enter your ID:")
    result = connection.execute("""
    SELECT id
    FROM expenses
    WHERE id = ?
""", (expense_id,))
    row = result.fetchone()
    if row is None:
        print("Expense not found!")
        return
    while True:
        try:
            quantity = int(input("New quantity: "))
            if quantity <= 0:
                print("Quantity must be greater than 0!")
                continue
            break
        except ValueError:
            print("Please enter a valid integer!")
    connection.execute("""
    UPDATE expenses
    SET quantity = ?
    WHERE id = ?
    """, (quantity, expense_id))
    
    connection.commit()

    

def delete_expense():
    expense_id = input("Enter your ID: ")
    result = connection.execute("""
        SELECT id
        FROM expenses
        WHERE id = ?
    """, (expense_id,))
    row = result.fetchone()
    if row is None:
        print("Expense not found!")
        return
    connection.execute("""
        DELETE FROM expenses
        WHERE id = ?
    """, (expense_id,))

    connection.commit()
    print("Expense deleted successfully!")

def category_total():
    while True:
        category = input("Category: ").strip().lower()

        if category in categories:
            category = categories[category]
            break
        else:
            print("Invalid category")
    result = connection.execute("""
    SELECT SUM(price * quantity)
    FROM expenses
    WHERE category = ?
    """, (category,))
    row = result.fetchone()
    total = row[0]
    if total is None:
        print("No expense found!")
    else:
        print(f"{total:.2f} €")

def sort_expenses():
    sort_choice = input("1. Highest first\n2. Lowest first\nChoose: ")
    sort_type = None
    if sort_choice == "1":
        sort_type = "DESC"
    elif sort_choice == "2":
        sort_type = "ASC"
    else:
        print("Invalid choice!")
        return
    result = connection.execute(f"""
        SELECT *
        FROM expenses
        ORDER BY price * quantity {sort_type}
    """)
    rows = result.fetchall()
    if not rows:
        print("No expenses found.")
        return
    print("ID | Description | Category | Price | Qty | Total | Date")
    print("-" * 65)
    for row in rows:
        total = calculate_total(row[3], row[4])
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]:.2f} € | {row[4]} | {total:.2f} € | {row[5]}")


def main():
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
            add_expense()
        elif choice == "2":
            view_expense()
        elif choice == "3":
            show_total()
        elif choice == "4":
            search_expenses()
        elif choice == "5":
            print("Goodbye!")
            break
        elif choice =="6":
            update_expenses()
        elif choice == "7":
            delete_expense()
        elif choice == "8":
            category_total()
        elif choice == "9":
            sort_expenses()
        else: 
            print("Invalid choice. Please choose 1-4.")

if __name__ == "__main__":
    try:
        main()
    finally:
        connection.close()

