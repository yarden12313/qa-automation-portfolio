# You are given a list of security events from Tenable's platform.
# Each event has a timestamp, asset, event type, and severity.
import json

events = [
    {"timestamp": "2026-07-20 08:01:00", "asset": "server-01", "type": "login_failure",    "severity": "LOW"},
    {"timestamp": "2026-07-20 08:02:00", "asset": "server-01", "type": "login_failure",    "severity": "LOW"},
    {"timestamp": "2026-07-20 08:03:00", "asset": "server-01", "type": "login_failure",    "severity": "LOW"},
    {"timestamp": "2026-07-20 08:04:00", "asset": "server-01", "type": "login_success",    "severity": "INFO"},
    {"timestamp": "2026-07-20 08:05:00", "asset": "server-02", "type": "port_scan",        "severity": "HIGH"},
    {"timestamp": "2026-07-20 08:06:00", "asset": "server-02", "type": "port_scan",        "severity": "HIGH"},
    {"timestamp": "2026-07-20 08:07:00", "asset": "server-03", "type": "login_failure",    "severity": "LOW"},
    {"timestamp": "2026-07-20 08:08:00", "asset": "server-03", "type": "login_failure",    "severity": "LOW"},
    {"timestamp": "2026-07-20 08:09:00", "asset": "server-03", "type": "file_access",      "severity": "MEDIUM"},
    {"timestamp": "2026-07-20 08:10:00", "asset": "server-01", "type": "file_access",      "severity": "MEDIUM"},
]


def has_consecutive_failures(asset_events, threshold=3):
    consecutive = 0
    for event in asset_events:
        if event["type"] == "login_failure":
            consecutive += 1
            if consecutive >= threshold:
                return True
        else:
            consecutive = 0  # reset — sequence broken
    return False

def analyze_events(events: list) -> dict:
    events_by_asset = {}
    events_by_type = {}
    for event in events:
        if event["asset"] not in events_by_asset:
            events_by_asset[event["asset"]] = []
        events_by_asset[event["asset"]].append(event)
        if event["type"] not in events_by_type:
            events_by_type[event["type"]] = []
        events_by_type[event["type"]].append(event)

    # list of asset names that have 3 or more consecutive "login_failure" events
    # (consecutive means one after another with no other event type in between for that asset)
    brute_force_suspects = [asset for asset in events_by_asset if has_consecutive_failures(events_by_asset[asset])]

    # list of unique asset names that have at least one HIGH severity event
    high_severity_assets = list(set([asset for asset in events_by_asset for event in events_by_asset[asset] if event["severity"] == "HIGH"]))

    # dict mapping each event type to how many times it appears across all events
    event_summary = {f"{event}":len(events_by_type[event]) for event in events_by_type}

    # the asset name with the most total events
    assets_by_events = {f"{event}":len(events_by_asset[event]) for event in events_by_asset}
    most_active_asset = max(assets_by_events, key=assets_by_events.get)

    return {"brute_force_suspects": brute_force_suspects,
            "high_severity_assets": high_severity_assets,
            "event_summary": event_summary,
            "most_active_asset": most_active_asset}

print(json.dumps(analyze_events(events), indent=2))


