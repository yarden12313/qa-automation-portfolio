# Write calculate_exposure_score(vuln) that:
# - Starts with cvss as base score
# - CRITICAL severity: multiply by 2
# - HIGH severity: multiply by 1.5
# - No patch available: add 3 points
# - Patch available: subtract 1 point
# - Cap at 20 (max)
# - Round to 1 decimal place
# Then write get_prioritized_vulns(vulnerabilities)
# Returns all vulnerabilities sorted by exposure_score descending
# with exposure_score added to each dict
# Then write tests for calculate_exposure_score
# Write a complete Pytest test file for calculate_exposure_score() that:
# 1. Tests a CRITICAL vuln with no patch — should be high score
# 2. Tests a LOW vuln with patch — should be low score
# 3. Tests that score never exceeds 20 (the cap)
# 4. Tests that a missing required field raises the right exception
# Use parametrize for at least the scoring cases

import pytest

vulnerabilities = [
    {"id": "CVE-2024-001", "host": "192.168.1.1", "severity": "CRITICAL", "cvss": 9.8, "patch_available": True},
    {"id": "CVE-2024-002", "host": "192.168.1.2", "severity": "HIGH",     "cvss": 7.5, "patch_available": False},
    {"id": "CVE-2024-003", "host": "192.168.1.1", "severity": "MEDIUM",   "cvss": 5.3, "patch_available": True},
    {"id": "CVE-2024-004", "host": "192.168.1.3", "severity": "CRITICAL", "cvss": 9.1, "patch_available": False},
    {"id": "CVE-2024-005", "host": "192.168.1.2", "severity": "LOW",      "cvss": 2.1, "patch_available": True},
]

def calculate_exposure_score(vuln: dict) -> float:
    # Validate required fields
    if "severity" not in vuln:
        raise ValueError("No severity provided")
    if not isinstance(vuln["severity"], str):
        raise ValueError("Invalid severity  — must be a string")
    if "cvss" not in vuln:
        raise ValueError("No cvss provided")
    if not isinstance(vuln["cvss"], (int, float)):
        raise ValueError("Invalid cvss — must be a number")
    if "patch_available" not in vuln:
        raise ValueError("No patch_available provided")
    if not isinstance(vuln["patch_available"], bool):
        raise ValueError("Invalid patch_available - must be a bool")

    # Calculate score — use local variable, never mutate original
    score = vuln["cvss"]

    if vuln["severity"] == "CRITICAL":
        score *= 2
    elif vuln["severity"] == "HIGH":
        score *= 1.5

    if not vuln["patch_available"]:
        score += 3
    else:
        score -= 1

    score = min(score, 20.0)
    return round(score, 1)

def get_prioritized_vulns(vulnerabilities: list) -> list:
    return sorted(
        [{**vulnerability, "exposure_score": calculate_exposure_score(vulnerability)} for vulnerability in vulnerabilities],
        key=lambda vulnerability: vulnerability["exposure_score"],
        reverse=True)

# ── scoring tests ────────────────────────────────────────
@pytest.mark.parametrize("vuln, expected", [
    ({"severity": "CRITICAL", "cvss": 9.8, "patch_available": False}, 20.0),  # 9.8*2+3=22.6 → capped
    ({"severity": "CRITICAL", "cvss": 9.8, "patch_available": True},  18.6),  # 9.8*2-1=18.6
    ({"severity": "HIGH",     "cvss": 7.5, "patch_available": False}, 14.2),  # 7.5*1.5+3=14.25
    ({"severity": "LOW",      "cvss": 2.1, "patch_available": True},   1.1),  # 2.1-1=1.1
    ({"severity": "MEDIUM",   "cvss": 5.3, "patch_available": False},  8.3),  # 5.3+3=8.3
])
def test_exposure_score(vuln, expected):
    assert calculate_exposure_score(vuln) == pytest.approx(expected, rel=1e-1)

# ── cap test ─────────────────────────────────────────────
@pytest.mark.parametrize("vulnerability", vulnerabilities)
def test_score_never_exceeds_cap(vulnerability):
    assert calculate_exposure_score(vulnerability) <= 20.0

@pytest.mark.parametrize("vulnerability", [
    {"id": "CVE-2024-001", "host": "192.168.1.1", "cvss": 9.8, "patch_available": True},
    {"id": "CVE-2024-002", "host": "192.168.1.2", "severity": "HIGH",     "patch_available": False},
    {"id": "CVE-2024-003", "host": "192.168.1.1", "severity": "MEDIUM",   "cvss": 5.3, },
    {"id": "CVE-2024-004", "host": "192.168.1.3", "severity": 1, "cvss": 9.1, "patch_available": False},
    {"id": "CVE-2024-005", "host": "192.168.1.2", "severity": "LOW",      "cvss": "2.1", "patch_available": True},
    {"id": "CVE-2024-005", "host": "192.168.1.2", "severity": "LOW",      "cvss": 2.1, "patch_available": "True"}
])
def test_vuln_with_missing_required_fields_return_error(vulnerability):
    with pytest.raises(ValueError):
        calculate_exposure_score(vulnerability)
