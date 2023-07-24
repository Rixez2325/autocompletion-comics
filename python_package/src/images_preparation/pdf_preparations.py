import os
import fitz
from fitz import Page, Document, Pixmap, Matrix, Rect
import numpy as np
from images_preparation.utils import save_images
from utils.path import PDF_DIR, COMICS_PAGES_DIR

OUTPUT_WIDTH = 600
IMAGE_TYPE = "_##_page_"


def cut_pdf(input_directory: str = PDF_DIR, output_directory: str = COMICS_PAGES_DIR):
    comics = os.listdir(input_directory)
    for comic in comics:
        comic_pages = process_pdf(f"{input_directory}/{comic}")
        save_images(comic_pages, output_directory, comic[:-4], IMAGE_TYPE)


def process_pdf(file_path: str) -> list[np.ndarray]:
    pdf: Document = fitz.open(file_path)
    pages = split_document(pdf)
    return to_ndarray(pages)


def get_title(file_path: str) -> str:
    return file_path.split("/")[-1].split(".")[-2]


def split_document(pdf_file: Document) -> list[Page]:
    return [pdf_file.load_page(i) for i in range(pdf_file.page_count)]


def get_zoom_matrix(bound: Rect) -> Matrix:
    zoom = OUTPUT_WIDTH / bound.width
    return fitz.Matrix(zoom, zoom)


def to_ndarray(pages: list[Page]) -> list[np.ndarray]:
    image_list = [page_to_ndarray(page) for page in pages]
    return image_list


def page_to_ndarray(page: Page) -> np.ndarray:
    zoom_matrix = get_zoom_matrix(page.bound())
    pix: Pixmap = page.get_pixmap(matrix=zoom_matrix)
    img = np.frombuffer(pix.samples, dtype=np.uint8)
    img = img.reshape((pix.height, pix.width, pix.n))
    return img
