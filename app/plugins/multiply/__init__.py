from app.commands import Command
from calculator import CalcEngine 
from decimal import Decimal, InvalidOperation

class MultiplyCommand(Command):
    def execute(self, a_str: str, b_str: str) -> None:
        try:
            val_a = Decimal(a_str)
            val_b = Decimal(b_str)
        except InvalidOperation:
            print(f"Invalid number input: {a_str} or {b_str} is not a valid number.")
            return
        
        # Calculate the product
        result = CalcEngine.product(val_a, val_b)        
        if result == 0:
            result = 0
        
        print(f"The result of {a_str} * {b_str} is {result}")
