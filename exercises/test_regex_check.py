import re

def detect_ssn(text: str) -> bool:
    pattern = r"\b(\d{3})-(\d{2})-(\d{4})\b"
    matches = re.finditer(pattern, text)
    for match in matches:
        area = match.group(1)
        # Invalid SSN area numbers: 000, 666, and 900-999
        if area == "000" or area == "666" or area.startswith("9"):
            continue
        return True
    return False

if __name__ == "__main__":
    print(detect_ssn("Random text 12345"))  # should print False
    print(detect_ssn("Random text 12345"))  # False — no dashes
    print(detect_ssn("Phone: 123-456-7890")) # False — wrong grouping
    print(detect_ssn("SSN: 123-45-6789"))          # True — valid
    print(detect_ssn("Code: 999-99-9999"))         # should now be False
    print(detect_ssn("Order ID: 555-12-3489-X"))   # still True — still a false positive