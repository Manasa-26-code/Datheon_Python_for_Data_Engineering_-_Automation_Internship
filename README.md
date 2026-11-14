# Datheon Task 3 – Relational Database Auto-Ingestion & Upsert Engine

## Requirements
Python 3.8+; no extra packages required.

## Run
Open a terminal in this folder:
```bash
python main.py
python verify_db.py
```

## Features
- Creates a SQLite database and employees table.
- Reads `data/employees.csv`.
- Normalizes emails, department names, salaries and dates.
- Validates fields and logs invalid rows.
- Uses `ON CONFLICT ... DO UPDATE` for UPSERT.
- Uses a transaction to protect batch loading.
- Saves logs in `logs/ingestion.log`.

## Demonstrate UPSERT
Change employee 101 salary in the CSV from `$75,000` to `$78,000`, save, run `python main.py` again, then run `python verify_db.py`. Employee 101 should be updated, not duplicated.

## Evidence
Capture screenshots of the project folder, successful main.py run, successful verification and UPSERT demonstration. Upload the project to a public GitHub repository using the exact name required by your Datheon dashboard, then paste its URL into the Datheon submission form.
