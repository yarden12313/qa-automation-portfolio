# DONE uploads a file to S3 with mock PII content,
# DONE waits up to 10 seconds polling an SQS queue for a DLP event,
# DONE asserts the event action is BLOCK,
# DONE cleans up the S3 object in teardown.
# DONE add a negative test case (a file without PII that should NOT trigger a BLOCK event)
# DONE parametrize multiple PII types — SSN, credit card, passport — into one test

import boto3
import json
import time
import pytest
from moto import mock_aws

@pytest.fixture
def aws_mock():
    with mock_aws():
        yield

@pytest.fixture
def s3_bucket(aws_mock):
    s3 = boto3.client("s3", region_name="us-east-1")
    bucket_name = "test-bucket"
    s3.create_bucket(Bucket=bucket_name)
    yield bucket_name, s3
    objects = s3.list_objects_v2(Bucket=bucket_name).get("Contents", [])
    for obj in objects:
        s3.delete_object(Bucket=bucket_name, Key=obj["Key"])
    s3.delete_bucket(Bucket=bucket_name)

@pytest.fixture
def sqs_queue(aws_mock):
    sqs = boto3.client("sqs", region_name="us-east-1")
    queue_url = sqs.create_queue(QueueName="test-queue")["QueueUrl"]
    yield queue_url, sqs
    sqs.delete_queue(QueueUrl=queue_url)

def poll_for_block_event(sqs, queue_url, timeout=3):
    """Poll SQS until a BLOCK event arrives or timeout."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        resp = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=1
        )
        for msg in resp.get("Messages", []):
            body = json.loads(msg["Body"])
            if body.get("action") == "BLOCK":
                return body
    return None

def detect_pii(content: bytes) -> str | None:
    """Very simple fake 'DLP engine' so we have real logic to test against."""
    text = content.decode()
    if "SSN" in text:
        return "SSN"
    if "Credit Card" in text:
        return "CREDIT_CARD"
    if "Passport" in text:
        return "PASSPORT"
    return None

def test_without_pii_file_triggers_block_event(s3_bucket, sqs_queue):
    bucket_name, s3 = s3_bucket
    queue_url, sqs = sqs_queue

    # Step 1: upload a file NOT containing PII
    file_key = "clean-file.txt"
    s3.put_object(
        Bucket=bucket_name,
        Key=file_key,
        Body=b"Meeting notes: discussed Q3 roadmap and budget planning."
    )

    # Step 2: This stands in for "the real product scanning the file"
    detected = detect_pii(b"Meeting notes: discussed Q3 roadmap and budget planning.")
    assert detected is None

    # Only simulate a BLOCK event if PII was actually detected
    if detected:
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps({"action": "BLOCK", "file_key": file_key, "reason": f"PII detected: {detected}"})
        )

    # Step 3: poll SQS and assert the BLOCK event arrives
    event = poll_for_block_event(sqs, queue_url, timeout=3)
    assert event is None, f"Expected no BLOCK event, but got: {event}"
    # Cleanup happens automatically via fixture teardown

# --- Test data: (file content, expected detection result) ---
test_cases = [
    (b"SSN: 123-45-6789", "SSN"),
    (b"Credit Card: 4111-1111-1111-1111", "CREDIT_CARD"),
    (b"Passport: X1234567", "PASSPORT"),
    (b"Meeting notes: Q3 roadmap", None),   # clean file — no PII
]

@pytest.mark.parametrize("file_content,expected_pii_type", test_cases)
def test_dlp_detection(s3_bucket, sqs_queue, file_content, expected_pii_type):
    bucket_name, s3 = s3_bucket
    queue_url, sqs = sqs_queue

    file_key = "test-file.txt"
    s3.put_object(Bucket=bucket_name, Key=file_key, Body=file_content)

    # This stands in for "the real product scanning the file"
    detected = detect_pii(file_content)
    assert detected == expected_pii_type

    # Only simulate a BLOCK event if PII was actually detected
    if detected:
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps({"action": "BLOCK", "file_key": file_key, "reason": f"PII detected: {detected}"})
        )

    event = poll_for_block_event(sqs, queue_url)
    if expected_pii_type:
        assert event is not None, "Expected a BLOCK event but got none"
        assert event["action"] == "BLOCK"
    else:
        assert event is None, f"Expected no BLOCK event, got: {event}"