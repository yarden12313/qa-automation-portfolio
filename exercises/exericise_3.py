# Write a function that checks if a string is a valid US SSN format
# Valid format: XXX-XX-XXXX where X is a digit
# Return True or False
import re


# Test it against:
# "123-45-6789"  → True
# "123-456-789"  → False
# "abc-de-fghi"  → False
# "123-45-67890" → False

def check_ssn(text):
    pattern = r"^\d{3}-\d{2}-\d{4}$"
    return bool(re.match(pattern, text))

if __name__ == '__main__':
    print(check_ssn("123-45-6789"))  # True
    print(check_ssn("123-456-789"))  # False
    print(check_ssn("abc-de-fghi"))  # False
    print(check_ssn("123-45-67890"))  # False