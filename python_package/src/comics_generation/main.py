import argparse
from comics_generation.gpt_api import gpt_demo, generate_prompts
from comics_generation.comic_diffusion import diffusion_demo, generate_images
from comics_generation.board_generation import create_pdf_demo, create_pdf


def main(aws: bool = False):
    if aws:
        # generate_prompts()
        generate_images()
        create_pdf()
    else:
        args = parse_arguments()

        if args.process_gpt:
            gpt_demo()
        if args.process_diffusion:
            diffusion_demo()
        if args.process_page:
            create_pdf_demo()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--process-gpt", action="store_true")
    parser.add_argument("--process-page", action="store_true")
    parser.add_argument("--process-diffusion", action="store_true")

    return parser.parse_args()


if __name__ == "__main__":
    main()
