# ── רקע — שלושת סוגי המתודות ─────────────────────
#
# מתודה רגילה — מקבלת self, ניגשת/משנה state של המופע הספציפי
# @staticmethod — לא מקבלת self או cls, פשוט פונקציה "שגרה" בתוך המחלקה
#                 (שייכת לוגית למחלקה, אבל לא צריכה שום דבר ממנה)
# @classmethod — מקבלת cls (המחלקה עצמה, לא מופע), משמש בעיקר
#                ל-alternative constructors — דרכים נוספות ליצור אובייקט
#
# ── PART 1 — @staticmethod ──────────────────────────────
class TestResult:
    def __init__(self, name: str, duration_ms: int, status: str):
        self.name = name
        self.duration_ms = duration_ms
        self.status = status

    @staticmethod
    def is_slow(duration_ms: int, threshold: int = 1000) -> bool:
        return duration_ms > threshold

# ── PART 2 — @classmethod כ-alternative constructor ─────
    @classmethod
    def from_log_line(cls, line: str):
        name, duration_ms, status = line.split('|')
        return cls(name, int(duration_ms), status)

# ── PART 3 — למה זה שימושי — שילוב ──────────────────────
def parse_log_file(lines: list) -> list:
    return [TestResult.from_log_line(line) for line in lines] if lines else []

# ── PART 4 — Pytest ──────────────────────────────────────
# 1.
def test_is_slow_static():
    assert TestResult.is_slow(1500) == True

# 2.
def test_from_log_line():
    test_result = TestResult.from_log_line("test_login|450|PASS")
    assert test_result.name == "test_login"
    assert test_result.duration_ms == 450
    assert test_result.status == "PASS"

# 3.
def test_parse_log_file():
    lines = [
        "test_login|450|PASS",
        "test_payment|900|FAIL",
        "test_logout|200|PASS",
    ]
    results = parse_log_file(lines)

    assert len(results) == 3
    assert results[0].name == "test_login"
    assert results[1].name == "test_payment"
    assert results[2].name == "test_logout"