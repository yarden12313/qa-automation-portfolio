# test_step3.py
import boto3
import json
from moto import mock_aws

@mock_aws
def test_sqs_send_and_receive():
    sqs = boto3.client("sqs", region_name="us-east-1")

    queue_url = sqs.create_queue(QueueName="test-queue")["QueueUrl"]

    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps({"action": "BLOCK", "file": "test-pii.txt"})
    )

    response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)
    messages = response.get("Messages", [])
    assert len(messages) == 1

    body = json.loads(messages[0]["Body"])
    assert body["action"] == "BLOCK"
    print("Received:", body)