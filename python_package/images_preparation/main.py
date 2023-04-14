import os
from pdf_preparations import process_pdf
from panel_segmentation import process_page
from utils import save_pages, save_panels


COMICS_PDF_DIR = "datasets/comics_pdf"
COMICS_PAGES_DIR = "datasets/comics_pages"
PANELS_DIR = "datasets/panels"


def main():
    comics = os.listdir(COMICS_PDF_DIR)
    for comic in comics:
        comic_pages = process_pdf(f"{COMICS_PDF_DIR}/{comic}")
        save_pages(comic_pages, COMICS_PAGES_DIR, comic[:-4])

    pages = os.listdir(COMICS_PAGES_DIR)
    for page in pages:
        panels = process_page(f"{COMICS_PAGES_DIR}/{page}")
        save_panels(panels, PANELS_DIR, page[:-4])


if __name__ == "__main__":
    main()
