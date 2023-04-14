import fitz
from fitz import Page, Document, Pixmap, Matrix, Rect

OUTPUT_WIDTH = 600


def main(file_path: str, output_directory: str) -> None:
    title = get_title(file_path)
    pdf: Document = fitz.open(file_path)
    pages = split_document(pdf)
    save_pages(pages, output_directory, title)


def get_title(file_path: str) -> str:
    return file_path.split("/")[-1].split(".")[-2]


def split_document(pdf_file: Document) -> list[Page]:
    return [pdf_file.load_page(i) for i in range(pdf_file.page_count)]


def get_zoom_matrix(bound: Rect) -> Matrix:
    zoom = OUTPUT_WIDTH / bound.width
    return fitz.Matrix(zoom, zoom)


def save_pages(
    pages: list[Page],
    output_directory: str,
    document_title: str,
    format: str = "png",
) -> None:
    for i, page in enumerate(pages):
        zoom_matrix = get_zoom_matrix(page.bound())
        img: Pixmap = page.get_pixmap(matrix=zoom_matrix)

        img_name = f"{document_title}_page_{i}.{format}"
        img_full_path = f"{output_directory}/{img_name}"
        img.save(img_full_path)


main(
    "datasets/comics_pdf/DC Marvel Comics - Batman & Spiderman.pdf",
    "datasets/comics_pages",
)
