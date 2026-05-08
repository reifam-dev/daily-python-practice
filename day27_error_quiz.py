# Day 27 - Error Finding Quiz

class EmployeeRecords:

    def __init__(self):
        self.employees = {}

    def add_employee(self, emp_id, name, salary):
        if emp_id in self.employees:
            print("Employee already exists.")
        employees[emp_id] = {"name": name, "salary": salary}  # Bug 1 - missing self, missing else

    def remove_employee(self, emp_id):
        del self.employees[emp_id]    # Bug 2 - no check

    def give_pay_rise(self, emp_id, percentage):
        if emp_id in self.employees:
            self.employees[emp_id]["salary"] *= 1 + percentage  # Bug 3 - should be percentage / 100

    def get_details(self, emp_id):
        return self.employees.get(emp_id)

records = EmployeeRecords()
records.add_employee(1, "Alice", 30000)
records.give_pay_rise(1, 10)
print(records.get_details(1))