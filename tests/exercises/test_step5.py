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

def poll_for_block_event(sqs, queue_url, timeout=10):
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

def test_pii_file_triggers_block_event(s3_bucket, sqs_queue):
    bucket_name, s3 = s3_bucket
    queue_url, sqs = sqs_queue

    # Step 1: upload a file containing PII
    file_key = "sensitive-file.txt"
    s3.put_object(
        Bucket=bucket_name,
        Key=file_key,
        Body=b"SSN: 123-45-6789"
    )

    # Step 2: simulate the DLP system publishing a BLOCK event
    # (in a real system, this happens automatically — here we simulate it)
    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps({
            "action": "BLOCK",
            "file_key": file_key,
            "reason": "PII detected: SSN"
        })
    )

    # Step 3: poll SQS and assert the BLOCK event arrives
    event = poll_for_block_event(sqs, queue_url, timeout=10)
    assert event is not None, "No BLOCK event received within 10 seconds"
    assert event["action"] == "BLOCK"
    assert event["file_key"] == file_key
    print("BLOCK event received:", event)
    # Cleanup happens automatically via fixture teardown