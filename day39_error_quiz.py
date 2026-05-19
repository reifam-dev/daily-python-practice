# Day 39 - Error Finding Quiz

class FileManager:

    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file   # correct

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()
        return False

class Timer:

    def __init__(self):
        import time
        self.start = None

    def __enter__(self):
        import time
        self.start = time.time()
        # Bug 1 - missing return self

    def __exit__(self, exc_type, exc_value, traceback):
        import time
        elapsed = time.time() - self.start
        print(f"Elapsed: {elapsed:.4f}s")
        # Bug 2 - missing return False

class DatabaseConnection:

    def __init__(self, db_name):
        self.db_name = db_name
        self.connected = False

    def __enter__(self):
        self.connected = True
        print(f"Connected to {self.db_name}")
        return self   # correct

    def __exit__(self, exc_type, exc_val, exc_tb):
        connected = False   # Bug 3 - missing self
        print(f"Disconnected from {self.db_name}")
        return False

with DatabaseConnection("MyDB") as db:
    print(f"Is connected: {db.connected}")