import os
from images_preparation.pdf_preparations import cut_pdf
from images_preparation.panel_segmentation import cut_pages
from images_preparation.utils import parse_arguments


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
            cut_pages(args.input_directory, args.output_directory)
        elif args.input_directory:
            cut_pages(args.input_directory)
        elif args.output_directory:
            cut_pages(args.output_directory)
        else:
            cut_pages()


if __name__ == "__main__":
    main()
