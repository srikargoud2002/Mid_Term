from decimal import Decimal
from typing import Callable
from calculator.operations import add_numbers, sub_numbers, mul_numbers, div_numbers
from calculator.calculation import OperationRecord
from calculator.history.history import OperationHistory


class CalcEngine:
    @staticmethod
    def _execute_operation(x: Decimal, y: Decimal, op_func: Callable[[Decimal, Decimal], Decimal]) -> Decimal:
        record = OperationRecord.create(x, y, op_func)
        OperationHistory.add_record(record)
        return record.execute()

    @staticmethod
    def sum_values(x: Decimal, y: Decimal) -> Decimal:
        return CalcEngine._execute_operation(x, y, add_numbers)

    @staticmethod
    def difference(x: Decimal, y: Decimal) -> Decimal:
        return CalcEngine._execute_operation(x, y, sub_numbers)

    @staticmethod
    def product(x: Decimal, y: Decimal) -> Decimal:
        return CalcEngine._execute_operation(x, y, mul_numbers)

    @staticmethod
    def quotient(x: Decimal, y: Decimal) -> Decimal:
        return CalcEngine._execute_operation(x, y, div_numbers)
