import time
import random
from unittest.mock import patch, MagicMock
import pytest

class FlakyAPIError(Exception):
    pass

def retry(max_attempts=3, delay=0.1):
    """Decorator for retrying API calls."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except FlakyAPIError as e:
                    last_error = e
                    time.sleep(delay)
            raise last_error
        return wrapper
    return decorator

@retry(max_attempts=5, delay=0.05)
def extract_with_retry(doc_id: str) -> dict:
    return call_ai_extraction(doc_id)

def call_ai_extraction(doc_id: str) -> dict:
    """Simulates a flaky API — fails ~40% of the time."""
    if random.random() < 0.4:
        raise FlakyAPIError(f"Transient failure for {doc_id}")
    return {"doc_id": doc_id, "obligations": 3, "confidence": 0.91}

class Timer:
    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        self.elapsed = self.end_time - self.start_time
        return False

def test_retry_succeeds_after_failures():
    success_result = {"doc_id": "DOC-999", "obligations": 3, "confidence": 0.91}
    with patch("test_retry_and_timer.call_ai_extraction", side_effect=[
            FlakyAPIError("fail 1"),
            FlakyAPIError("fail 2"),
            success_result,
        ]):
        with patch("time.sleep"):  # skip the real delays during the test
            result = extract_with_retry("DOC-999")
    assert result == success_result

def test_retry_exhausts_and_raises():
    with patch("test_retry_and_timer.call_ai_extraction", side_effect=[FlakyAPIError(f"Transient failure for DOC-999") for _ in range(5)]):
        with patch("time.sleep"):
            with pytest.raises(FlakyAPIError) as exc_info:
                extract_with_retry("DOC-999")
            assert "Transient failure" in str(exc_info.value)

def test_timer_records_elapsed():
    with Timer() as t:
        time.sleep(0.5)
    assert t.elapsed > 0
