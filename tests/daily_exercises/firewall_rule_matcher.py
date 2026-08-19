def evaluate_packet(rules:list, dst_port:int, protocol:str)->str:
    for rule in rules:
        port_matches = dst_port == rule["dst_port"]
        protocol_matches = protocol == rule["protocol"] or rule["protocol"] == "ANY"
        if port_matches and protocol_matches:
            return rule["action"]
    return "DENY"

rules = [
    {"action": "ALLOW", "src": "10.0.0.0/8", "dst_port": 443, "protocol": "TCP"},
    {"action": "DENY",  "src": "10.0.0.0/8", "dst_port": 22,  "protocol": "TCP"},
    {"action": "ALLOW", "src": "0.0.0.0/0",  "dst_port": 53,  "protocol": "UDP"},
    {"action": "DENY",  "src": "0.0.0.0/0",  "dst_port": 0,   "protocol": "ANY"},
]

if __name__ == "__main__":
    print(evaluate_packet(rules, 22, protocol="TCP"))