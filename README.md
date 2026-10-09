# Python Expense Tracker

A command-line expense tracking application built with Python and SQLite.

The application allows users to add, view, search, update, and delete expenses, calculate totals, filter expenses by category, and sort expenses by total amount. Expense data is stored in an SQLite database so it remains available after the application is closed.

## Requirements

-Python 3.10 or newer
-SQLite (included with Python's standard library)

## How to Run

1.Clone or download this repository.
2.Open a terminal in the project folder.
3.Run the application:

python expense_tracker.py

The application will create or use the expenses.db database file to store expenses.

## Running the Tests

Run the automated tests with:

python -m unittest discover -s tests -v

## Features

-Add new expenses with a description, category, price, quantity, and date
-View saved expenses
-Search for expenses
-Update existing expenses
-Delete expenses
-Calculate the total amount of expenses
-Calculate totals by category
-Sort expenses by total amount in ascending or descending order
-Validate user input, including prices, quantities, categories, and dates
-Store expense data persistently using SQLite
-Run automated unit tests with Python's unittest framework

## Project Structure

expense-tracker/
├── expense_tracker.py
├── expenses.db
├── README.md
└── tests/
└── test_expense_tracker.py

## Technologies Used

-Python
-SQLite
-SQL
-unittest

## What I Learned

Through this project, I practiced:

-Writing reusable functions
-Working with databases and SQL queries
-Implementing CRUD operations (Create, Read, Update, Delete)
-Validating user input and handling errors
-Writing automated unit tests
-Organizing a Python project
