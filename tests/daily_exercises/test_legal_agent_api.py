import requests
import pytest
from unittest.mock import patch, MagicMock

class LegalAgentClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def analyze_contract(self, contract_text: str) -> dict:
        response = requests.post(
            f"{self.base_url}/analyze",
            json={"contract_text": contract_text}
        )
        response.raise_for_status()
        return response.json()

@pytest.fixture
def client()  -> LegalAgentClient:
    return LegalAgentClient("http://localhost:5000")

def is_reliable(confidence: float) -> bool:
    return confidence >= 0.7

def test_extracts_payment_obligation(client: LegalAgentClient):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"obligations":
                                           [{"type": "payment", "due_date": "2026-08-01", "amount": 5000}],
                                       "confidence": 0.95}
    mock_response.raise_for_status.return_value = None
    with patch("requests.post", return_value=mock_response):
        response = client.analyze_contract("Payment obligation")
        assert response["obligations"][0]["type"] == "payment", "Obligation type not supported"
        assert response["obligations"][0]["amount"] == 5000, "Obligation amount not supported"

def test_clean_contract_returns_no_obligations(client: LegalAgentClient):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"obligations": []}
    mock_response.raise_for_status.return_value = None
    with patch("requests.post", return_value=mock_response):
        response = client.analyze_contract("No obligation")
        assert response["obligations"] == [], "Clean contract return obligations"

@pytest.mark.parametrize("confidence,reliability,error_msg",
    [(0.95, True, "result is NOT reliable"),
     (0.7, True, "result is NOT reliable"),
     (0.3, False, "Result is reliable")])
def test_low_confidence_flagged(client: LegalAgentClient, confidence: float, reliability: bool, error_msg: str):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"obligations":
                                           [{"type": "payment", "due_date": "2026-08-01", "amount": 5000}],
                                       "confidence": confidence}
    mock_response.raise_for_status.return_value = None
    with patch("requests.post", return_value=mock_response):
        response = client.analyze_contract("Payment obligation")
        assert is_reliable(response["confidence"]) is reliability, error_msg

def test_api_error_500(client: LegalAgentClient):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server error")
    with patch("requests.post", return_value=mock_response):
        with pytest.raises(requests.exceptions.HTTPError):
            client.analyze_contract("Obligations error")