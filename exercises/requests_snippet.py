import pytest
import requests

# GET request
response = requests.get("https://api.example.com/users/123")
response.raise_for_status()        # raises exception if 4xx or 5xx
data = response.json()             # parse JSON body
status = response.status_code      # 200, 404, 500 etc.

# GET with query params
response = requests.get(
    "https://api.example.com/users",
    params={"year": 2024, "status": "active"}
)
# builds: https://api.example.com/users?year=2024&status=active

# POST with JSON body
response = requests.post(
    "https://api.example.com/tax/calculate",
    json={"income": 85000, "rate": 0.20},
    headers={"Authorization": "Bearer my-token"}
)
data = response.json()

# Session (reuse headers across requests — useful in tests)
session = requests.Session()
session.headers.update({"Authorization": "Bearer my-token"})
response = session.get("https://api.example.com/users/123")

response = requests.get("https://api.example.com/data")

# --- Status code ---
print(response.status_code)        # 200, 404, 500 etc.

# --- Raise exception automatically if 4xx or 5xx ---
response.raise_for_status()        # raises requests.exceptions.HTTPError

# --- Read the body ---
data = response.json()             # parse JSON → dict
text = response.text               # raw string body
raw  = response.content            # raw bytes

# --- Headers ---
content_type = response.headers["Content-Type"]

# --- Full error handling pattern ---
try:
    response = requests.get("https://api.example.com/data", timeout=5)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e.response.status_code}")
except requests.exceptions.ConnectionError:
    print("Could not connect")


#--------------------------------------------------------------------------------------
# Without Session — repeat headers every time (bad)
requests.get("https://api.example.com/users",    headers={"Authorization": "Bearer TOKEN"})
requests.get("https://api.example.com/accounts", headers={"Authorization": "Bearer TOKEN"})
requests.get("https://api.example.com/tax",      headers={"Authorization": "Bearer TOKEN"})

# With Session — set once, reuse everywhere (good)
session = requests.Session()
session.headers.update({
    "Authorization": "Bearer TOKEN",
    "Content-Type": "application/json"
})

session.get("https://api.example.com/users")     # headers sent automatically
session.get("https://api.example.com/accounts")  # same
session.post("https://api.example.com/tax",
             json={"income": 85000})              # same

# In Pytest — Session as a fixture (the real pattern)
@pytest.fixture(scope="session")
def api_session():
    session = requests.Session()
    # Login once and get token
    response = session.post("https://api.example.com/auth",
                            json={"user": "test", "password": "secret"})
    token = response.json()["access_token"]
    session.headers.update({"Authorization": f"Bearer {token}"})
    yield session
    session.close()

def test_get_user(api_session):
    r = api_session.get("https://api.example.com/users/123")
    assert r.status_code == 200