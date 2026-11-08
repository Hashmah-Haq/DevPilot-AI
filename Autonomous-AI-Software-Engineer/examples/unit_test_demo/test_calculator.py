
from calculator import add, multiply

def test_add():
    assert add(5, 3) == 8

def test_multiply():
    assert multiply(4, 2) == 8

def test_negative_numbers():
    assert add(-5, 2) == -3
