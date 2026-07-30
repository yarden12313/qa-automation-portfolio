import boto3
import json
import pytest
from moto import mock_aws

@pytest.fixture
def aws_mock():
    """Start the fake AWS environment for the test, then it auto-stops after."""
    with mock_aws():
        yield

@pytest.fixture
def s3_bucket(aws_mock):
    s3 = boto3.client("s3", region_name="us-east-1")
    bucket_name = "test-bucket"
    s3.create_bucket(Bucket=bucket_name)
    yield bucket_name, s3
    # Teardown — clean up objects then delete bucket
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

def test_upload_file(s3_bucket):
    bucket_name, s3 = s3_bucket
    s3.put_object(Bucket=bucket_name, Key="pii.txt", Body=b"SSN: 123-45-6789")
    obj = s3.get_object(Bucket=bucket_name, Key="pii.txt")
    assert b"SSN" in obj["Body"].read()

def test_queue_receives_event(sqs_queue):
    queue_url, sqs = sqs_queue
    sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps({"action": "BLOCK"}))
    resp = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)
    msg = json.loads(resp["Messages"][0]["Body"])
    assert msg["action"] == "BLOCK"