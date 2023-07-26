import argparse

from images_preparation.main import main as images_preparation
from panel_description.main import main as panel_description
from comics_generation.main import main as comics_generation


def main():
    args = parse_arguments()

    if args.aws:
        images_preparation(args.aws)
        panel_description(args.aws)
        comics_generation(False, args.aws)
    elif args.local:
        images_preparation()
        panel_description()
        comics_generation(args.local, False)
    else:
        return "Wrong arguments"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--aws", action="store_true")
    parser.add_argument("--local", action="store_true")

    return parser.parse_args()


if __name__ == "__main__":
    main()
