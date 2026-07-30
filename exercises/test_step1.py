import boto3
from moto import mock_aws

@mock_aws
def test_can_use_fake_aws():
    s3 = boto3.client("s3", region_name="us-east-1")
    response = s3.list_buckets()
    assert "Buckets" in response
    print("Fake AWS working! Buckets:", response["Buckets"])