# Day 70 - Clean sqlite3 CRUD operations
# New concepts: sqlite3, parameterised queries, context manager, Row factory
# PEP 8, docstrings, type hints, exceptions throughout

import sqlite3
from typing import List, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class Employee:
    """Represents an employee record."""
    name: str
    department: str
    salary: float
    id: Optional[int] = None

    def __str__(self) -> str:
        return (f"Employee(id={self.id}, name='{self.name}', "
                f"dept='{self.department}', salary=£{self.salary:,.0f})")


class EmployeeDB:
    """SQLite-backed employee database with full CRUD operations.

    Uses parameterised queries throughout — never string formatting
    in SQL statements. Prevents SQL injection.
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        self._conn = sqlite3.connect(db_path)
        self._conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self) -> None:
        """Create the employees table if it does not exist."""
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                name      TEXT    NOT NULL,
                department TEXT   NOT NULL,
                salary    REAL    NOT NULL
            )
        """)
        self._conn.commit()

    def insert(self, employee: Employee) -> int:
        """Insert an employee. Returns the new row ID."""
        cursor = self._conn.execute(
            "INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)",
            (employee.name, employee.department, employee.salary)
        )
        self._conn.commit()
        return cursor.lastrowid

    def get_all(self) -> List[Employee]:
        """Return all employees."""
        cursor = self._conn.execute(
            "SELECT id, name, department, salary FROM employees ORDER BY id"
        )
        return [
            Employee(row["name"], row["department"], row["salary"], row["id"])
            for row in cursor.fetchall()
        ]

    def get_by_department(self, department: str) -> List[Employee]:
        """Return employees in a given department. Uses parameterised query."""
        cursor = self._conn.execute(
            "SELECT id, name, department, salary FROM employees WHERE department = ?",
            (department,)
        )
        return [
            Employee(row["name"], row["department"], row["salary"], row["id"])
            for row in cursor.fetchall()
        ]

    def update_salary(self, emp_id: int, new_salary: float) -> bool:
        """Update salary for an employee. Returns True if row was found."""
        cursor = self._conn.execute(
            "UPDATE employees SET salary = ? WHERE id = ?",
            (new_salary, emp_id)
        )
        self._conn.commit()
        return cursor.rowcount > 0

    def delete(self, emp_id: int) -> bool:
        """Delete an employee. Returns True if row was found."""
        cursor = self._conn.execute(
            "DELETE FROM employees WHERE id = ?",
            (emp_id,)
        )
        self._conn.commit()
        return cursor.rowcount > 0

    def get_department_summary(self) -> List[Dict[str, Any]]:
        """Return headcount and average salary per department."""
        cursor = self._conn.execute("""
            SELECT department,
                   COUNT(*)      AS headcount,
                   AVG(salary)   AS avg_salary,
                   SUM(salary)   AS total_salary
            FROM employees
            GROUP BY department
            ORDER BY total_salary DESC
        """)
        return [dict(row) for row in cursor.fetchall()]

    def close(self) -> None:
        """Close the database connection."""
        self._conn.close()


if __name__ == "__main__":
    db = EmployeeDB(":memory:")

    employees = [
        Employee("Alice",   "Engineering", 75000),
        Employee("Bob",     "Marketing",   55000),
        Employee("Charlie", "Engineering", 85000),
        Employee("Diana",   "HR",          50000),
        Employee("Eve",     "Marketing",   62000),
        Employee("Frank",   "Engineering", 90000),
    ]

    print("=== Insert employees ===\n")
    for emp in employees:
        row_id = db.insert(emp)
        print(f"  Inserted: {emp.name} → ID {row_id}")

    print("\n=== Get all employees ===\n")
    for emp in db.get_all():
        print(f"  {emp}")

    print("\n=== Get by department ===\n")
    for emp in db.get_by_department("Engineering"):
        print(f"  {emp}")

    print("\n=== Update salary ===\n")
    updated = db.update_salary(1, 80000)
    print(f"  Updated ID 1: {updated}")
    print(f"  {db.get_all()[0]}")

    print("\n=== Delete employee ===\n")
    deleted = db.delete(4)
    print(f"  Deleted ID 4: {deleted}")
    print(f"  Remaining: {len(db.get_all())} employees")

    print("\n=== Department summary ===\n")
    for row in db.get_department_summary():
        print(f"  {row['department']:<15} "
              f"count={row['headcount']}  "
              f"avg=£{row['avg_salary']:,.0f}  "
              f"total=£{row['total_salary']:,.0f}")

    db.close()