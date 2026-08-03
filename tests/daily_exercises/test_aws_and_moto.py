# You have this AWS asset discovery service:
import boto3
import pytest
from moto import mock_aws

class AWSAssetScanner:
    def __init__(self, region: str = "us-east-1"):
        self.ec2 = boto3.client("ec2", region_name=region)
        self.s3  = boto3.client("s3",  region_name=region)

    def get_running_instances(self) -> list:
        """Returns list of running EC2 instance IDs"""
        response = self.ec2.describe_instances(
            Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
        )
        instances = []
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                instances.append({
                    "id":    instance["InstanceId"],
                    "type":  instance["InstanceType"],
                    "state": instance["State"]["Name"]
                })
        return instances

    def get_public_buckets(self) -> list:
        """Returns list of S3 bucket names that have public access"""
        response = self.s3.list_buckets()
        return [b["Name"] for b in response["Buckets"]]

# an aws_mock fixture using moto's mock_aws that starts the fake AWS environment for each test
@pytest.fixture
def aws_mock():
    with mock_aws():
        yield

# a scanner fixture that returns an AWSAssetScanner instance
@pytest.fixture
def scanner(aws_mock):
    return AWSAssetScanner()

# no instances created, assert the function returns an empty list
def test_get_running_instances_empty(scanner):
    assert scanner.get_running_instances() == []

# no buckets created, assert returns empty list
def test_get_public_buckets_empty(scanner):
    assert scanner.get_public_buckets() == []

# create 2 fake S3 buckets using boto3, assert get_public_buckets() returns both bucket names
def test_get_public_buckets_returns_buckets(aws_mock, scanner):
    scanner.s3.create_bucket(Bucket="test-bucket-1")
    scanner.s3.create_bucket(Bucket="test-bucket-2")
    result = scanner.get_public_buckets()
    assert set(result) == {"test-bucket-1", "test-bucket-2"}
    assert len(result) == 2

# create 2 fake EC2 instances using boto3, assert get_running_instances() returns both
def test_get_running_instances(aws_mock, scanner):
    instances = scanner.ec2.run_instances(ImageId='ami-12345',
        InstanceType='t2.micro',
        MinCount=2,
        MaxCount=2)
    running_instances = scanner.get_running_instances()
    assert instances["Instances"][0]["InstanceId"] == running_instances[0]["id"]
    assert instances["Instances"][1]["InstanceId"] == running_instances[1]["id"]
    assert instances["Instances"][0]["InstanceType"] == running_instances[0]["type"]
    assert instances["Instances"][1]["InstanceType"] == running_instances[1]["type"]