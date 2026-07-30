# You have this API client that fetches vulnerability data:
import pytest
import requests
from unittest.mock import patch, MagicMock

class TenableClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {"X-ApiKeys": f"accessKey={api_key}"}

    def get_vulnerabilities(self, asset_id: str) -> list:
        response = requests.get(
            f"{self.base_url}/assets/{asset_id}/vulnerabilities",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_asset(self, asset_id: str) -> dict:
        response = requests.get(
            f"{self.base_url}/assets/{asset_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

fake_vulnerabilities = [
    {"asset": "server-01", "severity": "CRITICAL", "cvss": 9.8, "patch_available": False},
    {"asset": "server-02", "severity": "HIGH",     "cvss": 7.5, "patch_available": True},
]

# fixture called tenable_client that returns a TenableClient instance with fake base_url and api_key
@pytest.fixture
def tenable_client() -> TenableClient:
    return TenableClient(base_url="https://fake.tenable.com", api_key="fake-key-123")

# mock the API response, assert it returns a list of vulnerabilities correctly
def test_get_vulnerabilities_success(tenable_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "vulnerabilities": fake_vulnerabilities,
    }
    mock_response.raise_for_status.return_value = None
    with patch("requests.get", return_value=mock_response):
        result = tenable_client.get_vulnerabilities("123456")
        assert result["vulnerabilities"] == fake_vulnerabilities

# mock a 404 response, assert HTTPError is raised
def test_get_vulnerabilities_404(tenable_client):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
    with patch("requests.get", return_value=mock_response):
        with pytest.raises(requests.exceptions.HTTPError):
            tenable_client.get_vulnerabilities("noneexistuser")

# mock a valid asset response, assert the asset name and id are returned correctly
def test_get_asset_success(tenable_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "name": "asset_name",
        "id": "123456",
    }
    mock_response.raise_for_status.return_value = None
    with patch("requests.get", return_value=mock_response):
        result = tenable_client.get_asset("123456")
        assert result["name"] == "asset_name"
        assert result["id"] == "123456"

# mock a 500 response, assert HTTPError is raised
def test_get_asset_500(tenable_client):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")
    with patch("requests.get", return_value=mock_response):
        with pytest.raises(requests.exceptions.HTTPError):
            tenable_client.get_asset("noneexistuser")