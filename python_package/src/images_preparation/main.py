import os
from images_preparation.pdf_preparations import process_pdf
from images_preparation.panel_segmentation import process_page
from images_preparation.utils import save_pages, save_panels, parse_arguments


# local repo relatives paths
PDF_DIR = "datasets/pdf"
COMICS_PAGES_DIR = "datasets/pages"
PANELS_DIR = "datasets/panels"


def main():
    args = parse_arguments()

    if args.process_comics:
        if args.input_directory and args.output_directory:
            cut_pdf(args.input_directory, args.output_directory)
        elif args.input_directory:
            cut_pdf(args.input_directory)
        elif args.output_directory:
            cut_pdf(args.output_directory)
        else:
            cut_pdf()

    if args.process_pages:
        if args.input_directory and args.output_directory:
            cut_panels(args.input_directory, args.output_directory)
        elif args.input_directory:
            cut_panels(args.input_directory)
        elif args.output_directory:
            cut_panels(args.output_directory)
        else:
            cut_panels()


def cut_pdf(input_directory: str = PDF_DIR, output_directory: str = COMICS_PAGES_DIR):
    comics = os.listdir(input_directory)
    for comic in comics:
        comic_pages = process_pdf(f"{input_directory}/{comic}")
        save_pages(comic_pages, output_directory, comic[:-4])


def cut_panels(
    input_directory: str = COMICS_PAGES_DIR, output_directory: str = PANELS_DIR
):
    pages = os.listdir(input_directory)
    for page in pages:
        panels = process_page(f"{input_directory}/{page}")
        save_panels(panels, output_directory, page[:-4])


if __name__ == "__main__":
    main()
