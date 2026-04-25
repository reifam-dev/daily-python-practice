# Day 15 - Error Finding Quiz

class StudentRegister:

    def __init__(self)
        self.students = []

    def add_student(self, name):
        self.students.append(name)

    def remove_student(self, name):
        self.students.remove(name)   # Bug - no check if student exists

    def is_enrolled(self, name):
        return name in students   # Bug

    def get_all_students(self):
        return self.students

register = StudentRegister()
register.add_student("Alice")
register.add_student("Bob")
print(register.is_enrolled("Alice"))
print(register.get_all_students())