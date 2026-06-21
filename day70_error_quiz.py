# Day 70 - Error Finding Quiz

import sqlite3
from pathlib import Path
import tempfile

def create_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT NOT NULL,
            dept    TEXT NOT NULL,
            salary  REAL NOT NULL
        )
    """)
    conn.commit()

def insert_employee(conn, name, dept, salary):
    conn.execute(
        "INSERT INTO employees (name, dept, salary) VALUES (?, ?, ?)",
        (name, dept, salary)
    )
    conn.commit()

def get_all(conn):
    cursor = conn.execute("SELECT * FROM employees")
    return cursor.fetchall

def get_by_dept(conn, dept):
    cursor = conn.execute(
        f"SELECT * FROM employees WHERE dept = '{dept}'"  # Bug 2 - SQL injection
    )
    return cursor.fetchall()

def update_salary(conn, emp_id, new_salary):
    conn.execute(
        "UPDATE employees SET salary = ? WHERE id = ?",
        (emp_id, new_salary)           # Bug 3 - parameters in wrong order
    )
    conn.commit()

with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
    db_path = f.name

conn = sqlite3.connect(db_path)
create_table(conn)
insert_employee(conn, "Alice", "Engineering", 75000)
insert_employee(conn, "Bob", "Marketing", 55000)
rows = get_all(conn)
print(rows)   # Bug 1 - fetchall missing (), returns method not results
conn.close()