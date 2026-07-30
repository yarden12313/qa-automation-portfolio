# You receive a list of scan results from Tenable:
import json

scans = [
    {"asset": "server-01", "os": "Linux",   "vulnerabilities": 12, "last_seen": "2026-07-15"},
    {"asset": "server-02", "os": "Windows", "vulnerabilities": 3,  "last_seen": "2026-07-10"},
    {"asset": "server-03", "os": "Linux",   "vulnerabilities": 27, "last_seen": "2026-07-18"},
    {"asset": "server-04", "os": "Windows", "vulnerabilities": 0,  "last_seen": "2026-07-01"},
    {"asset": "server-05", "os": "Linux",   "vulnerabilities": 8,  "last_seen": "2026-07-17"},
]

# Write a function analyze_scans(scans) that returns a dict with:
# 1. "most_vulnerable" — the asset name with the most vulnerabilities
# 2. "clean_assets"   — list of asset names with 0 vulnerabilities
# 3. "by_os"          — dict mapping OS → total vulnerabilities across all assets of that OS
# 4. "avg_vulnerabilities"      — average number of vulnerabilities across all assets, rounded to 1 decimal

def analyze_scans(scans: list) -> dict:
    # Get the asset name with the most vulnerabilities
    most_vulnerable = max(scans, key=lambda scan: scan["vulnerabilities"])

    # Get list of asset names with 0 vulnerabilities
    clean_assets = [scan["asset"] for scan in scans if scan["vulnerabilities"] == 0]

    # Get dict mapping OS → total vulnerabilities across all assets of that OS
    by_os = {}
    for scan in scans:
        by_os[scan["os"]] = by_os.get(scan["os"], 0) + scan["vulnerabilities"]

    # Get average number of vulnerabilities across all assets, rounded to 1 decimal
    avg_vulnerabilities = round(sum(scan["vulnerabilities"] for scan in scans)/len(scans), 1) if scans else 0.0

    return {"most_vulnerable": most_vulnerable["asset"],
              "clean_assets": clean_assets,
              "by_os": by_os,
              "avg_vulnerabilities": avg_vulnerabilities}

result = analyze_scans(scans)
print(json.dumps(result))