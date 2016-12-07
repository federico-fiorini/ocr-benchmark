from app import app
import pytesseract
from PIL import Image#, ImageEnhance, ImageFilter
import base64
import cStringIO


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
    Create thumbnail and return base-64 encoded
    :param img_path:
    :return:
    """
    # Check file path
    if img_path is None or img_path == "":
        return None

    # Set thumbnail size
    size = 128, 128

    # Create thumbnail
    img = Image.open(img_path)
    img.thumbnail(size)

    # StringIO buffer
    buffer = cStringIO.StringIO()
    img.convert('RGB').save(buffer, format="JPEG")

    # Encode in base-64
    return base64.b64encode(buffer.getvalue())
