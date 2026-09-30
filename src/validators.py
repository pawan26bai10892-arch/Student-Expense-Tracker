"""Input validation helpers. Each raises ValueError on bad input."""
import re
from datetime import datetime

CATEGORIES = ["Food", "Transport", "Rent", "Shopping", "Health", "Bills", "Entertainment", "Other"]


def validate_username(name):
    name = (name or "").strip()
    if not re.fullmatch(r"[A-Za-z0-9_]{3,20}", name):
        raise ValueError("Username must be 3-20 letters, digits or underscores.")
    return name


def validate_password(pw):
    if not pw or len(pw) < 6:
        raise ValueError("Password must be at least 6 characters.")
    return pw


def validate_amount(value):
    try:
        amount = round(float(value), 2)
    except (TypeError, ValueError):
        raise ValueError("Amount must be a number.")
    if amount <= 0 or amount > 10_000_000:
        raise ValueError("Amount must be greater than 0 and at most 10,000,000.")
    return amount


def validate_date(value):
    try:
        return datetime.strptime((value or "").strip(), "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format.")


def validate_category(value):
    for c in CATEGORIES:
        if (value or "").strip().lower() == c.lower():
            return c
    raise ValueError("Category must be one of: " + ", ".join(CATEGORIES))


def validate_month(value):
    try:
        return datetime.strptime((value or "").strip(), "%Y-%m").strftime("%Y-%m")
    except ValueError:
        raise ValueError("Month must be in YYYY-MM format.")
