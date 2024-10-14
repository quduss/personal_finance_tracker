# Personal Finance Tracker

A web-based application to help users manage their personal finances by tracking income and expenses. Users can add, edit, delete, and filter transactions. The app is built with Flask and SQLAlchemy, with a focus on simplicity and user-friendliness.

## Features
- **Add Transactions**: Users can add transactions with a description, amount, category, and type (Income/Expense).
- **Edit Transactions**: Users can modify existing transactions.
- **Delete Transactions**: Users can delete transactions they no longer need.
- **Transaction Filtering**: Filter transactions by date, category, and transaction type.
- **User Authentication**: Register and log in to access personal financial data.
- **Dashboard**: A simple dashboard to view, filter, and manage transactions.

## Technologies Used
- **Flask**: Backend framework used to build the web application.
- **SQLAlchemy**: ORM for handling the SQLite database.
- **WTForms**: Form handling and validation.
- **Flask-Login**: User authentication management.
- **Flask-Migrate**: Database migrations.
- **SQLite**: Database for storing transactions and user information.

## Setup and Installation
### Prerequisites
Before you begin, ensure you have the following installed on your machine:
* Python 3.x
* pip3 (Python package installer)
### Clone the Repository
```
git clone https://github.com/quduss/personal_finance_tracker.git
cd personal_finance_tracker
```
### Set Up Virtual Environment (Optional but Recommended)
```
python3 -m venv venv
source venv/bin/activate
```
### Install Dependencies
```
pip install -r requirements.txt
```
### Set Up the Database
To set up the database for the first time, run the following commands:
```
flask db init - should be run only once!
flask db migrate
flask db upgrade
```
This will create the necessary tables for the application.
### Running the Application
To start the application on localhost port 5000, use the command:
```
python3 app.py
```
## Usage
Go to the dashboard -> http://127.0.0.1:5000/dashboard

