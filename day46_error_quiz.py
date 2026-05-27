# Day 46 - Error Finding Quiz

class DatabaseSingleton:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        return f"Connected to {self.host}:{self.port}"


class ConfigSingleton:

    _instance = None

    def __new__(cls):
        if _instance is None:           # Bug 1 - missing cls
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.settings = {}

    def set(self, key, value):
        self.settings[key] = value

    def get(self, key):
        return self.settings.get(key)


db1 = DatabaseSingleton("localhost", 5432)
db2 = DatabaseSingleton("remotehost", 9999)
print(db1 is db2)          # Should be True - same instance
print(db1.host)            # Bug 2 - __init__ runs again so host will be "remotehost"

config1 = ConfigSingleton()
config2 = ConfigSingleton  # Bug 3 - missing ()
print(config1 is config2)