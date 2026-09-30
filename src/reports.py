"""Summaries and reports."""
from .validators import validate_month


def total_spent(conn, user_id):
    return conn.execute("SELECT COALESCE(SUM(amount),0) FROM expenses WHERE user_id=?", (user_id,)).fetchone()[0]


def by_category(conn, user_id):
    rows = conn.execute("SELECT category, SUM(amount) t, COUNT(*) n FROM expenses WHERE user_id=? "
                        "GROUP BY category ORDER BY t DESC", (user_id,)).fetchall()
    return [(r["category"], r["t"], r["n"]) for r in rows]


def monthly_report(conn, user_id, month):
    month = validate_month(month)
    rows = conn.execute("SELECT * FROM expenses WHERE user_id=? AND substr(date,1,7)=? ORDER BY date",
                        (user_id, month)).fetchall()
    total = sum(r["amount"] for r in rows)
    cats = {}
    for r in rows:
        cats[r["category"]] = cats.get(r["category"], 0) + r["amount"]
    return {"month": month, "total": total, "count": len(rows),
            "categories": sorted(cats.items(), key=lambda x: -x[1])}


def format_report(rep):
    lines = [f"Report for {rep['month']}", "-" * 34]
    for c, t in rep["categories"]:
        pct = t / rep["total"] * 100 if rep["total"] else 0
        lines.append(f"{c:<15}{t:>10.2f}  {pct:5.1f}%")
    lines += ["-" * 34, f"{'TOTAL':<15}{rep['total']:>10.2f}  ({rep['count']} items)"]
    return "\n".join(lines)
