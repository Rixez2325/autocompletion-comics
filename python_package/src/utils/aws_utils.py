import boto3

from mypy_boto3_textract.client import TextractClient
from mypy_boto3_s3.service_resource import S3ServiceResource, Object


DEFAULT_REGION = "eu-west-1"


def get_s3_connection() -> S3ServiceResource:
    return boto3.resource("s3")


def get_textract_client(region: str = DEFAULT_REGION) -> TextractClient:
    return boto3.client("textract", region_name=region)


def write_in_s3(
    binary_file: bytes,
    s3_connection: S3ServiceResource,
    bucket_name: str,
    object_name: str,
):
    s3_file: Object = s3_connection.Object(bucket_name, object_name)
    s3_file.put(Body=binary_file)
