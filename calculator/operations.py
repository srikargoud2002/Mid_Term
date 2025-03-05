from decimal import Decimal

def add_numbers(x: Decimal, y: Decimal) -> Decimal:
    return x + y

def sub_numbers(x: Decimal, y: Decimal) -> Decimal:
    return x - y

def mul_numbers(x: Decimal, y: Decimal) -> Decimal:
    return x * y

def div_numbers(x: Decimal, y: Decimal) -> Decimal:
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y
