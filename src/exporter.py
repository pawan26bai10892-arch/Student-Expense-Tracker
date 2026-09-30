"""Export expenses to CSV."""
import csv
import os

from .expenses import list_expenses


def export_csv(conn, user_id, path="exports/expenses.csv"):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    rows = list_expenses(conn, user_id)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "date", "category", "amount", "description"])
        for r in rows:
            w.writerow([r["id"], r["date"], r["category"], f"{r['amount']:.2f}", r["description"]])
    return path, len(rows)
