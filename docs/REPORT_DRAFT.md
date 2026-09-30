# Expense Tracker - Project Report (Draft)
*Map these headings to the 15 sections in your instruction document; rename/reorder as needed. Add your name, registration number, screenshots and diagrams.*

## 1. Title and Author
Expense Tracker - Pawan Haddi, [Reg. No.], [Course], VIT

## 2. Abstract
Expense Tracker is a command-line application in Python that lets multiple users register, log in and record daily expenses. Data is stored in SQLite; users can filter, summarise, produce monthly reports and export to CSV. Passwords are salted and hashed, all input is validated, and 10 unit tests cover the core logic.

## 3. Introduction
Manual expense tracking is error-prone. This project offers a simple, private, offline alternative.

## 4. Problem Statement
See `statement.md`.

## 5. Objectives
- Secure multi-user access
- Reliable CRUD on expenses with validation
- Useful reports (category and monthly)
- Clean modular design with automated tests

## 6. Requirements
**Functional:** register, login, add/view/edit/delete, filter, summary, monthly report, CSV export.
**Non-functional:** security (hashed passwords), reliability (no crashes on bad input), maintainability (modules), portability (stdlib only).

## 7. System Design / Architecture
Layered design: CLI (`main.py`) -> business modules (`auth`, `expenses`, `reports`, `exporter`) -> `validators`, `logger`, `database`. Insert *architecture*, *workflow* and *use case* diagrams here.

## 8. Detailed Design
Insert *class*, *sequence* and *ER* diagrams. Tables: `users(id, username, salt, password_hash)`, `expenses(id, user_id, amount, category, description, date)`. Every expense query filters by `user_id` so users cannot access each other's data.

## 9. Implementation
Python 3, `sqlite3`, `hashlib.pbkdf2_hmac` (100,000 iterations), `csv`, `logging`. Parameterised SQL queries prevent SQL injection. Module-by-module description: see README structure.

## 10. Testing
`tests/test_app.py` - 10 tests: validators, auth (wrong password, duplicate user, hash not plaintext), CRUD, user isolation, filtering, reports, empty report, CSV export. All pass. *Insert test screenshot.*

## 11. Results and Screenshots
Insert screenshots: login menu, add expense, list, summary, monthly report, export, tests.

## 12. Challenges Faced
Handling invalid input without crashing (solved with `ValueError` and a single catch point in the menu); keeping users' data separate; deciding on password storage.

## 13. Limitations
CLI only; no currency support; no budgets; password reset not available.

## 14. Future Enhancements
GUI/web front end, budgets and alerts, charts, recurring expenses, password reset, import from CSV.

## 15. Conclusion and References
The project meets its objectives with a tested, modular design. References: Python docs (sqlite3, hashlib, unittest), SQLite docs, Mermaid docs.
