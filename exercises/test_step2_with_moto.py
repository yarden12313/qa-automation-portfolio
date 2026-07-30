# test_step2.py
import boto3
from moto import mock_aws

@mock_aws
def test_upload_file_to_s3():
    s3 = boto3.client("s3", region_name="us-east-1")

    s3.create_bucket(Bucket="test-bucket")
    s3.put_object(Bucket="test-bucket", Key="test-pii.txt", Body=b"SSN: 123-45-6789")

    obj = s3.get_object(Bucket="test-bucket", Key="test-pii.txt")
    content = obj["Body"].read()
    assert b"SSN" in content
    print("File content verified:", content)