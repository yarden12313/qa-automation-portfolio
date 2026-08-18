import re
import pytest

class InvalidPortError(Exception):
    pass

class InvalidIpError(Exception):
    pass

def validate_config(config: dict) -> bool:
    if not re.search(r"\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", config["ip"]):
        raise InvalidIpError("Invalid IP address: " + config["ip"])
    if not re.search(r"\b([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])\b", config["port"]):
        raise InvalidPortError("Invalid Port: " + config["port"])
    return True

class NetworkDevice:
    def __init__(self, name: str, ip: str):
        self.name = name
        self.ip = ip

    def status(self) -> str:
        return f"{self.name} ({self.ip}) is online"

class Firewall(NetworkDevice):
    def __init__(self, rules_count: int, name: str, ip: str):
        super().__init__(name, ip)
        self.rules_count = rules_count

    def status(self) -> str:
        return super().status() + f" with {self.rules_count} rules"

class Router(NetworkDevice):
    def __init__(self, connected_devices:list, name: str, ip: str):
        super().__init__(name, ip)
        self.connected_devices = connected_devices

    def status(self) -> str:
        return super().status() + f" managing {len(self.connected_devices)} devices"

def test_invalid_port_raises():
    with pytest.raises(InvalidPortError):
        validate_config({"ip": "125.255.255.1", "port": "99999"})

def test_invalid_ip_raises():
    with pytest.raises(InvalidIpError):
        validate_config({"ip": "999.1.1.1", "port": "6666"})

def test_valid_config_returns_true():
    assert validate_config({"ip": "125.255.255.255", "port": "6666"}) is True

def test_firewall_status():
    firewall = Firewall(3, "test", "125.255.255.1")
    assert firewall.status() == "test (125.255.255.1) is online with 3 rules"

def test_router_status():
    router = Router([1, 2, 3], "test", "125.255.255.1")
    assert router.status() == "test (125.255.255.1) is online managing 3 devices"
