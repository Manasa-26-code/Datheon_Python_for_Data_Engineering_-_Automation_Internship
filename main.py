import csv, logging, sqlite3
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
CSV_FILE = ROOT / "data" / "employees.csv"
DB_FILE = ROOT / "database" / "company.db"
LOG_FILE = ROOT / "logs" / "ingestion.log"

def main():
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                        format="%(asctime)s | %(levelname)s | %(message)s")
    con = sqlite3.connect(DB_FILE)
    try:
        con.execute("""CREATE TABLE IF NOT EXISTS employees (
            employee_id INTEGER PRIMARY KEY, full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE, department TEXT NOT NULL,
            salary REAL NOT NULL CHECK(salary >= 0),
            joining_date TEXT NOT NULL, updated_at TEXT NOT NULL)""")
        loaded = skipped = 0
        with con:
            with CSV_FILE.open(newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                required = {"employee_id","full_name","email","department","salary","joining_date"}
                if not reader.fieldnames or not required.issubset(reader.fieldnames):
                    raise ValueError("CSV is missing required columns.")
                for line, r in enumerate(reader, 2):
                    try:
                        emp_id = int(r["employee_id"].strip())
                        name = r["full_name"].strip()
                        email = r["email"].strip().lower()
                        dept = r["department"].strip().title()
                        salary = float(r["salary"].replace("$","").replace(",","").strip())
                        raw_date = r["joining_date"].strip()
                        try:
                            date = datetime.strptime(raw_date, "%Y-%m-%d").date().isoformat()
                        except ValueError:
                            date = datetime.strptime(raw_date, "%d-%m-%Y").date().isoformat()
                        if emp_id <= 0 or not name or "@" not in email or not dept or salary < 0:
                            raise ValueError("Invalid required field or value.")
                        con.execute("""INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?)
                            ON CONFLICT(employee_id) DO UPDATE SET
                            full_name=excluded.full_name, email=excluded.email,
                            department=excluded.department, salary=excluded.salary,
                            joining_date=excluded.joining_date, updated_at=excluded.updated_at""",
                            (emp_id,name,email,dept,salary,date,datetime.now().isoformat(timespec="seconds")))
                        loaded += 1
                    except (ValueError, KeyError) as e:
                        logging.warning("Skipping CSV row %s: %s", line, e)
                        skipped += 1
        print("Employee records:")
        for row in con.execute("SELECT employee_id, full_name, email, department, salary, joining_date FROM employees ORDER BY employee_id"):
            print(row)
        print(f"\\nThis run: {loaded} inserted/updated; {skipped} skipped.")
        print(f"Database: {DB_FILE}")
        print(f"Log: {LOG_FILE}")
        logging.info("Ingestion completed: %s loaded/updated, %s skipped", loaded, skipped)
    except Exception:
        logging.exception("Ingestion failed; transaction rolled back")
        raise
    finally:
        con.close()

if __name__ == "__main__":
    main()
