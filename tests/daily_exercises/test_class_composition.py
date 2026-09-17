from dataclasses import dataclass, field


@dataclass
class TestStep:
    name: str
    status: str

@dataclass
class TestCase:
    name: str
    steps: list

    def overall_status(self) -> str:
        return "FAIL" if any(step.status == "FAIL" for step in self.steps) else "PASS"

    def failed_steps(self) -> list:
        return [step.name for step in self.steps if step.status == "FAIL"]

@dataclass
class TestSuite:
    name: str
    test_cases: list

def suite_pass_rate(suite: TestSuite) -> float:
    if not suite.test_cases:
        return 0.0
    passed = sum(1 for tc in suite.test_cases if tc.overall_status() == "PASS")
    return round(passed / len(suite.test_cases) * 100, 1)

def test_overall_status_fails_if_any_step_fails():
    test_case = TestCase("test_payment", [TestStep("enter_card", "PASS"), TestStep("submit", "FAIL")])
    assert test_case.overall_status() == "FAIL"

def test_failed_steps_returns_correct_names():
    test_case = TestCase("test_payment", [TestStep("enter_card", "PASS"), TestStep("submit", "FAIL")])
    assert test_case.failed_steps() == ["submit"]

def test_suite_pass_rate():
    suite = TestSuite("checkout_flow", [
        TestCase("test_login", [TestStep("enter_email", "PASS"), TestStep("enter_password", "PASS")]),
        TestCase("test_payment", [TestStep("enter_card", "PASS"), TestStep("submit", "FAIL")]),
        TestCase("test_logout", [TestStep("click_logout", "PASS")]),
        TestCase("test_search", [TestStep("type_query", "PASS")]),
    ])
    assert suite_pass_rate(suite) == 75.0
