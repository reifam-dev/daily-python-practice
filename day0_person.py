# Day 0 - Clean Person class with basic input validation

class Person:
    """Simple Person class demonstrating basic OOP."""

    def __init__(self, name: str, age: int):
        self.name = name
        if age < 0:
            raise ValueError("Age cannot be negative!")
        self.age = age

    def greet(self) -> str:
        """Return a greeting message."""
        return f"Hello! My name is {self.name} and I am {self.age} years old."


# Main execution
if __name__ == "__main__":
    try:
        name = input("Enter your name: ").strip()
        age = int(input("Enter your age: "))

        person = Person(name, age)
        print(person.greet())

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")