from collections import Counter
import json

def parse_log_line(log: str) -> dict:
    parts = log.split()
    level = parts[2]
    service = parts[3].split("=", 1)[1]

    # מוצא את האינדקס של duration_ms= בלי להניח כמה מילים יש ל-msg
    duration_idx = next(i for i, p in enumerate(parts) if p.startswith("duration_ms="))
    duration_ms = int(parts[duration_idx].split("=", 1)[1])

    # כל מה שבין service ל-duration הוא ה-msg, באורך משתנה
    msg = " ".join(parts[4:duration_idx]).removeprefix("msg=")

    return {"level": level, "service": service, "msg": msg, "duration_ms": duration_ms}

def iter_errors(logs: list):
    for log in logs:
        parsed = parse_log_line(log)
        if parsed["level"] == "ERROR":
            yield parsed

def analyze_logs(logs: list) -> dict:
    errors_by_service = Counter()
    slow_requests = []
    error_counter = Counter()

    for log in logs:
        parsed = parse_log_line(log)
        if parsed["level"] == "ERROR":
            errors_by_service[parsed["service"]] += 1
            error_counter[(parsed["service"], parsed["msg"])] += 1
        if parsed["duration_ms"] > 1000:
            slow_requests.append({
                "service": parsed["service"],
                "duration_ms": parsed["duration_ms"],
                "level": parsed["level"],
            })

    repeated_errors = [item for item, count in error_counter.items() if count > 1]

    return {
        "errors_by_service": dict(errors_by_service),
        "slow_requests": slow_requests,
        "repeated_errors": repeated_errors,
    }

if __name__ == "__main__":
    logs = [
        "2026-08-10 09:12:01 INFO  service=auth-api  msg=request handled  duration_ms=45",
        "2026-08-10 09:12:03 ERROR service=auth-api  msg=connection timeout  duration_ms=5000",
        "2026-08-10 09:12:05 INFO  service=data-pipeline  msg=batch processed  duration_ms=1200",
        "2026-08-10 09:12:08 ERROR service=auth-api  msg=connection timeout  duration_ms=5000",
        "2026-08-10 09:12:10 WARN  service=data-pipeline  msg=retry triggered  duration_ms=300",
        "2026-08-10 09:12:12 ERROR service=data-pipeline  msg=disk full  duration_ms=10",
        "2026-08-10 09:12:15 INFO  service=auth-api  msg=request handled  duration_ms=52",
    ]
    print(json.dumps(analyze_logs(logs), indent=2))
    print(list(iter_errors(logs)))