# ============================================================
# EXERCISE 2 — Parametrize
# ============================================================
import pytest

def get_refund(tax_paid, tax_owed):
    if not isinstance(tax_paid, (int, float)) or not isinstance(tax_owed, (int, float)):
        raise TypeError("tax_paid and tax_owed must be numbers")
    if tax_paid < 0 or tax_owed < 0:
        raise ValueError("tax_paid and tax_owed must be non-negative")
    if tax_owed >= tax_paid:
        return 0
    return tax_paid - tax_owed

@pytest.mark.parametrize("tax_paid, tax_owed, expected", [
    (200,    50,    150),      # normal refund
    (50,     200,   0),        # no refund — owed more than paid
    (200,    200,   0),        # edge case — exactly equal
    (0,      0,     0),        # zero values
    (1500.5, 200.5, 1300.0),   # float inputs
])
def test_get_refund(tax_paid, tax_owed, expected):
    assert get_refund(tax_paid, tax_owed) == expected

@pytest.mark.parametrize("tax_paid, tax_owed, error", [
    (-50,   200,   ValueError),   # negative tax_paid
    (200,   -50,   ValueError),   # negative tax_owed
    ("200", 50,    TypeError),    # wrong type
])
def test_get_refund_errors(tax_paid, tax_owed, error):
    with pytest.raises(error):
        get_refund(tax_paid, tax_owed)