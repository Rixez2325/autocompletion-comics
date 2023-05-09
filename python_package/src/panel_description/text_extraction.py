import boto3
import io
import json
from PIL import Image, ImageDraw
from utils import aws_utils as aws

from mypy_boto3_textract.client import TextractClient
from mypy_boto3_s3.service_resource import S3ServiceResource, Object


MINIMUM_CONFIDENCE = 50

BUCKET = "autocompletion-comics-buckets"

DEMO_FILE = "datasets/panels/one_picture.PNG"
S3_DEMO_FILE = "samples/one_picture.PNG"

DEMO_OUTPUT = "datasets/panels_text/demo.json"
S3_DEMO_OUTPUT = "samples/output.json"


# TMP
# Get the document from S3
def get_original_image_from_s3(s3_connection: S3ServiceResource) -> Image:
    s3_object = s3_connection.Object(BUCKET, S3_DEMO_FILE)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response["Body"].read())
    image = Image.open(stream)

    return image


# TMP
def get_original_image_from_local(file_name) -> Image:
    return Image.open(file_name)


# TMP
def display_bubbles(image: Image, blocks, width, height):
    for block in blocks:
        print(
            f"""
        Text: {block["Text"]}
        Confidence: {block["Confidence"]}
        Boudingbox: {block["BoundingBox"]}

        """
        )
        draw = ImageDraw.Draw(image)

        # Draw box around entire Bubble
        bbox = block["BoundingBox"]

        left = bbox["Left"] * width
        top = bbox["Top"] * height
        right = (bbox["Left"] + bbox["Width"]) * width
        bottom = (bbox["Top"] + bbox["Height"]) * height
        points = [(left, top), (right, top), (right, bottom), (left, bottom)]

        draw.polygon((points), outline="black")

    image.show()


# TODO check for exception
def get_request_document_througt_local_file(file_full_path):
    with open(file_full_path, "rb") as image_file:
        return {"Bytes": image_file.read()}


# TODO check for exception
def get_request_document_througt_s3(bucket, document):
    return {"S3Object": {"Bucket": bucket, "Name": document}}


# TODO check for exception
def textract_api_request(textract_client: TextractClient):
    request_document = get_request_document_througt_local_file(DEMO_FILE)
    response = textract_client.detect_document_text(Document=request_document)
    return response["Blocks"]


def get_lines(blocks: list[dict]) -> list[dict]:
    return [
        {
            "Text": block["Text"],
            "Confidence": block["Confidence"],
            "BoundingBox": block["Geometry"]["BoundingBox"],
        }
        for block in blocks
        if block["BlockType"] == "LINE" and block["Confidence"] >= MINIMUM_CONFIDENCE
    ]


def merge_lines(lines: list[dict], threshold=0.1):
    bubbles = []
    for line in lines:
        bbox1 = line["BoundingBox"]
        merged = False
        for bubble in bubbles:
            bbox2 = bubble["BoundingBox"]
            # Calculate distance between centers of bounding boxes
            x_dist = abs(
                bbox1["Left"] + bbox1["Width"] / 2 - bbox2["Left"] - bbox2["Width"] / 2
            )
            y_dist = abs(
                bbox1["Top"] + bbox1["Height"] / 2 - bbox2["Top"] - bbox2["Height"] / 2
            )
            dist = (x_dist**2 + y_dist**2) ** 0.5

            # Merge boxes if distance is below threshold
            if dist < threshold:
                bubble["BoundingBox"]["Width"] = max(bbox1["Width"], bbox2["Width"])
                bubble["BoundingBox"]["Height"] = bbox1["Height"] + bbox2["Height"]
                bubble["BoundingBox"]["Left"] = min(bbox1["Left"], bbox2["Left"])
                bubble["BoundingBox"]["Top"] = min(bbox1["Top"], bbox2["Top"])
                bubble["Text"] += " " + line["Text"]
                merged = True
                break

        # Add current line as new bubble if not merged with existing bubbles
        if not merged:
            bubbles.append(line)

    return bubbles


def sort_bubbles(merged_lines: list[dict]) -> list[dict]:
    return sorted(merged_lines, key=lambda line: line["BoundingBox"]["Left"])


# TODO dynamic definition of object name
def write_result_in_s3_old(merged_lines: list[dict], s3_connection):
    json_file = json.dumps(merged_lines).encode("UTF-8")
    aws.write_in_s3(json_file, s3_connection, BUCKET, S3_DEMO_OUTPUT)


def write_result_in_s3_old(merged_lines: list[dict], s3_connection):
    s3_file = s3_connection.Object(BUCKET, S3_DEMO_OUTPUT)
    s3_file.put(Body=(bytes(json.dumps(merged_lines).encode("UTF-8"))))


def write_result_localy(merged_lines: list[dict]):
    with open(DEMO_OUTPUT, "w") as outfile:
        json.dump(merged_lines, outfile)


# init s3 instances
# TODO extract to function
s3_connection = aws.get_s3_connection()
textract_client = aws.get_textract_client()


# Get the text blocks
blocks = textract_api_request(textract_client)
lines = get_lines(blocks)
bubbles = merge_lines(lines)
ordered_bubbles = sort_bubbles(bubbles)


# TMP for demo purpose
image = get_original_image_from_local(DEMO_FILE)
# image = get_original_image_from_s3(s3_connection)
width, height = image.size
display_bubbles(image, ordered_bubbles, width, height)
# write_result_in_s3(merged_lines, s3_connection)
