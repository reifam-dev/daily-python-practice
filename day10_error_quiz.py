# Day 10 - Error Finding Quiz

class EmailValidator:
    def __init__(self, email)
        self.email = email

    def is_valid(self):
        if "@" not in email:   # Bug
            return False
        if "." not in self.email:
            return False
        return True

validator = EmailValidator("test@example.com")
print(validator.is_valid())