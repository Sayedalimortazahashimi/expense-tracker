class Expense:
    def __init__(
        self, description, category, price, quantity, date, expense_id=None
    ):
        self.id = expense_id
        self.description = description
        self.category = category
        self.price = price
        self.quantity = quantity
        self.date = date

    def calculate_total(self):
        return self.price * self.quantity