import pytest

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Basic usage
def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)

# Check the actual error MESSAGE too
def test_divide_by_zero_message():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

# Capture the exception object for deeper inspection
def test_divide_by_zero_inspect():
    with pytest.raises(ValueError) as exc_info:
        divide(10, 0)
    assert "zero" in str(exc_info.value).lower()