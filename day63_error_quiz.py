# Day 63 - Error Finding Quiz

class ValidatedRecord:

    ALLOWED_FIELDS = {"name", "age", "salary"}

    def __setattr__(self, name, value):
        if name not in self.ALLOWED_FIELDS:   # Bug 1 - infinite recursion, ALLOWED_FIELDS
            raise AttributeError(              #         accessed via __getattribute__ not __setattr__
                f"'{name}' is not an allowed field."
            )
        super().__setattr__(name, value)

    def __getattr__(self, name):
        return f"'{name}' has not been set."


class LoggedObject:

    def __init__(self):
        self.__dict__["_log"] = []

    def __setattr__(self, name, value):
        self.__dict__["_log"].append(f"SET {name} = {value}")
        self.__dict__[name] = value           # correct

    def __getattr__(self, name):
        raise AttributeError(f"'{name}' not found")

    def get_log(self):
        return _log                           # Bug 2 - missing self


class FrozenObject:

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            object.__setattr__(self, key, val)

    def __setattr__(self, name, value):
        raise AttributeError("This object is frozen and cannot be modified.")

    def __delattr__(self, name):
        raise AttributeError("Cannot delete attributes from frozen object.")


r = ValidatedRecord()
r.name = "Alice"   # Bug 1 demonstrates here - hits ALLOWED_FIELDS before it is set
r.age = 30
print(r.name)
print(r.missing_field)