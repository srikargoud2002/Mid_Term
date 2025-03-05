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
