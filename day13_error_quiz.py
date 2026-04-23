class GradeCalculator:

    def __init__(self, grades)
        self.grades = grades

    def get_average(self):
        return sum(grades) / len(self.grades)   # Bug

    def is_passing(self):
        return self.get_average() >= 50

    def get_highest(self):
        return max(self.grades)

calc = GradeCalculator([45, 72, 88, 60, 55])
print(calc.get_average())
print(calc.is_passing())