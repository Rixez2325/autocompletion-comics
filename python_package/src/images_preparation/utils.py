import cv2
import numpy as np
from typing import List


DEFAULT_FORMAT = "png"


def save_images_localy(
    images: List[np.ndarray],
    output_directory,
    document_title,
    image_type,
    format=DEFAULT_FORMAT,
) -> None:
    for i, img in enumerate(images):
        img_name = f"{document_title}{image_type}{i:02d}.{format}"
        img_full_path = f"{output_directory}/{img_name}"
        cv2.imwrite(img_full_path, img)
