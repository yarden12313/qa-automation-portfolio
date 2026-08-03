# Build a VulnerabilityScanner class that manages scan results.

# The class should:
# 1. __init__  — initialize with a scanner_name (string) and
#                an empty list of scan results

# 2. add_scan(asset, severity, cvss) — adds a scan result to the list
#                as a dict: {"asset": asset, "severity": severity, "cvss": cvss}
#                Raises ValueError if cvss is not between 0 and 10
#                Raises ValueError if severity is not one of:
#                ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

# 3. get_critical() — returns list of all CRITICAL scan results

# 4. highest_risk() — returns the single scan result with the highest cvss score
#                     returns None if no scans have been added yet

# 5. summary() — returns a dict with:
#                "scanner":      the scanner name
#                "total_scans":  total number of scans added
#                "avg_cvss":     average cvss rounded to 1 decimal, or 0.0 if no scans
#                "critical_count": number of CRITICAL results

class VulnerabilityScanner:
    def __init__(self, scanner_name):
        self.scanner_name = scanner_name
        self.scan_results = []

    def add_scan(self, asset, severity, cvss):
        if not 0 <= cvss <= 10:
            raise ValueError("CVSS must be between 0 and 10")
        if severity not in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]:
            raise ValueError("Severity must be LOW, MEDIUM, HIGH or CRITICAL")
        self.scan_results.append({"asset": asset, "severity": severity, "cvss": cvss})

    def get_critical(self):
        return [scan for scan in self.scan_results if scan["severity"] == "CRITICAL"]

    def highest_risk(self):
        return max(self.scan_results, key=lambda scan: scan["cvss"]) if self.scan_results else None

    def summary(self):
        return {"scanner": self.scanner_name,
                "total_scans": len(self.scan_results),
                "avg_cvss": round(sum(scan["cvss"] for scan in self.scan_results) / len(self.scan_results), 1) if self.scan_results else 0.0,
                "critical_count": len(self.get_critical())}

# Example usage:
scanner = VulnerabilityScanner("Tenable-01")
scanner.add_scan("server-01", "CRITICAL", 9.8)
scanner.add_scan("server-02", "HIGH", 7.5)
scanner.add_scan("server-03", "CRITICAL", 9.1)
scanner.add_scan("server-04", "LOW", 2.1)

print(scanner.get_critical())   # server-01 and server-03
print(scanner.highest_risk())   # server-01 with cvss 9.8
print(scanner.summary())        # dict with stats