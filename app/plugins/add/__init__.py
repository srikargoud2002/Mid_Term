from app.commands import Command
from decimal import Decimal, InvalidOperation
from calculator import CalcEngine 

class AddCommand(Command):
    def execute(self, a_str: str, b_str: str) -> None:
        try:
            val_a = Decimal(a_str)
            val_b = Decimal(b_str)
        except InvalidOperation:
            print(f"Invalid number input: {a_str} or {b_str} is not a valid number.")
            return
        
        result = CalcEngine.sum_values(val_a, val_b)
        print(f"The result of {a_str} + {b_str} is {result}")