# Day 27 - Clean EmployeeRecords class (PEP 8, docstrings, type hints, exceptions)

from typing import Dict, Optional


class EmployeeRecords:
    """Manages employee records with name, salary and pay rise functionality."""

    def __init__(self) -> None:
        self._employees: Dict[int, Dict] = {}

    def add_employee(self, emp_id: int, name: str, salary: float) -> None:
        """Add a new employee. Raises ValueError if ID already exists or inputs invalid."""
        if not name or not name.strip():
            raise ValueError("Employee name cannot be empty.")
        if salary <= 0:
            raise ValueError("Salary must be positive.")
        if emp_id in self._employees:
            raise ValueError(f"Employee ID {emp_id} already exists.")
        self._employees[emp_id] = {
            "name": name.strip(),
            "salary": salary
        }

    def remove_employee(self, emp_id: int) -> None:
        """Remove an employee. Raises KeyError if ID not found."""
        if emp_id not in self._employees:
            raise KeyError(f"Employee ID {emp_id} not found.")
        del self._employees[emp_id]

    def give_pay_rise(self, emp_id: int, percentage: float) -> None:
        """Apply a percentage pay rise. Raises KeyError if ID not found, ValueError if percentage invalid."""
        if emp_id not in self._employees:
            raise KeyError(f"Employee ID {emp_id} not found.")
        if percentage <= 0:
            raise ValueError("Pay rise percentage must be positive.")
        self._employees[emp_id]["salary"] *= 1 + (percentage / 100)

    def get_details(self, emp_id: int) -> Optional[Dict]:
        """Return a copy of employee details, or None if not found."""
        employee = self._employees.get(emp_id)
        return employee.copy() if employee else None

    def get_employee_count(self) -> int:
        """Return the total number of employees."""
        return len(self._employees)


if __name__ == "__main__":
    try:
        records = EmployeeRecords()
        records.add_employee(1, "Alice", 30000)
        records.add_employee(2, "Bob", 45000)
        records.add_employee(3, "Charlie", 52000)

        print(f"Total employees  : {records.get_employee_count()}")
        print(f"Alice details    : {records.get_details(1)}")

        records.give_pay_rise(1, 10)
        print(f"Alice after 10%  : {records.get_details(1)}")

        records.remove_employee(2)
        print(f"After removing Bob: {records.get_employee_count()} employees")

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")