from dataclasses import dataclass
import pytest


class LowConfidenceExtractionError(Exception):
    pass

@dataclass
class ExtractedField:
    field_name: str
    extracted_value: str
    confidence: float

# ── PART 1 — Generator שמעבד אצווה גדולה ─────────────────
# כתבי generator function process_batch(lines: list, min_confidence: float = 0.85)
# שעובר על כל שורת OCR (כמו "ssn|123-45-6789|0.97"), ועבור כל שורה:
# - מפרק אותה ל-ExtractedField (אותו פירוק מ-from_ocr_line)
# - אם confidence >= min_confidence: yield ("valid", field)
# - אם confidence < min_confidence: yield ("flagged", field)
#
# שימי לב: זה generator, אז אם יש מיליון שורות (אצווה אמיתית
# של Tax Autopilot), הוא לא בונה הכל בזיכרון בבת אחת —
# מעבד שורה-שורה ומחזיר תוצאה אחת בכל פעם
def process_batch(lines: list, min_confidence: float = 0.85):
    for line in lines:
        field_name, extracted_value, confidence = line.split("|")
        field = ExtractedField(field_name, extracted_value, float(confidence))
        if field.confidence >= min_confidence:
            yield "valid", field
        else:
            yield "flagged", field

# ── PART 2 — ניצול ה-generator לסיכום ────────────────────
# כתבי summarize_batch(lines: list, min_confidence: float = 0.85) -> dict
# שמשתמשת ב-process_batch (לא כותבת את הלוגיקה שוב!),
# ומחזירה: {"valid_count": X, "flagged_count": Y, "flagged_fields": [...]}
# flagged_fields היא רשימת שמות השדות שסומנו (field_name בלבד)
def summarize_batch(lines: list, min_confidence: float = 0.85) -> dict:
    valid_count = 0
    flagged_count = 0
    flagged_fields = []
    for status, field in process_batch(lines, min_confidence):
        if status == "valid":
            valid_count += 1
        elif status == "flagged":
            flagged_count += 1
            flagged_fields.append(field.field_name)
    return {"valid_count": valid_count, "flagged_count": flagged_count, "flagged_fields": flagged_fields}

# ── PART 3 — context manager לדיווח התקדמות ──────────────
# כתבי class BatchProgress שמשמשת כ-context manager:
# - __enter__: מדפיסה "Starting batch..." ומחזירה self
# - __exit__: מדפיסה "Batch complete" (תמיד, גם אם הייתה שגיאה)
# - יש לה attribute self.processed שמתחיל מ-0
#
# שימוש:
# with BatchProgress() as progress:
#     for status, field in process_batch(lines):
#         progress.processed += 1
class BatchProgress:
    def __init__(self):
        self.processed = 0

    def __enter__(self):
        print("Starting batch...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Batch complete")

# ── PART 4 — Pytest ──────────────────────────────────────
# 1. test_process_batch_yields_correct_status — 3 שורות,
#    2 עם confidence גבוה ו-1 נמוך, בודקת שה-status נכון לכל אחת
@pytest.mark.parametrize("line,expected_status", [
    ("name|Don|0.95", "valid"),
    ("address|Varburg|0.90", "valid"),
    ("ssn|123-45-6789|0.75", "flagged"),
])
def test_process_batch_yields_correct_status(line, expected_status):
    status, field = next(process_batch([line]))
    assert status == expected_status

# 2. test_summarize_batch — אותם נתונים, בודקת את ה-dict המסכם
def test_summarize_batch():
    summary = summarize_batch(["name|Don|0.95", "address|Varburg|0.90", "ssn|123-45-6789|0.75"], 0.85)
    assert summary["valid_count"] == 2
    assert summary["flagged_count"] == 1
    assert summary["flagged_fields"] == ["ssn"]

# 3. test_batch_progress_tracks_count — עם BatchProgress,
#    מעבדת 5 שורות, בודקת ש-progress.processed == 5 בסוף
def test_batch_progress_tracks_count():
    lines = [
        "name|Don|0.95",
        "address|Varburg|0.90",
        "ssn|123-45-6789|0.75",
        "dob|1990-01-01|0.88",
        "income|50000|0.60",
    ]

    with BatchProgress() as progress:
        for status, field in process_batch(lines):
            progress.processed += 1

    assert progress.processed == 5
