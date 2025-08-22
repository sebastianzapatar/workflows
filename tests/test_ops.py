import pytest
from calc.ops import add

@pytest.mark.parametrize(
    "a,b,expected",
    [
        (1, 2, 3),
        (-5, 5, 0),
        (2.5, 0.5, 3.0),
        (0, 0, 0),
        (10, -3, 7),
    ],
)
def test_add(a, b, expected):
    assert add(a, b) == expected
