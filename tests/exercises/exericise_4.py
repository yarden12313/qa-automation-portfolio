# Write a function calculate_refund(tax_paid, tax_owed) that:
# - Returns the refund amount (tax_paid - tax_owed)
# - Raises a ValueError if either input is negative
# - Raises a TypeError if either input is not a number
# - Returns 0 if tax_owed >= tax_paid (no refund owed)

def get_refund(tax_paid, tax_owed):
    if not isinstance(tax_paid, (int, float)) or not isinstance(tax_owed, (int, float)):
        raise TypeError("tax_paid and tax_owed must be numbers")
    if tax_paid < 0 or tax_owed < 0:
        raise ValueError("tax_paid or tax_owed is negative")
    if tax_owed >= tax_paid:
        return 0
    return tax_paid - tax_owed

if __name__ == '__main__':
    test_cases = [
        (200, 50),  # normal refund → 150
        (-50, 200),  # negative → ValueError
        ("50", "200"),  # wrong type → TypeError
        (50, 200),  # no refund → 0
        (1500.50, 200),  # float → should work now
    ]
    for tax_paid, tax_owed in test_cases:
        try:
            refund = get_refund(tax_paid, tax_owed)
            print(f"get_refund({tax_paid}, {tax_owed}) → {refund}")
        except (TypeError, ValueError) as e:
            print(f"get_refund({tax_paid}, {tax_owed}) → {type(e).__name__}: {e}")
