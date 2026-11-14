import sqlite3
from pathlib import Path
db = Path(__file__).resolve().parent / "database" / "company.db"
if not db.exists():
    raise SystemExit("Database not found. Run: python main.py")
with sqlite3.connect(db) as con:
    total = con.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
    unique_ids = con.execute("SELECT COUNT(DISTINCT employee_id) FROM employees").fetchone()[0]
    missing = con.execute("""SELECT COUNT(*) FROM employees
        WHERE full_name IS NULL OR email IS NULL OR department IS NULL OR joining_date IS NULL""").fetchone()[0]
    negative = con.execute("SELECT COUNT(*) FROM employees WHERE salary < 0").fetchone()[0]
print("DATABASE VERIFICATION REPORT")
print("----------------------------")
print(f"Total employee rows: {total}")
print(f"Distinct employee IDs: {unique_ids}")
print(f"Rows missing required values: {missing}")
print(f"Rows with negative salary: {negative}")
assert total > 0 and total == unique_ids and missing == 0 and negative == 0
print("\\nPASS: All database verification checks succeeded.")
