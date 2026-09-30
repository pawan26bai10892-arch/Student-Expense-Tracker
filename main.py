"""Expense Tracker - command line application."""
from datetime import date

from src import auth, expenses, exporter, reports
from src.database import get_connection
from src.validators import CATEGORIES


def ask(prompt):
    return input(prompt).strip()


def show(rows):
    if not rows:
        print("No expenses found.")
        return
    print(f"{'ID':<5}{'Date':<12}{'Category':<15}{'Amount':>10}  Description")
    for r in rows:
        print(f"{r['id']:<5}{r['date']:<12}{r['category']:<15}{r['amount']:>10.2f}  {r['description']}")


def get_int(prompt):
    try:
        return int(ask(prompt))
    except ValueError:
        raise ValueError("Please enter a whole number.")


def add(conn, uid):
    print("Categories:", ", ".join(CATEGORIES))
    expenses.add_expense(conn, uid, ask("Amount: "), ask("Category: "),
                         ask(f"Date [{date.today()}]: ") or str(date.today()), ask("Description: "))
    print("Expense added.")


def edit(conn, uid):
    eid = get_int("Expense ID: ")
    expenses.update_expense(conn, uid, eid, ask("New amount: "), ask("New category: "),
                            ask("New date (YYYY-MM-DD): "), ask("New description: "))
    print("Expense updated.")


def delete(conn, uid):
    expenses.delete_expense(conn, uid, get_int("Expense ID: "))
    print("Expense deleted.")


def summary(conn, uid):
    print(f"Total spent: {reports.total_spent(conn, uid):.2f}")
    for c, t, n in reports.by_category(conn, uid):
        print(f"  {c:<15}{t:>10.2f} ({n})")


def export(conn, uid):
    path, n = exporter.export_csv(conn, uid)
    print(f"Exported {n} expenses to {path}")


ACTIONS = {
    "1": add,
    "2": lambda c, u: show(expenses.list_expenses(c, u)),
    "3": edit,
    "4": delete,
    "5": lambda c, u: show(expenses.list_expenses(c, u, ask("Category: "))),
    "6": summary,
    "7": lambda c, u: print(reports.format_report(reports.monthly_report(c, u, ask("Month (YYYY-MM): ")))),
    "8": export,
}

MENU = """
===== EXPENSE TRACKER =====
1. Add expense      5. Filter by category
2. View expenses    6. Summary
3. Edit expense     7. Monthly report
4. Delete expense   8. Export to CSV
9. Logout"""


def user_menu(conn, uid):
    while True:
        print(MENU)
        choice = ask("Choose: ")
        if choice == "9":
            return
        action = ACTIONS.get(choice)
        if not action:
            print("Invalid choice.")
            continue
        try:
            action(conn, uid)
        except ValueError as e:
            print("Error:", e)


def main():
    conn = get_connection()
    while True:
        print("\n1. Login\n2. Register\n3. Exit")
        try:
            choice = ask("Choose: ")
            if choice == "1":
                user_menu(conn, auth.login(conn, ask("Username: "), ask("Password: ")))
            elif choice == "2":
                auth.register(conn, ask("Username: "), ask("Password: "))
                print("Registered. You can log in now.")
            elif choice == "3":
                print("Goodbye!")
                return
            else:
                print("Invalid choice.")
        except ValueError as e:
            print("Error:", e)
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return


if __name__ == "__main__":
    main()
