import cv2
import argparse
import numpy as np


DEFAULT_FORMAT = "png"

# local repo relatives paths
PDF_DIR = "datasets/pdf"
COMICS_PAGES_DIR = "datasets/pages"
PANELS_DIR = "datasets/panels"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("--process-comics", action="store_true")
    parser.add_argument("--process-pages", action="store_true")
    parser.add_argument("--input-directory", type=str, default=None)
    parser.add_argument("--output-directory", type=str, default=None)

    return parser.parse_args()


def save_images(
    images: list[np.ndarray],
    output_directory: str,
    document_title: str,
    image_type: str,
    format: str = DEFAULT_FORMAT,
) -> None:
    for i, img in enumerate(images):
        img_name = f"{document_title}{image_type}{i:02d}.{format}"
        img_full_path = f"{output_directory}/{img_name}"
        cv2.imwrite(img_full_path, img)
