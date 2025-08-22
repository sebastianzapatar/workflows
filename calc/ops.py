"""
Operaciones aritméticas simples.
"""
from typing import Union

Number = Union[int, float]

def add(a: Number, b: Number) -> Number:
    """Suma dos números y devuelve el resultado."""
    return a + b
