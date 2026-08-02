# QA Automation Portfolio

Automation test suite demonstrating QA engineering patterns — built with Python, Pytest, Docker, and GitHub Actions CI.

## What's inside

- **AWS testing with moto** — S3 and SQS mocking, fixtures with automatic teardown, async event polling
- **API test framework** — mocked REST API client tests including error handling (404/500) and confidence-threshold validation for AI-agent responses
- **Detection accuracy testing** — parametrized true/false-positive cases for PII detection (SSN, credit card, passport) with regex validation
- **Pytest patterns** — fixtures, parametrize, pytest.raises, MagicMock, generators and decorators

## Infrastructure

- **Docker** — containerized test runner (Python 3.11 slim, cached dependency layer)
- **CI** — GitHub Actions pipeline runs the full suite on every push and pull request, with JUnit XML reporting

## Running the tests

```bash
# Locally
pip install -r requirements.txt
pytest tests/ -v

# In Docker
docker build -t test-runner .
docker run test-runner
```

## Author

Yarden Tasa — Senior Automation QA Engineer
9 years of experience in Israeli cybersecurity companies (Checkmarx, CyberProof, GK8, Reyzon)
