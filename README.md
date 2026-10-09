# Python Expense Tracker

A command-line expense tracking application built with Python and SQLite. The project allows users to manage expenses, calculate spending totals, and store data persistently in a local database.

## Features

-Add expenses with a description, category, price, quantity, and date
-View all saved expenses
-Search for expenses
-Update existing expenses
-Delete expenses
-Calculate the total amount of all expenses
-Calculate spending totals by category
-Sort expenses by total amount in ascending or descending order
-Validate user input, including prices, quantities, categories, and dates
-Store expense data persistently using SQLite
-Run automated unit tests with Python's unittest framework

## Technologies Used

-Python — application logic and object-oriented programming
-SQLite — local database storage
-SQL — database queries and CRUD operations
-unittest — automated testing

## Requirements

-Python 3.10 or newer
-SQLite (included with Python's standard library)

## How to Run

1.Clone or download this repository.
2.Open a terminal in the project directory.
3.Run the application:

python expense_tracker.py

The application creates or uses an expenses.db file to store expenses. The database file is generated locally and is not included in the Git repository.

## Running the Tests

To run the automated test suite, execute:

python -m unittest discover -s tests -v

The tests cover expense calculations, input validation, database operations, and model behavior.

## Project Structure

expense-tracker/
├── expense_tracker.py
├── models.py
├── database.py
├── README.md
├── .gitignore
└── tests/
├── test_database.py
├── test_expense_tracker.py
└── test_models.py

## What I Learned

Through this project, I practiced:

-Organizing Python code using classes and methods
-Separating application logic, data models, and database operations
-Working with SQLite and SQL queries
-Implementing CRUD operations (Create, Read, Update, Delete)
-Validating user input and handling errors
-Writing automated unit tests
-Using Git and GitHub to track and publish a software project

## Future Improvements

-Improve monetary precision throughout the application
-Add more automated tests for user interactions and edge cases
-Improve the command-line interface and error messages
