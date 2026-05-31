# Day 51 - Error Finding Quiz

class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:      # Bug 1 - should be SingletonMeta._instances
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ValidatedMeta(type):

    def __new__(mcs, name, bases, namespace):
        for key, value in namespace.items():
            if callable(value) and not key.startswith('_'):
                if not value.__doc__:
                    raise TypeError(
                        f"Method '{key}' in class '{name}' is missing a docstring."
                    )
        return super().__new__(mcs, name, bases, namespace)


class Database(metaclass=SingletonMeta):

    def __init__(self, host):
        self.host = host

    def connect(self):
        return f"Connected to {self.host}"


class Config(metaclass=ValidatedMeta):

    def get_setting(self, key):    # Bug 2 - missing docstring
        return key

    def set_setting(self, key, value):
        """Set a configuration value."""
        pass


DynamicClass = type("DynamicClass", (object,), {
    "greet": lambda self: f"Hello from {self.__class__.__name__}",
    "value": 42
})

db1 = Database("localhost")
db2 = Database("remotehost")
print(db1 is db2)          # Should be True
print(db1.host)            # Bug 3 - will be "remotehost" without __init__ guard