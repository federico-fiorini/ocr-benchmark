from app import app
import pytesseract
from PIL import Image, ImageEnhance#, ImageFilter
import base64
import cStringIO
from werkzeug import secure_filename
import uuid
import os


def allowed_file(filename):
    """
    For a given file, return whether it's an allowed type or not
    :param filename:
    :return:
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def unique_filename(filename):
    """
    Generate unique filename
    :param filename:
    :return:
    """
    extension = filename.rsplit('.', 1)[1] if '.' in filename else 'jpeg'
    return secure_filename(str(uuid.uuid1()) + '.' + extension)


def get_filepath(filename):
    """
    Return filepath
    :param filename:
    :return:
    """
    # Build filepath
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Return None if it's not a file
    return filepath if os.path.isfile(filepath) else None


def delete_file(filename):
    """
    Helper function to delete a file
    :param filename:
    :return:
    """
    path = get_filepath(filename)
    if path is not None:
        os.remove(path)


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
    img = Image.open(img_path).convert('L')
    sharpness = ImageEnhance.Sharpness(img)
    img = sharpness.enhance(2.0)
    contrast = ImageEnhance.Contrast(img)
    img = contrast.enhance(1.5)
    return pytesseract.image_to_string(img)


def create_thumbnail(img_path):
    """
    Create thumbnail and return base-64 encoded
    :param img_path:
    :return:
    """
    # Check file path
    if img_path is None or img_path == "":
        return ""

    # Set thumbnail size
    size = 128, 128

    # Create thumbnail
    img = Image.open(img_path)
    img.thumbnail(size)

    return encode_base64(img)


def encode_base64(img):
    """
    Convert image object to base64 string
    :param img:
    :return:
    """
    # StringIO buffer
    buffer = cStringIO.StringIO()
    img.convert('RGB').save(buffer, format="JPEG")

    # Encode in base-64
    return base64.b64encode(buffer.getvalue())
