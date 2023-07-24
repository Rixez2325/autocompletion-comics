import argparse
from comics_generation.gpt_api import demo as gpt_demo, generate_prompts
from comics_generation.comic_diffusion import demo as diffusion_deom, generate_images
from comics_generation.board_generation import create_pdf


def main():
    args = parse_arguments()

    if args.demo:
        if args.process_gpt:
            gpt_demo()
        if args.process_diffusion:
            diffusion_deom()
        if args.process_pages:
            create_pdf()
    else:
        generate_prompts()
        generate_images()
        create_pdf()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--process-gpt", action="store_true")
    parser.add_argument("--process-page", action="store_true")
    parser.add_argument("--process-diffusion", action="store_true")

    return parser.parse_args()


if __name__ == "__main__":
    main()
