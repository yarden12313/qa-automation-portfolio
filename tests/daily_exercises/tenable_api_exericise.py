import requests
import pytest

BASE_URL = "https://tenable.test.com"

class TenableAPIHandler:
    def __init__(self, base_url: str):
        self.session = requests.Session()
        self.base_url = base_url

    def get_users(self) -> list:
        response = self.session.get(f"{self.base_url}/users")
        response.raise_for_status()
        return response.json()

    def create_post(self, payload: dict) -> dict:
        response = self.session.post(f"{self.base_url}/posts", json=payload)
        response.raise_for_status()
        return response.json()

@pytest.fixture
def api():
    return TenableAPIHandler(BASE_URL)

def test_user_has_correct_username(api):
    users = api.get_users()
    user = next((u for u in users if u["email"] == "qa@email.com"), None)
    assert user is not None, "User with email qa@email.com not found"
    assert user["username"] == "Tester"

def test_create_post(api):
    payload = {"title": "foo", "body": "lalala", "user_id": 1}
    result = api.create_post(payload)
    assert result["title"] == "foo"
    assert result["body"] == "lalala"
    assert result["user_id"] == 1