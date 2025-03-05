from app.commands import Command
from calculator import CalcEngine 
from decimal import Decimal, InvalidOperation

class DivideCommand(Command):
    def execute(self, a_str: str, b_str: str) -> None:
        try:
            val_a = Decimal(a_str)
            val_b = Decimal(b_str)
        except InvalidOperation:
            print(f"Invalid number input: {a_str} or {b_str} is not a valid number.")
            return
        
        try:
            result = CalcEngine.quotient(val_a, val_b)
            print(f"The result of {a_str} / {b_str} is {result}")
        except ZeroDivisionError:
            print("An error occurred: Cannot divide by zero")
        except ValueError:
            print("An error occurred: Cannot divide by zero")