# Expense Tracker

A command-line personal expense manager in Python with user accounts, SQLite storage, reports and CSV export.

## Features
- Register / login (salted PBKDF2 password hashing)
- Add, view, edit, delete expenses (each user sees only their own)
- Filter by category, overall summary, monthly report
- Export to CSV
- Input validation everywhere, activity logging to `data/app.log`

## Requirements
Python 3.8+. The app uses only the standard library. `pytest` is optional (for running tests).

## Setup and run
```bash
git clone https://github.com/<your-username>/expense-tracker.git
cd expense-tracker
python main.py
```

## Run tests
```bash
python -m unittest discover -s tests -t .
# or: pip install -r requirements.txt && pytest tests/
```

## Project structure
```
main.py            CLI menus
src/database.py    SQLite connection + schema
src/validators.py  input validation
src/logger.py      logging
src/auth.py        register / login
src/expenses.py    CRUD
src/reports.py     summaries
src/exporter.py    CSV export
tests/test_app.py  unit tests
docs/diagrams/     Mermaid diagram sources
docs/screenshots/  screenshots for the report
```

## Usage example
Register, log in, choose `1` to add an expense (amount, category, date, description), `6` for a summary, `7` for a monthly report (`YYYY-MM`), `8` to export.

## Author
Pawan Pal
26BAI10892
