"""SQLite connection and schema."""
import os
import sqlite3

DEFAULT_DB = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "expenses.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    salt TEXT NOT NULL,
    password_hash TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    amount REAL NOT NULL CHECK(amount > 0),
    category TEXT NOT NULL,
    description TEXT DEFAULT '',
    date TEXT NOT NULL
);
"""


def get_connection(path=DEFAULT_DB):
    if path != ":memory:":
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    return conn
