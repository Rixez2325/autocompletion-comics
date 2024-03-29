import os
import io
import json
from PIL import Image, ImageDraw
from typing import Dict, List
from mypy_boto3_textract.client import TextractClient
from mypy_boto3_s3.service_resource import S3ServiceResource

from helpers.aws_helper import (
    get_s3_connection,
    get_textract_client,
    load_images_from_s3,
    save_json_to_s3,
    write_in_s3,
    S3_BUCKET,
)
from helpers.path_helper import PANELS_DIR, PANELS_TEXT_DIR, load_images_from_local


MINIMUM_CONFIDENCE = 50
THRESHOLD = 0.1


S3_DEMO_FILE = "samples/one_picture.PNG"
S3_DEMO_OUTPUT = "samples/output.json"


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


# DEMO
def get_original_image_from_local(file_name) -> Image:
    return Image.open(file_name)


# DEMO
def demo_show_result(bubbles: List[Dict], words: List[Dict], file):
    image = get_original_image_from_local(file)
    # image = get_original_image_from_s3(s3_connection)
    width, height = image.size
    image = display_bubbles(image, words, width, height, "green")
    image = display_bubbles(image, bubbles, width, height, "red")
    image.show()
    # write_result_in_s3(merged_lines, s3_connection)


# DEMO
def display_bubbles(image: Image, blocks: List[Dict], width: int, height: int, color):
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


def extract_panels_text(
    aws: bool = False,
    input_directory=PANELS_DIR,
    output_directory=PANELS_TEXT_DIR,
):
    if aws:
        panels = load_images_from_s3(input_directory)
    else:
        panels = load_images_from_local(input_directory)

    _, textract_client = init_aws_instance()

    for i, panel in enumerate(panels):
        bubbles = extract_bubles(textract_client, panel)
        if aws:
            save_json_to_s3(bubbles, output_directory)
        else:
            result_path = f"{output_directory}/{panel}_{i}_text.json"
            write_result_localy(bubbles, result_path)


def init_aws_instance() -> tuple[S3ServiceResource, TextractClient]:
    s3_connection = get_s3_connection()
    textract_client = get_textract_client()

    return s3_connection, textract_client


def get_request_document_througt_local_file(
    file_full_path,
) -> Dict[str, bytes]:
    with open(file_full_path, "rb") as image_file:
        return {"Bytes": image_file.read()}


def pillow_image_to_bytes(image) -> Dict[str, bytes]:
    byte_stream = io.BytesIO()
    image.save(byte_stream, format="PNG")
    bytes_data = byte_stream.getvalue()
    return {"Bytes": bytes_data}


def get_request_document_througt_s3(bucket, document) -> Dict[str, str]:
    return {"S3Object": {"Bucket": bucket, "Name": document}}


def textract_api_request(textract_client: TextractClient, document: Dict) -> List[Dict]:
    response = textract_client.detect_document_text(Document=document)
    return response["Blocks"]


def get_lines(blocks: List[Dict]) -> List[Dict]:
    return [
        {
            "Text": block["Text"],
            "Confidence": block["Confidence"],
            "BoundingBox": block["Geometry"]["BoundingBox"],
        }
        for block in blocks
        if block["BlockType"] == "LINE" and block["Confidence"] >= MINIMUM_CONFIDENCE
    ]


def get_words(blocks: List[Dict]) -> List[Dict]:
    return [
        {
            "Text": block["Text"],
            "Confidence": block["Confidence"],
            "BoundingBox": block["Geometry"]["BoundingBox"],
        }
        for block in blocks
        if block["BlockType"] == "WORD" and block["Confidence"] >= MINIMUM_CONFIDENCE
    ]


def horizontaly_close(bbox1: Dict, bbox2: Dict) -> bool:
    return (
        abs(
            (bbox1["Left"] + (bbox1["Width"] / 2))
            - (bbox2["Left"] + (bbox2["Width"] / 2))
        )
        < THRESHOLD
    )


def verticaly_close(bbox1: Dict, bbox2: Dict) -> bool:
    y_dist = abs(
        bbox1["Top"] + bbox1["Height"] / 2 - bbox2["Top"] - bbox2["Height"] / 2
    )

    return y_dist - (bbox1["Height"] / 2 + bbox2["Height"] / 2) < THRESHOLD


def merge_lines(lines: List[Dict], threshold=THRESHOLD) -> List[Dict]:
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


def sort_bubbles(merged_lines: List[Dict]) -> List[Dict]:
    return sorted(merged_lines, key=lambda line: line["BoundingBox"]["Left"])


# TODO dynamic definition of object name
def write_result_in_s3(merged_lines: List[Dict], s3_connection: S3ServiceResource):
    json_file = json.dumps(merged_lines).encode("UTF-8")
    write_in_s3(json_file, s3_connection, S3_BUCKET, S3_DEMO_OUTPUT)


def write_result_in_s3_old(bubbles: List[Dict], s3_connection: S3ServiceResource):
    s3_file = s3_connection.Object(S3_BUCKET, S3_DEMO_OUTPUT)
    s3_file.put(Body=(bytes(json.dumps(bubbles).encode("UTF-8"))))


def write_result_localy(bubbles: List[Dict], output_path):
    with open(output_path, "w") as outfile:
        json.dump(bubbles, outfile)


def extract_bubles(textract_client: TextractClient, panel):
    request_document = pillow_image_to_bytes(panel)
    blocks = textract_api_request(textract_client, request_document)
    lines = get_lines(blocks)
    bubbles = merge_lines(lines)
    ordered_bubbles = sort_bubbles(bubbles)
    return ordered_bubbles
