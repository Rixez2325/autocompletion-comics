import argparse
from panel_description.text_extraction import extract_panels_text_from_local, demo


def main():
    args = parse_arguments()

    if args.demo:
        demo()
    elif args.aws:
        pass  # TODO extract_bubbles_from_s3
    else:
        extract_panels_text_from_local()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("--aws", action="store_true")
    parser.add_argument("--demo", action="store_true")
    # TODO  constants or parameters ?
    parser.add_argument("--input-directory", type=str, default=None)
    parser.add_argument("--output-directory", type=str, default=None)

    return parser.parse_args()


if __name__ == "__main__":
    main()
