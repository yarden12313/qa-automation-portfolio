from enum import Enum
import pytest


class Severity(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

def classify_alert(cpu_usage: float) -> Severity:
    if cpu_usage >= 90:
        return Severity.CRITICAL
    elif cpu_usage >= 70:
        return Severity.HIGH
    elif cpu_usage >= 40:
        return Severity.MEDIUM
    else:
        return Severity.LOW

class Firewall:
    def __init__(self, max_rules: int, rules_count: int):
        self._max_rules = max_rules
        self._rules_count = rules_count

    @property
    def is_overloaded(self) -> bool:
        return self._rules_count > self._max_rules

    @property
    def capacity_percent(self) -> float:
        return round((self._rules_count / self._max_rules) * 100, 1) if self._max_rules > 0 else 0.0

# parametrize across at least 4 cpu_usage values, one for each Severity level
@pytest.mark.parametrize("cpu_usage, expected", [
    (100.1, Severity.CRITICAL),
    (20.2, Severity.LOW),
    (50.5, Severity.MEDIUM),
    (80.9, Severity.HIGH),
])
def test_classify_alert(cpu_usage, expected):
    assert classify_alert(cpu_usage) == expected

# a firewall with rules_count greater than max_rules -> is_overloaded is True
def test_firewall_is_overloaded_true():
    firewall = Firewall(10, 12)
    assert firewall.is_overloaded is True

# a firewall with rules_count under max_rules -> is_overloaded is False
def test_firewall_is_overloaded_false():
    firewall = Firewall(10, 8)
    assert firewall.is_overloaded is False

# assert the exact percentage for a specific rules_count/max_rules combo
def test_firewall_capacity_percent():
    firewall = Firewall(10, 8)
    assert firewall.capacity_percent == 80.0

def test_firewall_at_exact_capacity_not_overloaded():
    firewall = Firewall(10, 10)
    assert firewall.is_overloaded is False