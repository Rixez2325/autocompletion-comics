import os
from tesserocr import PyTessBaseAPI

images = os.listdir("inputs_images")

with PyTessBaseAPI() as api:
    for img in images:
        api.SetImageFile(f"inputs_images/{img}")
        print(api.GetUTF8Text())
        print(api.AllWordConfidences())
