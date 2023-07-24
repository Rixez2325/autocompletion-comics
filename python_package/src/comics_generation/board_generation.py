import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.utils import ImageReader

from utils.path import GENERATED_PAGE_DIR, GENERATED_PANELS_DIR


PANEL_WIDTH_MM = 91
PANEL_HEIGHT_MM = 133
PANEL_WIDTH_PX = 280
PANEL_HEIGHT_PX = 408
SPACING = 10


def create_pdf(
    generated_panels_path: str = GENERATED_PANELS_DIR,
    output_pdf: str = f"{GENERATED_PAGE_DIR}/result.pdf",
):
    panels = get_panels(generated_panels_path)

    pagesize = portrait(A4)

    c = canvas.Canvas(output_pdf, pagesize=pagesize)

    write_image(panels, pagesize, c)

    c.save()


def get_panels(dir_path: str) -> list:
    return [
        Image.open(os.path.join(dir_path, f))
        for f in os.listdir(dir_path)
        if os.path.isfile(os.path.join(dir_path, f))
    ]


def write_image(panels: list, pagesize, c: canvas.Canvas, columns: int = 2):
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


def demo():
    create_pdf()