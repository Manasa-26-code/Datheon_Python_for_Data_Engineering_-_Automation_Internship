CREATE TABLE IF NOT EXISTS employees (
 employee_id INTEGER PRIMARY KEY, full_name TEXT NOT NULL,
 email TEXT NOT NULL UNIQUE, department TEXT NOT NULL,
 salary REAL NOT NULL CHECK(salary >= 0),
 joining_date TEXT NOT NULL, updated_at TEXT NOT NULL
);
