# Scenario: you have a base config shared across all microservices,
# and each service can override specific values.
import pytest

base_config = {
    "timeout_seconds": 30,
    "retry_attempts": 3,
    "log_level": "INFO",
    "max_connections": 100,
}

service_overrides = {
    "user-service": {"timeout_seconds": 10, "log_level": "DEBUG"},
    "payment-service": {"retry_attempts": 5, "max_connections": 50},
    "notification-service": {},  # no overrides, use base as-is
}

def get_service_config(service_name: str, base: dict, overrides: dict) -> dict:
    if service_name not in overrides:
        raise KeyError(f"Service '{service_name}' not found in overrides")
    return {**base, **overrides[service_name]}

class InvalidConfigError(Exception):
    pass

def validate_config(config: dict) -> bool:
    if config["timeout_seconds"] <= 0:
        raise InvalidConfigError(f"timeout_seconds must be positive, got {config['timeout_seconds']}")
    if config["retry_attempts"] < 0:
        raise InvalidConfigError(f"retry_attempts cannot be negative, got {config['retry_attempts']}")
    if config["max_connections"] <= 0:
        raise InvalidConfigError(f"max_connections must be positive, got {config['max_connections']}")
    if config["log_level"] not in ["DEBUG", "INFO", "WARNING", "ERROR"]:
        raise InvalidConfigError(f"log_level '{config['log_level']}' is not valid")
    return True

# user-service gets timeout_seconds=10 (overridden) but retry_attempts=3 (from base)
def test_get_service_config_applies_override():
    assert get_service_config("user-service", base_config, service_overrides) == {
    "timeout_seconds": 10,
    "retry_attempts": 3,
    "log_level": "DEBUG",
    "max_connections": 100,
}

# KeyError for a service not in overrides
def test_get_service_config_unknown_service_raises():
    with pytest.raises(KeyError):
        get_service_config("test-service", base_config, service_overrides)

# call get_service_config twice, assert base_config["timeout_seconds"] is still 30 after both calls
def test_base_config_not_mutated():
    get_service_config("user-service", base_config, service_overrides)
    get_service_config("payment-service", base_config, service_overrides)
    assert base_config["timeout_seconds"] == 30

# Parametrized test for validate_config covering all 4 invalid cases
@pytest.mark.parametrize("bad_config, key", [({
    "timeout_seconds": -1,
    "retry_attempts": 3,
    "log_level": "DEBUG",
    "max_connections": 100,
}, "timeout_seconds"), ({
    "timeout_seconds": 10,
    "retry_attempts": -3,
    "log_level": "DEBUG",
    "max_connections": 100,
}, "retry_attempts"), ({
    "timeout_seconds": 10,
    "retry_attempts": 3,
    "log_level": "TEST",
    "max_connections": 100,
}, "log_level"), ({
    "timeout_seconds": 10,
    "retry_attempts": 3,
    "log_level": "DEBUG",
    "max_connections": -100,
}, "max_connections")])
def test_validate_invalid_config(bad_config: dict, key:str):
    with pytest.raises(InvalidConfigError, match=key):
        validate_config(bad_config)