from unittest.mock import patch, MagicMock

import pytest
import requests

def get_user(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    response.raise_for_status()
    return response.json()

# Without patch: this would hit the real API
# With patch: requests.get is replaced by our fake
def test_get_user_success():
    # 1. Create a fake response object
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": "123", "name": "Alice"}
    mock_response.raise_for_status.return_value = None  # do nothing

    # 2. Patch requests.get to return our fake response
    with patch("requests.get", return_value=mock_response):
        result = get_user("123")  # never hits real API

    # 3. Assert on the result
    assert result["name"] == "Alice"

# Simulating a failure
def test_get_user_404():
    mock_response = MagicMock()
    # side_effect means "raise this exception when called"
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404")

    with patch("requests.get", return_value=mock_response):
        with pytest.raises(requests.exceptions.HTTPError):
            get_user("nonexistent")