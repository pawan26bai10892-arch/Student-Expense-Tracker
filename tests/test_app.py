import os, tempfile, unittest
from src import auth, expenses, exporter, reports, validators as v
from src.database import get_connection


class ValidatorTests(unittest.TestCase):
    def test_amount(self):
        self.assertEqual(v.validate_amount("12.5"), 12.5)
        for bad in ["abc", "-5", "0", "", None]:
            with self.assertRaises(ValueError):
                v.validate_amount(bad)

    def test_date(self):
        self.assertEqual(v.validate_date("2025-01-31"), "2025-01-31")
        for bad in ["31-01-2025", "2025-02-30", ""]:
            with self.assertRaises(ValueError):
                v.validate_date(bad)

    def test_category(self):
        self.assertEqual(v.validate_category("food"), "Food")
        with self.assertRaises(ValueError):
            v.validate_category("Gold")

    def test_username_password_month(self):
        self.assertEqual(v.validate_username(" bob_1 "), "bob_1")
        for bad in ["ab", "bad name", "x" * 21]:
            with self.assertRaises(ValueError):
                v.validate_username(bad)
        with self.assertRaises(ValueError):
            v.validate_password("123")
        self.assertEqual(v.validate_month("2025-03"), "2025-03")
        with self.assertRaises(ValueError):
            v.validate_month("2025-13")


class AppTests(unittest.TestCase):
    def setUp(self):
        self.conn = get_connection(":memory:")
        self.uid = auth.register(self.conn, "alice", "secret1")

    def test_auth(self):
        self.assertEqual(auth.login(self.conn, "alice", "secret1"), self.uid)
        with self.assertRaises(ValueError):
            auth.login(self.conn, "alice", "wrong")
        with self.assertRaises(ValueError):
            auth.register(self.conn, "alice", "secret1")
        h = self.conn.execute("SELECT password_hash FROM users").fetchone()[0]
        self.assertNotIn("secret1", h)

    def test_crud(self):
        eid = expenses.add_expense(self.conn, self.uid, "50", "food", "2025-01-05", "lunch")
        self.assertEqual(len(expenses.list_expenses(self.conn, self.uid)), 1)
        expenses.update_expense(self.conn, self.uid, eid, "75", "Bills", "2025-01-06", "x")
        self.assertEqual(expenses.list_expenses(self.conn, self.uid)[0]["amount"], 75)
        expenses.delete_expense(self.conn, self.uid, eid)
        self.assertEqual(expenses.list_expenses(self.conn, self.uid), [])
        with self.assertRaises(ValueError):
            expenses.delete_expense(self.conn, self.uid, eid)

    def test_isolation_between_users(self):
        bob = auth.register(self.conn, "bobby", "secret2")
        eid = expenses.add_expense(self.conn, self.uid, 10, "Food", "2025-01-01")
        self.assertEqual(expenses.list_expenses(self.conn, bob), [])
        with self.assertRaises(ValueError):
            expenses.delete_expense(self.conn, bob, eid)

    def test_filter_and_reports(self):
        for a, c, d in [(100, "Food", "2025-01-02"), (50, "Food", "2025-01-09"),
                        (200, "Rent", "2025-01-10"), (30, "Food", "2025-02-01")]:
            expenses.add_expense(self.conn, self.uid, a, c, d)
        self.assertEqual(len(expenses.list_expenses(self.conn, self.uid, "food")), 3)
        self.assertEqual(reports.total_spent(self.conn, self.uid), 380)
        rep = reports.monthly_report(self.conn, self.uid, "2025-01")
        self.assertEqual((rep["total"], rep["count"]), (350, 3))
        self.assertEqual(rep["categories"][0], ("Rent", 200))
        self.assertIn("TOTAL", reports.format_report(rep))
        self.assertEqual(reports.by_category(self.conn, self.uid)[0][0], "Rent")

    def test_empty_report(self):
        rep = reports.monthly_report(self.conn, self.uid, "2030-01")
        self.assertEqual(rep["total"], 0)
        self.assertIn("TOTAL", reports.format_report(rep))

    def test_export(self):
        expenses.add_expense(self.conn, self.uid, 9.5, "Other", "2025-01-01", "pen")
        with tempfile.TemporaryDirectory() as d:
            path, n = exporter.export_csv(self.conn, self.uid, os.path.join(d, "o.csv"))
            self.assertEqual(n, 1)
            self.assertIn("9.50", open(path).read())


if __name__ == "__main__":
    unittest.main()
