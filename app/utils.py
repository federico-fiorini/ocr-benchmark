from app import app
import pytesseract
from PIL import Image#, ImageEnhance, ImageFilter


def perform_ocr(img_path):
    """
    Performs OCR on image and returns text
    :param img_path:
    :return: Text found in the image
    """
    img = Image.open(img_path)
    return pytesseract.image_to_string(img)


def allowed_file(filename):
    """
    For a given file, return whether it's an allowed type or not
    :param filename:
    :return:
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']