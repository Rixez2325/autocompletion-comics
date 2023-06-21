import os
import io
import json
from PIL import Image, ImageDraw
from utils import aws_utils as aws

from mypy_boto3_textract.client import TextractClient
from mypy_boto3_s3.service_resource import S3ServiceResource

from images_preparation.utils import PANELS_DIR


MINIMUM_CONFIDENCE = 50
THRESHOLD = 0.1

PANELS_TEXT_DIR = "datasets/panels_text"

S3_BUCKET = "autocompletion-comics-buckets"

S3_DEMO_FILE = "samples/one_picture.PNG"
S3_DEMO_OUTPUT = "samples/output.json"


# TMP
def demo():
    _, textract_client = init_aws_instance()
    for panel in os.listdir(PANELS_DIR):
        panel_full_path = f"{PANELS_DIR}/{panel}"
        request_document = get_request_document_througt_local_file(panel_full_path)
        blocks = textract_api_request(textract_client, request_document)

        words = get_words(blocks)
        lines = get_lines(blocks)
        bubbles = merge_lines(lines)
        ordered_bubbles = sort_bubbles(bubbles)

        with open(f"{PANELS_TEXT_DIR}/{panel}_text.json", "w") as outfile:
            json.dump(ordered_bubbles, outfile)

        demo_show_result(ordered_bubbles, words, panel_full_path)


# TMP
# Get the document from S3
def get_original_image_from_s3(s3_connection: S3ServiceResource) -> Image:
    s3_object = s3_connection.Object(S3_BUCKET, S3_DEMO_FILE)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response["Body"].read())
    image = Image.open(stream)

    return image


# TMP
def get_original_image_from_local(file_name: str) -> Image:
    return Image.open(file_name)


# TMP
def demo_show_result(bubbles: list[dict], words: list[dict], file: str):
    image = get_original_image_from_local(file)
    # image = get_original_image_from_s3(s3_connection)
    width, height = image.size
    image = display_bubbles(image, words, width, height, "green")
    image = display_bubbles(image, bubbles, width, height, "red")
    image.show()
    # write_result_in_s3(merged_lines, s3_connection)


# TMP
def display_bubbles(
    image: Image, blocks: list[dict], width: int, height: int, color: str
):
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

        draw.polygon((points), outline=color)

    return image


def init_aws_instance() -> tuple[S3ServiceResource, TextractClient]:
    s3_connection = aws.get_s3_connection()
    textract_client = aws.get_textract_client()

    return s3_connection, textract_client


# TODO check for exception
def get_request_document_througt_local_file(
    file_full_path: str,
) -> dict[str, bytes]:
    with open(file_full_path, "rb") as image_file:
        return {"Bytes": image_file.read()}


# TODO check for exception
def get_request_document_througt_s3(bucket: str, document: str) -> dict[str, str]:
    return {"S3Object": {"Bucket": bucket, "Name": document}}


# TODO check for exception
def textract_api_request(textract_client: TextractClient, document: dict) -> list[dict]:
    response = textract_client.detect_document_text(Document=document)
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


def get_words(blocks: list[dict]) -> list[dict]:
    return [
        {
            "Text": block["Text"],
            "Confidence": block["Confidence"],
            "BoundingBox": block["Geometry"]["BoundingBox"],
        }
        for block in blocks
        if block["BlockType"] == "WORD" and block["Confidence"] >= MINIMUM_CONFIDENCE
    ]


def horizontaly_close(bbox1: dict, bbox2: dict) -> bool:
    return (
        abs(
            (bbox1["Left"] + (bbox1["Width"] / 2))
            - (bbox2["Left"] + (bbox2["Width"] / 2))
        )
        < THRESHOLD
    )


def verticaly_close(bbox1: dict, bbox2: dict) -> bool:
    y_dist = abs(
        bbox1["Top"] + bbox1["Height"] / 2 - bbox2["Top"] - bbox2["Height"] / 2
    )

    return y_dist - (bbox1["Height"] / 2 + bbox2["Height"] / 2) < THRESHOLD


def merge_lines(lines: list[dict], threshold=THRESHOLD) -> list[dict]:
    bubbles = []
    for line in lines:
        bbox1 = line["BoundingBox"]
        merged = False
        for bubble in bubbles:
            bbox2 = bubble["BoundingBox"]

            # Merge boxes if distance is below threshold
            if verticaly_close(bbox1, bbox2) and horizontaly_close(bbox1, bbox2):
                bubble["BoundingBox"]["Width"] = max(bbox1["Width"], bbox2["Width"])
                bubble["BoundingBox"]["Height"] = (
                    bbox1["Top"] + bbox1["Height"] - bbox2["Top"]
                )
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
def write_result_in_s3(merged_lines: list[dict], s3_connection: S3ServiceResource):
    json_file = json.dumps(merged_lines).encode("UTF-8")
    aws.write_in_s3(json_file, s3_connection, S3_BUCKET, S3_DEMO_OUTPUT)


def write_result_in_s3_old(bubbles: list[dict], s3_connection: S3ServiceResource):
    s3_file = s3_connection.Object(S3_BUCKET, S3_DEMO_OUTPUT)
    s3_file.put(Body=(bytes(json.dumps(bubbles).encode("UTF-8"))))


def write_result_localy(bubbles: list[dict], output_path: str):
    with open(output_path, "w") as outfile:
        json.dump(bubbles, outfile)


def extract_panels_text_from_local(
    input_directory: str = PANELS_DIR, output_directory: str = PANELS_TEXT_DIR
):
    panels = os.listdir(input_directory)
    _, textract_client = init_aws_instance()
    for panel in panels:
        panel_path = f"{input_directory}/{panel}"
        bubbles = extract_bubles_local(textract_client, panel_path)
        result_path = f"{output_directory}/{panel}_text.json"
        write_result_localy(bubbles, result_path)


def extract_bubles_local(textract_client: TextractClient, panel_path: str):
    request_document = get_request_document_througt_local_file(panel_path)
    blocks = textract_api_request(textract_client, request_document)
    lines = get_lines(blocks)
    bubbles = merge_lines(lines)
    ordered_bubbles = sort_bubbles(bubbles)
    return ordered_bubbles
