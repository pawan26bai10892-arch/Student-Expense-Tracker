"""CRUD operations on expenses (always scoped to a user)."""
from .logger import get_logger
from .validators import validate_amount, validate_category, validate_date

log = get_logger()


def add_expense(conn, user_id, amount, category, date, description=""):
    cur = conn.execute(
        "INSERT INTO expenses(user_id,amount,category,description,date) VALUES(?,?,?,?,?)",
        (user_id, validate_amount(amount), validate_category(category),
         (description or "").strip()[:100], validate_date(date)))
    conn.commit()
    log.info("expense added id=%s user=%s", cur.lastrowid, user_id)
    return cur.lastrowid


def list_expenses(conn, user_id, category=None):
    sql, args = "SELECT * FROM expenses WHERE user_id=?", [user_id]
    if category:
        sql += " AND category=?"
        args.append(validate_category(category))
    return conn.execute(sql + " ORDER BY date DESC, id DESC", args).fetchall()


def update_expense(conn, user_id, expense_id, amount, category, date, description=""):
    cur = conn.execute(
        "UPDATE expenses SET amount=?,category=?,description=?,date=? WHERE id=? AND user_id=?",
        (validate_amount(amount), validate_category(category), (description or "").strip()[:100],
         validate_date(date), expense_id, user_id))
    conn.commit()
    if cur.rowcount == 0:
        raise ValueError("Expense not found.")
    log.info("expense updated id=%s", expense_id)


def delete_expense(conn, user_id, expense_id):
    cur = conn.execute("DELETE FROM expenses WHERE id=? AND user_id=?", (expense_id, user_id))
    conn.commit()
    if cur.rowcount == 0:
        raise ValueError("Expense not found.")
    log.info("expense deleted id=%s", expense_id)
