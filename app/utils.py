import pytesseract
from PIL import Image#, ImageEnhance, ImageFilter


def ocr(img_path):
    """
    Performs OCR on image and returns text
    :param img_path:
    :return: Text found in the image
    """
    img = Image.open(img_path)
    return pytesseract.image_to_string(img)
