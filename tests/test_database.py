import os
import tempfile
import unittest

from database import DatabaseManager
from models import Expense

class TestDatabaseManager(unittest.TestCase):
    def test_create_table(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            database_path = os.path.join(temp_dir, "test_expenses.db")
            database = DatabaseManager(database_path)

            try:
                database.create_table()

                result = database.connection.execute("""
                    SELECT name
                    FROM sqlite_master
                    WHERE type = 'table' AND name = 'expenses'
                """)

                self.assertIsNotNone(result.fetchone())
            finally:
                database.close()

    def test_add_expense(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            database_path = os.path.join(temp_dir, "test_expenses.db")
            database = DatabaseManager(database_path)

            try:
                database.create_table()

                expense = Expense(
                    "Coffee", "Food", 2.5, 2, "2026-10-09"
                )

                expense_id = database.add_expense(expense)

                self.assertIsNotNone(expense_id)
                self.assertGreater(expense_id, 0)
            finally:
                database.close()


    def test_get_all_expenses(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            database_path = os.path.join(temp_dir, "test_expenses.db")
            database = DatabaseManager(database_path)

            try:
                database.create_table()

                expense = Expense(
                    "Coffee", "Food", 2.5, 2, "2026-10-09"
                )
                database.add_expense(expense)

                expenses = database.get_all_expenses()

                self.assertEqual(len(expenses), 1)
                self.assertEqual(expenses[0].description, "Coffee")
                self.assertEqual(expenses[0].category, "Food")
                self.assertEqual(expenses[0].calculate_total(), 5.0)
                self.assertGreater(expenses[0].id, 0)
            finally:
                database.close()

    def test_update_expense(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            database_path = os.path.join(temp_dir, "test_expenses.db")
            database = DatabaseManager(database_path)

            try:
                database.create_table()

                expense = Expense(
                    "Coffee", "Food", 2.5, 2, "2026-10-09"
                )
                expense.id = database.add_expense(expense)

                expense.description = "Tea"
                expense.price = 1.5

                database.update_expense(expense)

                updated = database.get_all_expenses()[0]
                self.assertEqual(updated.description, "Tea")
                self.assertEqual(updated.price, 1.5)
            finally:
                database.close()


    def test_delete_expense(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            database_path = os.path.join(temp_dir, "test_expenses.db")
            database = DatabaseManager(database_path)

            try:
                database.create_table()

                expense = Expense(
                    "Coffee", "Food", 2.5, 2, "2026-10-09"
                )
                expense_id = database.add_expense(expense)

                database.delete_expense(expense_id)

                self.assertEqual(database.get_all_expenses(), [])
            finally:
                database.close()

if __name__ == "__main__":
    unittest.main()