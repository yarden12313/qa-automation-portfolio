# Write a function that returns:
# 1. All hosts that have port 22 open (SSH — potential risk)
# 2. The host with the most open ports
# 3. A dict mapping each host to its number of open ports

import json

def get_open_ports_hosts(hosts: list) -> tuple:
    # 1. All hosts with port 22 open
    ssh_hosts = [host for host in hosts if 22 in host["open_ports"]]

    # 2. Host with most open ports
    most_exposed = max(hosts, key=lambda x: len(x["open_ports"]))

    # 3. Dict mapping host IP → number of open ports
    ports_by_host =  {host["host"]: len(host["open_ports"]) for host in hosts}
    return ssh_hosts, most_exposed, ports_by_host

if __name__ == "__main__":
    # You receive this list of network scan results:
    scans = [
        {"host": "192.168.1.1", "open_ports": [80, 443, 22], "os": "Linux"},
        {"host": "192.168.1.2", "open_ports": [3389, 445], "os": "Windows"},
        {"host": "192.168.1.3", "open_ports": [22, 8080, 8443], "os": "Linux"},
        {"host": "192.168.1.4", "open_ports": [], "os": "Unknown"},
    ]

    ssh_hosts, most_exposed, ports_by_host = get_open_ports_hosts(scans)

    print("SSH hosts:")
    print(json.dumps(ssh_hosts, indent=4))
    print(f"\nMost exposed host: {most_exposed['host']} ({len(most_exposed['open_ports'])} ports)")
    print(f"\nPorts by host: {ports_by_host}")
