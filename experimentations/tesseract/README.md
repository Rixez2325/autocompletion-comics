# Test with [Tesseract OCR](https://github.com/tesseract-ocr "Documentation")

Install can be made on **[WSL](https://learn.microsoft.com/fr-fr/windows/wsl/ "Documentation")**

* `sudo apt install tesseract-ocr`
* `sudo apt install libtesseract-dev`
* `sudo apt install python3-dev` -> to be able to install python requirements

___

It can be used with directly on the CLI, like so:
`tesseract imagename outputbase [-l lang]`

___

But also with a Python API, you can find a simple example realized with **[tesserocr](https://github.com/sirfz/tesserocr "Documentation")** in the file *[tesseract_test.py](tesseract_test.py "python file")*

Python requirements:

* `tesserocr==2.6.0`
