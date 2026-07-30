# Write a function is_safe_port(port) that:
# Returns True if port is in the "safe" list: [80, 443, 53, 123]
# Returns False for any other port
# Raises ValueError if port is not an integer
# Raises ValueError if port is out of range (< 1 or > 65535)
# Then write a complete Pytest test file covering:
# happy path, unsafe port, invalid type, out of range
# Use parametrize for the happy path and unsafe port cases

import pytest

safe_ports = [80, 443, 53, 123]

def is_safe_port(port: int, safe_ports: list) -> bool:
    if not isinstance(port, int):
        raise ValueError("port is not an integer")

    if not (1 <= port <= 65535):
        raise ValueError("port is not in the range [1, 65535]")

    return port in safe_ports

@pytest.mark.parametrize("port", [80, 443, 53, 123])
def test_is_safe_port(port):
    assert is_safe_port(port, safe_ports) is True

@pytest.mark.parametrize("port", [444, 8080, 3000])
def test_is_unsafe_port(port):
    assert is_safe_port(port, safe_ports) is False

@pytest.mark.parametrize("port", [0, -1, 66666, "jhjh"])
def test_is_invalid_port(port):
    with pytest.raises(ValueError):
       is_safe_port(port, safe_ports)
