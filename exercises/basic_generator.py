vulnerabilities = [
    {"id": "CVE-001", "severity": "CRITICAL", "cvss": 9.8},
    {"id": "CVE-002", "severity": "HIGH",     "cvss": 7.5},
    {"id": "CVE-003", "severity": "CRITICAL", "cvss": 9.1},
    {"id": "CVE-004", "severity": "LOW",      "cvss": 2.1},
]

# Write a generator function critical_vulns(vulns)
# that yields one critical vulnerability at a time
# Then iterate over it and print each one

def basic_generator(vulns):
    for vulnerability in vulns:
        if vulnerability["severity"] == "CRITICAL":
            yield vulnerability

for vulnerability in basic_generator(vulnerabilities):
    print(vulnerability)