import unittest
import sqlite3
from database import DatabaseManager
from models import Expense
from expense_tracker import (
    calculate_total,
    is_valid_price,
    is_valid_quantity,
    is_valid_category,
    is_valid_date,
    categories
)

class TestExpenseTracker(unittest.TestCase):
    def test_integer_total(self):
        self.assertEqual(calculate_total(10, 3), 30)

    def test_decimal_price(self):
        self.assertEqual(calculate_total(24.99, 1), 24.99)

    def test_multiple_quantity(self):
        self.assertEqual(calculate_total(1.99, 3), 5.97)

    def test_whole_number(self):
        self.assertEqual(calculate_total(75,1), 75)

    def test_valid_price(self):
        self.assertTrue(is_valid_price(12.50))

    def test_invalid_prices(self):
        self.assertFalse(is_valid_price(0))
        self.assertFalse(is_valid_price(-5))

    def test_valid_quantity(self):
        self.assertTrue(is_valid_quantity(3))

    def test_invalid_quantities(self):
        self.assertFalse(is_valid_quantity(0))
        self.assertFalse(is_valid_quantity(-2))

    def test_valid_category(self):
        self.assertTrue(is_valid_category("Food"))
        self.assertTrue(is_valid_category("  FOOD "))

    def test_invalid_category(self):
        self.assertFalse(is_valid_category("Shoes"))

    def test_valid_date(self):
        self.assertTrue(is_valid_date("2026-10-09"))

    def test_invalid_dates(self):
        self.assertFalse(is_valid_date("2026-02-30"))
        self.assertFalse(is_valid_date("09-10-2026"))

    def test_database_connection(self):
        self.assertIsNotNone(self.connection)
    

    def test_create_expenses_table(self):
        result = self.connection.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name = 'expenses'
        """)

        self.assertIsNotNone(result.fetchone())

    def test_insert_and_read_expense(self):
        database = DatabaseManager(":memory:")
        database.create_table()

        expense = Expense(
            description="Coffee",
            category="Food",
            price=2.5,
            quantity=2,
            date="2026-10-09"
        )

        expense.id = database.add_expense(expense)

        expenses = database.get_all_expenses()

        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0].description, "Coffee")
        self.assertEqual(expenses[0].category, "Food")
        self.assertAlmostEqual(expenses[0].price, 2.50)
        self.assertEqual(expenses[0].quantity, 2)
        self.assertEqual(expenses[0].date, "2026-10-09")

        database.close()
    
    def test_update_expense(self):
  
        self.connection.execute("""
            INSERT INTO expenses
            (description, category, price, quantity, date)
            VALUES (?, ?, ?, ?, ?)
        """, ("Coffee", "Food", 2.50, 2, "2026-10-09"))

        self.connection.execute("""
            UPDATE expenses
            SET quantity = ?
            WHERE id = ?
        """, (5, 1))

        result = self.connection.execute("""
            SELECT quantity
            FROM expenses
            WHERE id = ?
        """, (1,))

        row = result.fetchone()

        self.assertEqual(row[0], 5)

    
    def test_delete_expense(self):

        self.connection.execute("""
            INSERT INTO expenses
            (description, category, price, quantity, date)
            VALUES (?, ?, ?, ?, ?)
        """, ("Coffee", "Food", 2.50, 2, "2026-10-09"))

        self.connection.execute("""
            DELETE FROM expenses
            WHERE id = ?
        """, (1,))

        result = self.connection.execute("""
            SELECT * FROM expenses
            WHERE id = ?
        """, (1,))

        row = result.fetchone()

        self.assertIsNone(row)


    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        
        self.connection.execute("""
        CREATE TABLE expenses (
            id INTEGER PRIMARY KEY,
            description TEXT,
            category TEXT,
            price REAL,
            quantity INTEGER,
            date TEXT
        )
    """)

    def tearDown(self):
        self.connection.close()

    def test_database_starts_empty(self):
        result = self.connection.execute("""
            SELECT COUNT(*)
            FROM expenses
        """)

        row = result.fetchone()

        self.assertEqual(row[0], 0)

    def test_each_test_has_fresh_database(self):
        self.connection.execute("""
            INSERT INTO expenses
            (description, category, price, quantity, date)
            VALUES (?, ?, ?, ?, ?)
        """, ("Coffee", "Food", 2.50, 1, "2026-10-09"))

        result = self.connection.execute("""
            SELECT COUNT(*)
            FROM expenses
        """)

        self.assertEqual(result.fetchone()[0], 1)

    def test_category_display_name(self):
        self.assertEqual(categories["food"], "Food")
        self.assertEqual(categories["education"], "Education")
        self.assertEqual(categories["electronics"], "Electronics")

if __name__ == "__main__":
    unittest.main()