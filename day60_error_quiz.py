# Day 60 - Error Finding Quiz

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass
class Employee:
    name: str
    department: str
    salary: float

    def get_annual_bonus(self, rate=0.1):
        return self.salary * rate


def read_employees_csv(filepath: Path) -> List[Employee]:
    employees = []
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            emp = Employee(
                name=row["name"],
                department=row["department"],
                salary=float(row["salary"])
            )
            employees.append(emp)
    return employees


def write_employees_csv(filepath: Path, employees: List[Employee]) -> None:
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "department", "salary"])
        writer.writeheader
        for emp in employees:           # Bug 1 - writeheader missing ()
            writer.writerow({
                "name": emp.name,
                "department": emp.department,
                "salary": emp.salary
            })


def get_department_total(employees: List[Employee], dept: str) -> float:
    return sum(emp.salary for emp in employees if emp.department = dept)  # Bug 2 - = should be ==


def get_highest_earner(employees: List[Employee]) -> Employee:
    return max(employees, key=lambda e: e.salary)


emps = [
    Employee("Alice", "Engineering", 75000),
    Employee("Bob", "Marketing", 55000),
    Employee("Charlie", "Engineering", 85000),
]

print(get_department_total(emps, "Engineering"))
print(get_highest_earner(emps))
print(emps[0].get_annual_bonus)   # Bug 3 - missing ()