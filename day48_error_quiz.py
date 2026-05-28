# Day 48 - Error Finding Quiz

class RealDatabase:

    def __init__(self, name):
        print(f"Connecting to {name}...")
        self.name = name

    def query(self, sql):
        return f"Result from {self.name}: {sql}"


class DatabaseProxy:

    def __init__(self, name):
        self.name = name
        self._real = None

    def query(self, sql):
        if self._real is None:
            self._real = RealDatabase(self.name)
        return self._real.query(sql)


class ProtectedDatabase:

    def __init__(self, name, allowed_users):
        self.name = name
        self.allowed_users = allowed_users
        self._real = RealDatabase(name)   # Bug 1 - should be lazy, not eager

    def query(self, user, sql):
        if user not in allowed_users:     # Bug 2 - missing self
            raise PermissionError(f"{user} is not allowed.")
        return self._real.query(sql)


class LoggingProxy:

    def __init__(self, name):
        self.name = name
        self._real = RealDatabase(name)
        self.log = []

    def query(self, sql):
        result = self._real.query(sql)
        self.log.append(sql)
        return result                     # Bug 3 - log should record result too

proxy = DatabaseProxy("ProductionDB")
print(proxy.query("SELECT * FROM users"))
print(proxy.query("SELECT * FROM orders"))