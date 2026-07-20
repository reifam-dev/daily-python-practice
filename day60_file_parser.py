# Day 60 - Clean file parser combining pathlib, dataclass and csv
# Demonstrates: composition of standard library modules
# PEP 8, docstrings, type hints, exceptions throughout

import csv
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional


@dataclass
class Employee:
    """Represents an employee record."""

    name: str
    department: str
    salary: float

    def get_annual_bonus(self, rate: float = 0.10) -> float:
        """Return the annual bonus based on salary and rate."""
        return round(self.salary * rate, 2)

    def __str__(self) -> str:
        return (f"Employee(name='{self.name}', "
                f"dept='{self.department}', "
                f"salary=£{self.salary:,.0f})")


def write_employees_csv(filepath: Path, employees: List[Employee]) -> None:
    """Write a list of employees to a CSV file."""
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["name", "department", "salary"]
        )
        writer.writeheader()
        for emp in employees:
            writer.writerow({
                "name": emp.name,
                "department": emp.department,
                "salary": emp.salary
            })


def read_employees_csv(filepath: Path) -> List[Employee]:
    """Read employees from a CSV file and return a list of Employee objects."""
    employees = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            employees.append(Employee(
                name=row["name"],
                department=row["department"],
                salary=float(row["salary"])
            ))
    return employees


def get_department_total(
    employees: List[Employee], dept: str
) -> float:
    """Return the total salary for a given department."""
    return sum(emp.salary for emp in employees if emp.department == dept)


def get_department_summary(
    employees: List[Employee]
) -> Dict[str, Dict]:
    """Return a summary of headcount and total salary per department."""
    summary: Dict[str, Dict] = {}
    for emp in employees:
        if emp.department not in summary:
            summary[emp.department] = {"count": 0, "total_salary": 0.0}
        summary[emp.department]["count"] += 1
        summary[emp.department]["total_salary"] += emp.salary
    return summary


def get_highest_earner(employees: List[Employee]) -> Optional[Employee]:
    """Return the employee with the highest salary."""
    if not employees:
        return None
    return max(employees, key=lambda e: e.salary)


if __name__ == "__main__":
    employees = [
        Employee("Alice", "Engineering", 75000),
        Employee("Bob", "Marketing", 55000),
        Employee("Charlie", "Engineering", 85000),
        Employee("Diana", "HR", 50000),
        Employee("Eve", "Marketing", 62000),
        Employee("Frank", "Engineering", 90000),
    ]

    with tempfile.TemporaryDirectory() as tmp:
        csv_path = Path(tmp) / "employees.csv"

        print("=== Write and read CSV ===\n")
        write_employees_csv(csv_path, employees)
        loaded = read_employees_csv(csv_path)
        print(f"  Written and loaded {len(loaded)} employees\n")

        print("=== Department summary ===\n")
        summary = get_department_summary(loaded)
        for dept, data in sorted(summary.items()):
            avg = data["total_salary"] / data["count"]
            print(f"  {dept:<15} count={data['count']}  "
                  f"total=£{data['total_salary']:,.0f}  "
                  f"avg=£{avg:,.0f}")

        print("\n=== Engineering total ===\n")
        eng_total = get_department_total(loaded, "Engineering")
        print(f"  Engineering payroll: £{eng_total:,.0f}")

        print("\n=== Highest earner ===\n")
        top = get_highest_earner(loaded)
        if top:
            print(f"  {top}")
            print(f"  Annual bonus (10%): £{top.get_annual_bonus():,.0f}")

        print("\n=== CSV file preview ===\n")
        print(f"  {csv_path.read_text(encoding='utf-8')}")