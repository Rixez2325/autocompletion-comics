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
    file_list = [obj["Key"] for obj in folder_response["Contents"][1:]]
    print(file_list)
    return file_list


def load_file_from_s3_old(folder_prefix: str, bucket_name: str = S3_BUCKET) -> list:
    s3_client = boto3.client("s3")

    bucket_content = list_s3_folder(folder_prefix)

    files_list = []

    for file_key in bucket_content:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        file = response["Body"].read()
        files_list.append(file)

    return files_list


def load_obj_from_s3(file_key, bucket_name: str = S3_BUCKET):
    s3_client = boto3.client("s3")

    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    file = response["Body"].read()

    return file


def load_pdf_from_s3(folder_prefix: str) -> list:
    return [
        fitz.open(stream=BytesIO(load_obj_from_s3(pdf_data)))
        for pdf_data in list_s3_folder(folder_prefix)
    ]


def load_images_from_s3(folder_prefix: str) -> list:
    return [
        Image.open(BytesIO(load_obj_from_s3(image_data)))
        for image_data in list_s3_folder(folder_prefix)
    ]


def load_json_from_s3(folder_prefix: str) -> list:
    return [
        json.loads(load_obj_from_s3(json_str))
        for json_str in list_s3_folder(folder_prefix)
    ]


def save_pdf_to_s3(objects: list, folder_prefix: str, bucket_name: str = S3_BUCKET):
    s3_client = boto3.client("s3")
    responses = {}

    for i, object in enumerate(objects):
        s3_key = f"{folder_prefix}/result_{i}.pdf"
        response = s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=object)
        responses[s3_key] = response

    return responses


def save_images_to_s3(
    pillow_images: list, folder_prefix: str, bucket_name: str = S3_BUCKET
):
    s3_client = boto3.client("s3")
    for index, pillow_image in enumerate(pillow_images):
        with BytesIO() as buffer:
            pillow_image.save(buffer, format="PNG")
            image_data = buffer.getvalue()

        image_key = f"{folder_prefix}/image_{index}.png"

        s3_client.put_object(Bucket=bucket_name, Key=image_key, Body=image_data)


def save_json_to_s3(json_objects, folder_prefix: str, bucket_name: str = S3_BUCKET):
    s3_client = boto3.client("s3")

    for index, json_data in enumerate(json_objects):
        json_key = f"{folder_prefix}/data_{index}.json"
        json_content = json.dumps(json_data)
        s3_client.put_object(Bucket=bucket_name, Key=json_key, Body=json_content)
