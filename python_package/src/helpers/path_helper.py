import os
from io import BytesIO
import json
from PIL import Image
import fitz

# relatives paths
DATASETS_DIR = "datasets"

COMICS_PAGES_DIR = f"{DATASETS_DIR}/pages"
GENERATED_PAGE_DIR = f"{DATASETS_DIR}/generated_page"
GENERATED_PANELS_DIR = f"{DATASETS_DIR}/generated_panels"
GENERATED_PROMPS_DIR = f"{DATASETS_DIR}/generated_prompts"
PANELS_DIR = f"{DATASETS_DIR}/splited_panels"
PANELS_TEXT_DIR = f"{DATASETS_DIR}/panels_text"
PDF_DIR = f"{DATASETS_DIR}/pdf"


def load_pdf_from_local(folder_path: str):
    return [
        fitz.open(os.path.join(folder_path, filename))
        for filename in os.listdir(folder_path)
    ]


def load_images_from_local(folder_path: str):
    return [
        Image.open(os.path.join(folder_path, filename))
        for filename in os.listdir(folder_path)
    ]


def load_json_from_local(folder_path: str):
    return [
        json.load(open(os.path.join(folder_path, filename), "r"))
        for filename in os.listdir(folder_path)
    ]
