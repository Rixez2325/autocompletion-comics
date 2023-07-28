import argparse
from images_preparation.pdf_preparations import cut_pdf
from images_preparation.panel_segmentation import cut_pages


def main(aws: bool = False):
    if aws:
        cut_pages(aws)
    else:
        args = parse_arguments()

        if args.process_comics:
            cut_pdf()
        if args.process_pages:
            cut_pages()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--aws", action="store_true")
    parser.add_argument("--process-comics", action="store_true")
    parser.add_argument("--process-pages", action="store_true")

    return parser.parse_args()


if __name__ == "__main__":
    main()
