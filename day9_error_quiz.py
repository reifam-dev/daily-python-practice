# Day 9 - Error Finding Quiz

class PasswordValidator:
    def __init__(self, password)
        self.password = password

    def is_valid(self):
        if len(password) < 8:   # Bug
            return False
        if not any(c.isupper() for c in self.password):
            return False
        if not any(c.isdigit() for c in self.password):
            return False
        return True

validator = PasswordValidator("Password1")
print(validator.is_valid())