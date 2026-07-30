# conftest.py
import pytest
import boto3
import os
import requests

ENV = os.getenv("TEST_ENV", "staging")
BASE_URLS = {
    "staging": "https://staging-api.example.com",
    "prod":    "https://api.example.com",
}

@pytest.fixture(scope="session")
def base_url():
    return BASE_URLS[ENV]

@pytest.fixture(scope="session")
def aws_session():
    return boto3.Session(region_name="us-east-1")

@pytest.fixture(scope="session")
def s3(aws_session):
    return aws_session.client("s3")

@pytest.fixture(scope="session")
def auth_token(base_url):
    r = requests.post(f"{base_url}/auth/token", json={
        "client_id":     os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
    })
    r.raise_for_status()
    return r.json()["access_token"]

@pytest.fixture(scope="session")
def api(base_url, auth_token):
    s = requests.Session()
    s.headers["Authorization"] = f"Bearer {auth_token}"
    s.base_url = base_url
    return s