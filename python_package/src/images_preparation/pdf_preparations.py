import fitz
from fitz import Page, Document, Pixmap, Matrix, Rect
from PIL import Image
import numpy as np
from typing import List
from images_preparation.utils import save_images_localy
from helpers.aws_helper import load_pdf_from_s3, save_images_to_s3
from helpers.path_helper import PDF_DIR, COMICS_PAGES_DIR, load_pdf_from_local


OUTPUT_WIDTH = 600
IMAGE_TYPE = "_##_page_"


def cut_pdf(
    aws: bool = False,
    input_directory: str = PDF_DIR,
    output_directory: str = COMICS_PAGES_DIR,
):
    if aws:
        comics = load_pdf_from_s3(input_directory)
    else:
        comics = load_pdf_from_local(input_directory)

    for comic in comics:
        comic_pages = process_pdf(comic)
        if aws:
            comic_pages = [Image.fromarray(page) for page in comic_pages]
            save_images_to_s3(comic_pages, output_directory)
        else:
            comic_title = comic.name.split("\\")[-1][:-4]
            save_images_localy(comic_pages, output_directory, comic_title, IMAGE_TYPE)


def process_pdf(pdf: Document) -> List[np.ndarray]:
    pages = split_document(pdf)
    return to_ndarray(pages)


def get_title(file_path: str) -> str:
    return file_path.split("/")[-1].split(".")[-2]


def split_document(pdf_file: Document) -> List[Page]:
    return [pdf_file.load_page(i) for i in range(pdf_file.page_count)]


def get_zoom_matrix(bound: Rect) -> Matrix:
    zoom = OUTPUT_WIDTH / bound.width
    return fitz.Matrix(zoom, zoom)


def to_ndarray(pages: list[Page]) -> List[np.ndarray]:
    image_list = [page_to_ndarray(page) for page in pages]
    return image_list


def page_to_ndarray(page: Page) -> np.ndarray:
    zoom_matrix = get_zoom_matrix(page.bound())
    pix: Pixmap = page.get_pixmap(matrix=zoom_matrix)
    img = np.frombuffer(pix.samples, dtype=np.uint8)
    img = img.reshape((pix.height, pix.width, pix.n))
    return img
