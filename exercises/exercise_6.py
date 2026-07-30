# You have this simple tax calculator function:
def calculate_tax(income, rate):
    if not isinstance(income, (int, float)):
        raise TypeError("Income must be an integer.")
    if income < 0:
        raise ValueError("Income cannot be negative.")
    return round(income * rate, 2)

# Write a Pytest test file that:
# 1. Has a fixture that returns a list of test users with income and expected tax
# 2. Tests that calculate_tax returns the correct amount for each user
# 3. Tests that passing a negative income raises a ValueError
# 4. Tests that passing a string raises a TypeError

import pytest

@pytest.fixture
def test_users():
    return [{"user": "alice", "income": 85000,  "rate": 0.20, "expected_tax": 17000.0},
            {"user": "bob",   "income": 120000, "rate": 0.23, "expected_tax": 27600.0},
            {"user": "carol", "income": 60000,  "rate": 0.18, "expected_tax": 10800.0}]

def test_calculate_tax(test_users):
    for user in test_users:
        result = calculate_tax(user["income"], user["rate"])
        assert result == user["expected_tax"], f"Failed for user: {user['user']}"

def test_calculate_tax_with_negative_income():
    with pytest.raises(ValueError):
        calculate_tax(-50000, 0.20)

def test_calculate_tax_with_string_income():
    with pytest.raises(TypeError):
        calculate_tax("50000", 0.20)