from abc import ABC, abstractmethod
import pytest

# ── רקע ──────────────────────────────────────────
# ABC (Abstract Base Class) = מחלקת "חוזה" — מגדירה אילו מתודות
# חובה שיהיו לכל מחלקה שיורשת ממנה, אבל לא מיישמת אותן בעצמה.
# אי אפשר ליצור מופע ישירות מ-ABC עצמה — רק ממחלקות בת שהשלימו
# את כל המתודות המסומנות @abstractmethod.

# ── PART 1 — הגדרת ה"חוזה" ─────────────────────────
class TestReporter(ABC):
    @abstractmethod
    def send(self, message: str) -> bool:
        pass

    @abstractmethod
    def format_message(self, results: dict) -> str:
        pass

# ── PART 2 — שתי מימושים שונים של אותו "חוזה" ───────
class SlackReporter(TestReporter):
    def format_message(self, results: dict) -> str:
        return f"🔔 Tests: {results['passed']}/{results['total']} passed"

    def send(self, message: str) -> bool:
        print(f"[SLACK] {message}")
        return True

class EmailReporter(TestReporter):
    def format_message(self, results: dict) -> str:
        return f"Test Report: {results['passed']} of {results['total']} tests passed."

    def send(self, message: str) -> bool:
        print(f"[EMAIL] {message}")
        return True

# ── PART 3 — הכוח האמיתי — קוד שלא צריך לדעת איזה reporter ──
def publish_results(reporter: TestReporter, results: dict) -> bool:
    return reporter.send(reporter.format_message(results)) if results else False

# ── PART 4 — מה קורה אם שוכחים ליישם מתודה? ─────────
class BrokenReporter(TestReporter):
    def send(self, message: str) -> bool:
        return True

# ── PART 5 — Pytest ──────────────────────────────────
def test_slack_reporter_format():
    reporter = SlackReporter()
    message = reporter.format_message({"passed": 8, "total": 10})
    assert message == "🔔 Tests: 8/10 passed"

def test_email_reporter_format():
    reporter = EmailReporter()
    message = reporter.format_message({"passed": 8, "total": 10})
    assert message == "Test Report: 8 of 10 tests passed."

def test_publish_results_works_with_any_reporter():
    results = {"passed": 8, "total": 10}
    assert publish_results(SlackReporter(), results) == True
    assert publish_results(EmailReporter(), results) == True

def test_cannot_instantiate_abstract_class():
    with pytest.raises(TypeError):
        TestReporter()
