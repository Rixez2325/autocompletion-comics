import cv2
import numpy as np


DEFAULT_FORMAT = "png"


def save_pages(
    images: list[np.ndarray],
    output_directory: str,
    document_title: str,
    format: str = DEFAULT_FORMAT,
) -> None:
    for i, img in enumerate(images):
        img_name = f"{document_title}_##_page_##_{i:02d}.{format}"
        img_full_path = f"{output_directory}/{img_name}"
        cv2.imwrite(img_full_path, img)


def save_panels(
    images: list[np.ndarray],
    output_directory: str,
    document_title: str,
    format: str = DEFAULT_FORMAT,
) -> None:
    for i, img in enumerate(images):
        img_name = f"{document_title}_##_panel_##_{i:02d}.{format}"
        img_full_path = f"{output_directory}/{img_name}"
        cv2.imwrite(img_full_path, img)
