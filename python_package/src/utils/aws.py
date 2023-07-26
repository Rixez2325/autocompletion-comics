from io import BytesIO
import json
from PIL import Image
import fitz
import boto3

from mypy_boto3_textract.client import TextractClient
from mypy_boto3_s3.service_resource import S3ServiceResource, Object


DEFAULT_REGION = "eu-west-1"
S3_BUCKET = "autocompletion-comics-buckets"


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


def list_s3_folder(folder_prefix: str, bucket_name: str = S3_BUCKET) -> list:
    s3_client = boto3.client("s3")
    folder_response = s3_client.list_objects_v2(
        Bucket=bucket_name, Prefix=folder_prefix
    )
    return folder_response["Contents"][1:]


def load_file_from_s3(folder_prefix: str, bucket_name: str = S3_BUCKET) -> list:
    s3_client = boto3.client("s3")

    bucket_content = list_s3_folder(folder_prefix)

    files_list = []

    for file in bucket_content:
        file_key = file["Key"]
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        file = response["Body"].read()
        files_list.append(file)

    return files_list


def load_pdf_from_s3(folder_prefix: str, bucket_name: str = S3_BUCKET) -> list:
    return [
        fitz.open(stream=BytesIO(pdf_data))
        for pdf_data in load_file_from_s3(folder_prefix)
    ]


def load_image_from_s3(folder_prefix: str, bucket_name: str = S3_BUCKET) -> list:
    return [
        Image.open(BytesIO(image_data)).show()
        for image_data in load_file_from_s3(folder_prefix)
    ]


def load_json_from_s3(folder_prefix: str, bucket_name: str = S3_BUCKET) -> list:
    return [json.loads(json_str) for json_str in load_file_from_s3(folder_prefix)]


def save_objects_to_s3(objects: list, folder_prefix: str, bucket_name: str = S3_BUCKET):
    s3_client = boto3.client("s3")
    responses = {}
    for object_name, object_content in objects.items():
        # Combine the folder prefix with the object name to get the S3 key (full path)
        s3_key = folder_prefix + object_name

        # Use 'put_object' to upload the object content to the S3 bucket with the specified key
        response = s3_client.put_object(
            Bucket=bucket_name, Key=s3_key, Body=object_content
        )

        # Store the response for each object upload
        responses[object_name] = response

    return responses
