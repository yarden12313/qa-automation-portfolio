# You have this list of vulnerability scan results:
from email import generator

scans = [
    {"asset": "server-01", "severity": "CRITICAL", "cvss": 9.8, "patch_available": False},
    {"asset": "server-02", "severity": "HIGH",     "cvss": 7.5, "patch_available": True},
    {"asset": "server-03", "severity": "CRITICAL", "cvss": 9.1, "patch_available": False},
    {"asset": "server-04", "severity": "LOW",      "cvss": 2.1, "patch_available": True},
    {"asset": "server-05", "severity": "MEDIUM",   "cvss": 5.3, "patch_available": False},
    {"asset": "server-06", "severity": "HIGH",     "cvss": 8.2, "patch_available": True},
]

# PART 1 — Generator
# Write a generator function urgent_scans(scans) that:
# Yields scans one at a time where:
# - severity is CRITICAL or HIGH
# - AND patch is not available
# Then iterate over it and print each result

def urgent_scans(scans: list):
    for scan in scans:
        if scan["severity"] in ["CRITICAL", "HIGH"] and not scan["patch_available"]:
            yield scan

# PART 2 — Decorator
# Write a decorator called validate_scan that:
# - Checks that the dict passed to a function has
#   "asset", "severity", and "cvss" keys
# - Raises KeyError if any are missing
# - Raises ValueError if cvss is not between 0 and 10
# - Lets the function run normally if everything is valid
#

def validate_scan(func):
    def inner(*args, **kwargs):
        for arg in args:
            if not isinstance(arg, dict):
                raise TypeError(f"Expected dict, got {type(arg).__name__}")
            if not all(key in arg for key in ["asset", "severity", "cvss"]):
                raise KeyError(f"Argument must contain 'asset', 'severity' and 'cvss'")
            if not 0 <= arg["cvss"] <= 10:
                raise ValueError("cvss value must be between 0 and 10")
        result = func(*args, **kwargs)
        return result
    return inner

# Apply it to this function:
@validate_scan
def process_scan(scan: dict) -> str:
    return f"Processing {scan['asset']} — severity {scan['severity']}, cvss {scan['cvss']}"

# PART 3 — combine them
# Use your urgent_scans generator to iterate over scans
# and call process_scan on each one
# Print the result of each call

for scan in urgent_scans(scans):
    print(process_scan(scan))
