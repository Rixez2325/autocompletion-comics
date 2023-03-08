# Manga/Comic Page Generator
This is a project that generates the next page of a manga/comic based on the text, style, and visual of the current page. The generation is done using Tesseract OCR, a GAN model, and a captioning model.

## How it works
The process of generating the next page of the manga/comic involves the following steps:

- Text Extraction: The text is extracted from the current page using Tesseract OCR. This text is then used as an input to the captioning model.
- Caption Generation: The captioning model takes in the text and generates a caption for the next page.
- Image Generation: The GAN model takes in the current page and the generated caption and generates an image that represents the next page of the manga/comic.
- The generated image is then displayed to the user.

## Requirements
The following packages are required to run the project:

 - Python 3.x
- TensorFlow
- NumPy
- Tesseract OCR
- OpenCV

## Installation
- Clone the repository: git clone https://github.com/Rixez2325/autocompletion-comics
- Install the required packages: pip install -r requirements.txt
- Download the trained models and put them in the models directory.


