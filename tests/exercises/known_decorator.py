import pytest
from moto import mock_aws
from unittest.mock import patch

@pytest.fixture
def my_fixture():
    return {"user": "test"}

@pytest.mark.parametrize("x,y", [(1,2),(3,4)])
def test_something(x, y):
    assert x < y

@mock_aws
def test_s3():
    import boto3
    s3 = boto3.client("s3")

# For each one — what does the decorator actually DO?