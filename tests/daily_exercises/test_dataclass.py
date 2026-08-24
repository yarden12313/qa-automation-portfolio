import dataclasses
from dataclasses import dataclass
from collections import defaultdict, Counter

@dataclass
class TestResult:
    test_name: str
    status: str          # "PASS", "FAIL", "SKIP"
    duration_ms: int
    suite: str

def group_by_suite(test_results: list[TestResult]) -> dict:
    grouped = defaultdict(list)
    for result in test_results:
        grouped[result.suite].append(result)
    return dict(grouped)

def suite_summary(test_results: list) -> dict:
    summary = {}
    for suite, results in group_by_suite(test_results).items():
        summary[suite] = {
            "total": len(results),
            "passed": sum(1 for r in results if r.status == "PASS"),
            "failed": sum(1 for r in results if r.status == "FAIL"),
            "avg_duration_ms": round(sum(r.duration_ms for r in results) / len(results)) if results else 0,
        }
    return summary

def test_group_by_suite ():
    results = [
        TestResult("test_login", "PASS", 120, "auth"),
        TestResult("test_logout", "PASS", 90, "auth"),
        TestResult("test_charge", "FAIL", 340, "payment"),
        TestResult("test_refund", "PASS", 200, "payment"),
        TestResult("test_signup", "FAIL", 150, "auth"),
    ]
    assert group_by_suite(results) == {
        'auth': [TestResult(test_name='test_login', status='PASS', duration_ms=120, suite='auth'),
                  TestResult(test_name='test_logout', status='PASS', duration_ms=90, suite='auth'),
                  TestResult(test_name='test_signup', status='FAIL', duration_ms=150, suite='auth')],
         'payment': [TestResult(test_name='test_charge', status='FAIL', duration_ms=340, suite='payment'),
                     TestResult(test_name='test_refund', status='PASS', duration_ms=200, suite='payment')]}

def test_suite_summary():
    results = [
        TestResult("test_login", "PASS", 120, "auth"),
        TestResult("test_logout", "PASS", 90, "auth"),
        TestResult("test_charge", "FAIL", 340, "payment"),
        TestResult("test_refund", "PASS", 200, "payment"),
        TestResult("test_signup", "FAIL", 150, "auth"),
    ]
    assert suite_summary(results) ==  {'auth': {'total': 3, 'passed': 2, 'failed': 1, 'avg_duration_ms': 120},
                                    'payment': {'total': 2, 'passed': 1, 'failed': 1, 'avg_duration_ms': 270}}

def test_dataclass_equality():
    assert TestResult("test_login", "PASS", 120, "auth") == TestResult("test_login", "PASS", 120, "auth")

