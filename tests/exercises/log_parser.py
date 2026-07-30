# Write a function that parses these logs and returns:
# 1. List of all DENY events as dicts with keys: timestamp, protocol, src, dst
# 2. List of unique destination IPs that were denied
# 3. Which source IP triggered the most DENY events
import json

def log_parser(logs: list) -> tuple:
    # 1. List of all DENY events as dicts with keys: timestamp, protocol, src, dst
    deny_events = []

    # 2. List of unique destination IPs that were denied
    unique_dst = []

    # 3. Which source IP triggered the most DENY events
    unique_src = []

    for log in logs:
        current_log = log.split()
        if current_log[2] == "DENY":
            timestamp = current_log[0] + " " + current_log[1]
            protocol = current_log[3]
            src = current_log[4].split(":")[0]
            dst = current_log[6].split(":")[0]
            deny_events.append({"timestamp": timestamp, "protocol": protocol, "src": src, "dst": dst})
            unique_dst.append(dst)
            unique_src.append(src)
    unique_dst = list(dict.fromkeys(unique_dst))
    unique_src = max(unique_src, key=unique_src.count) if unique_src else None
    return (deny_events, unique_dst, unique_src)

if __name__ == "__main__":
    # You receive raw firewall log lines as strings:
    logs = [
        "2024-01-15 10:23:45 ALLOW TCP 192.168.1.5:52341 -> 8.8.8.8:443",
        "2024-01-15 10:23:46 DENY  TCP 192.168.1.8:44821 -> 185.220.101.5:4444",
        "2024-01-15 10:23:47 ALLOW UDP 192.168.1.5:53124 -> 1.1.1.1:53",
        "2024-01-15 10:23:48 DENY  TCP 10.0.0.5:39812 -> 185.220.101.5:4444",
    ]
    deny_events, unique_dst, unique_src = log_parser(logs)
    print("List of all DENY events:")
    print(json.dumps(deny_events, indent=2))
    print(f"List of unique destination IPs that were denied: {unique_dst}")
    print(f"The source IP triggered the most DENY events: {unique_src}")