# You receive a list of raw log entries from Tenable's scanner:
import json

logs = [
    "2026-07-20 08:14:32 INFO  Asset server-01 scan completed. Found 12 vulnerabilities.",
    "2026-07-20 08:15:01 ERROR Asset server-02 scan failed. Connection timeout.",
    "2026-07-20 08:16:45 INFO  Asset server-03 scan completed. Found 27 vulnerabilities.",
    "2026-07-20 08:17:12 WARN  Asset server-04 scan completed. Found 0 vulnerabilities.",
    "2026-07-20 08:18:55 ERROR Asset server-05 scan failed. Authentication error.",
    "2026-07-20 08:19:30 INFO  Asset server-06 scan completed. Found 5 vulnerabilities.",
]

# Write a function parse_logs(logs) that returns a dict with:
# 1. "completed"     — list of asset names where scan completed successfully
# 2. "failed"        — list of asset names where scan failed, with their error reason
#                      e.g. [{"asset": "server-02", "reason": "Connection timeout"}]
# 3. "total_vulns"   — total number of vulnerabilities found across all completed scans
# 4. "error_count"   — number of ERROR level log entries

def parse_logs(logs: list) -> dict:
    completed = []
    failed = []
    total_vulns = 0

    for log in logs:
        parts = log.split()
        asset = parts[4]

        if "completed." in log:
            completed.append(asset)
            # "Found 12 vulnerabilities." → parts[-2] is the number
            total_vulns += int(parts[-2])

        if "failed." in log:
            # Everything after "failed." is the reason
            reason = log.split("failed. ")[1].rstrip(".")
            failed.append({"asset": asset, "reason": reason})

    error_count = sum(1 for log in logs if log.split()[2] == "ERROR")

    return {
        "completed": completed,
        "failed": failed,
        "total_vulns": total_vulns,
        "error_count": error_count,
    }

parsed_logs = parse_logs(logs)
print(json.dumps(parsed_logs, indent=2))
