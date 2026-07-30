# April's platform calls an external IRS API to fetch tax transcripts.
# You have this function:
import pytest
import requests
from unittest.mock import patch, MagicMock

def get_tax_transcript(user_id: str) -> dict:
    response = requests.get(f"https://api.irs.gov/transcripts/{user_id}")
    response.raise_for_status()
    return response.json()

# Write tests that:
# 1. Mock the API response — don't call the real IRS API
# 2. Test the happy path: API returns valid transcript data
# 3. Test API failure: API returns 404 — assert the right exception is raised
# 4. Test API failure: API returns 500 — assert the right exception is raised
#
# Hint: use pytest-mock or unittest.mock.patch

def test_get_transcript_happy_path():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "user_id": "user123",
        "year": 2024,
        "income": 85000,
        "tax_paid": 17000
    }
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response):
        result = get_tax_transcript("user123")
        assert result["user_id"] == "user123"
        assert result["income"] == 85000
        assert result["tax_paid"] == 17000

def test_get_transcript_404():
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")

    with patch("requests.get", return_value=mock_response):
        with pytest.raises(requests.exceptions.HTTPError):
            get_tax_transcript("nonexistent_user")

def test_get_transcript_500():
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")

    with patch("requests.get", return_value=mock_response):
        with pytest.raises(requests.exceptions.HTTPError):
            get_tax_transcript("user123")