
import unittest
from models import Expense


class TestExpense(unittest.TestCase):
    def test_calculate_total(self):
        expense = Expense(
            "Coffee",
            "Food",
            2.5,
            2,
            "2026-10-09"
        )

        self.assertEqual(expense.calculate_total(), 5.0)
    def test_expense_stores_id(self):
        expense = Expense(
            "Coffee", "Food", 2.5, 2, "2026-10-09", expense_id=1
        )

        self.assertEqual(expense.id, 1)

if __name__ == "__main__":
    unittest.main()