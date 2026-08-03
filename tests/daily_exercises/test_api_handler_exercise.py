import pytest
import requests
from unittest.mock import patch, MagicMock

class TenableAPIHandler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def get_users(self):
        response = self.session.get(f"{self.base_url}/users")
        response.raise_for_status()
        return response.json()

    def create_post(self, payload):
        response = self.session.post(f"{self.base_url}/posts", json=payload)
        response.raise_for_status()
        return response.json()

@pytest.fixture
def api():
    return TenableAPIHandler("https://tenable.test.com")

def test_user_has_correct_username(api):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"email": "qa@email.com", "username": "Tester"}
    ]
    mock_response.raise_for_status.return_value = None
    with patch("requests.Session.get", return_value=mock_response):
        users = api.get_users()
        user = next((u for u in users if u["email"] == "qa@email.com"), None)
        assert user is not None
        assert user["username"] == "Tester"

def test_create_post(api):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"title": "foo", "body": "lalala", "user_id": 1}
    mock_response.raise_for_status.return_value = None
    with patch("requests.Session.post", return_value=mock_response):
        result = api.create_post({"title": "foo", "body": "lalala", "user_id": 1})
        assert result["title"] == "foo"