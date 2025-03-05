from decimal import Decimal
from typing import Callable

class OperationRecord:
    def __init__(self, x: Decimal, y: Decimal, operation: Callable[[Decimal, Decimal], Decimal]):
        self.x = x
        self.y = y
        self.operation = operation

    def execute(self) -> Decimal:
        return self.operation(self.x, self.y)

    @staticmethod
    def create(x: Decimal, y: Decimal, operation: Callable[[Decimal, Decimal], Decimal]) -> 'OperationRecord':
        return OperationRecord(x, y, operation)

    def __repr__(self) -> str:
        return f"OperationRecord({self.x}, {self.y}, {self.operation.__name__})"
    
    @property
    def symbol(self) -> str:
        """Get operation symbol from function mapping"""
        operation_map = {
            'add_numbers': '+',
            'sub_numbers': '-',
            'mul_numbers': '×',
            'div_numbers': '÷'
        }
        return operation_map.get(self.operation.__name__, '?')
