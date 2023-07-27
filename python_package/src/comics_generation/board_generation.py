import io
import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.utils import ImageReader
from typing import List

from helpers.path_helper import GENERATED_PAGE_DIR, GENERATED_PANELS_DIR
from helpers.aws_helper import (
    load_images_from_s3,
    get_s3_connection,
    S3_BUCKET,
    save_pdf_to_s3,
)


PANEL_WIDTH_MM = 91
PANEL_HEIGHT_MM = 133
PANEL_WIDTH_PX = 280  # 280
PANEL_HEIGHT_PX = 408  # 408
SPACING = 10


def create_pdf_demo(
    input_path: str = GENERATED_PANELS_DIR,
    output_pdf: str = f"{GENERATED_PAGE_DIR}/result.pdf",
):
    panels = get_panels_from_local(input_path)

    pagesize = portrait(A4)

    c = canvas.Canvas(output_pdf, pagesize=pagesize)

    write_image_in_pdf(panels, pagesize, c)

    c.save()


def create_pdf(
    input_path: str = GENERATED_PANELS_DIR,
    output_path: str = f"{GENERATED_PAGE_DIR}",
):
    panels = load_images_from_s3(input_path)

    pagesize = portrait(A4)

    buffer = io.BytesIO()

    c = canvas.Canvas(buffer, pagesize=pagesize)

    write_image_in_pdf(panels, pagesize, c)
    c.save()
    buffer.seek(0)

    save_pdf_to_s3([buffer], output_path)


def get_panels_from_local(dir_path: str) -> List:
    return [
        Image.open(os.path.join(dir_path, f))
        for f in os.listdir(dir_path)
        if os.path.isfile(os.path.join(dir_path, f))
    ]


def write_image_in_pdf(panels: list, pagesize, c: canvas.Canvas, columns: int = 2):
    for i, img in enumerate(panels):
        img_reader = ImageReader(img)

        # Calculate the position of the image in the grid
        row = i // columns
        column = i % columns
        x = SPACING + column * (PANEL_WIDTH_PX + SPACING)
        y = pagesize[1] - SPACING - (row + 1) * (PANEL_HEIGHT_PX + SPACING)

        # Resize the image to fit the cell
        img = img.resize((int(PANEL_WIDTH_MM), int(PANEL_HEIGHT_MM)), Image.ANTIALIAS)

        # Add the image to the PDF
        try:
            img_reader = ImageReader(img)
            c.drawImage(img_reader, x, y, width=PANEL_WIDTH_PX, height=PANEL_HEIGHT_PX)
        except Exception as e:
            print(str(e))
            continue
