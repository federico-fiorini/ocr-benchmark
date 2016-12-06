from app import app
import pytesseract
from PIL import Image#, ImageEnhance, ImageFilter


def allowed_file(filename):
    """
    For a given file, return whether it's an allowed type or not
    :param filename:
    :return:
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def perform_ocr(img_path):
    """
    Performs OCR on image and returns text
    :param img_path:
    :return: Text found in the image
    """
    # Check file path
    if img_path is None or img_path == "":
        return None

    # Perform ocr and return result
    img = Image.open(img_path)
    return pytesseract.image_to_string(img)


def create_thumbnail(img_path):
    """
    Create thumbnail
    :param img_path:
    :return:
    """
    # Check file path
    if img_path is None or img_path == "":
        return None

    # Set thumbnail size
    size = 128, 128

    # Create thumbnail and return it
    img = Image.open(img_path)
    img.thumbnail(size)
    return img