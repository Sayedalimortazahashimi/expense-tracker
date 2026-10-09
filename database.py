import sqlite3
from models import Expense

class DatabaseManager:
    def __init__(self, database_name="expenses.db"):
        self.connection = sqlite3.connect(database_name)

    def create_table(self):
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                description TEXT,
                category TEXT,
                price REAL,
                quantity INTEGER,
                date TEXT
            )
        """)
        self.connection.commit()
    def add_expense(self, expense):
        cursor = self.connection.execute("""
            INSERT INTO expenses
            (description, category, price, quantity, date)
            VALUES (?, ?, ?, ?, ?)
        """, (
            expense.description,
            expense.category,
            expense.price,
            expense.quantity,
            expense.date
        ))
        self.connection.commit()
        return cursor.lastrowid


    def get_all_expenses(self):
        result = self.connection.execute("""
            SELECT id, description, category, price, quantity, date
            FROM expenses
        """)
        rows = result.fetchall()

        return [
            Expense(
                description=row[1],
                category=row[2],
                price=row[3],
                quantity=row[4],
                date=row[5],
                expense_id=row[0]
            )
            for row in rows
        ]


    def update_expense(self, expense):
        self.connection.execute("""
            UPDATE expenses
            SET description = ?, category = ?, price = ?,
                quantity = ?, date = ?
            WHERE id = ?
        """, (
            expense.description,
            expense.category,
            expense.price,
            expense.quantity,
            expense.date,
            expense.id
        ))
        self.connection.commit()


    def delete_expense(self, expense_id):
        self.connection.execute("""
            DELETE FROM expenses
            WHERE id = ?
        """, (expense_id,))
        self.connection.commit()
    def close(self):
        self.connection.close()