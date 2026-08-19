def ip_in_range(ip: str, cidr: str) -> bool:
    network_ip, prefix = cidr.split("/")
    prefix = int(prefix)
    parts_to_compare = prefix // 8
    return ip.split(".")[:parts_to_compare] == network_ip.split(".")[:parts_to_compare]

if __name__ == "__main__":
    print(ip_in_range("10.5.20.3", "10.0.0.0/8"))
    print(ip_in_range("11.5.20.3", "10.0.0.0/8"))
    print(ip_in_range("192.168.1.50", "192.168.1.0/24"))
    print(ip_in_range("192.168.2.50", "192.168.1.0/24"))