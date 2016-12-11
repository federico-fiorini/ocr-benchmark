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
    return os.path.join(app.config['UPLOAD_FOLDER'], filename)


def get_filename(filepath):
    """
    Return filename
    :param filepath:
    :return:
    """
    # Get filename
    return filepath.rsplit('/')[-1] if '/' in filepath else filepath


def delete_file(filename):
    """
    Helper function to delete a file
    :param filename:
    :return:
    """
    path = get_filepath(filename)
    if os.path.isfile(path):
        os.remove(path)


def perform_ocr(img):
    """
    Performs OCR on image and returns text
    :param img:
    :return: Text found in the image
    """
    # Check file path
    if img is None:
        return ""

    # Perform ocr and return result
    # img = img.convert('L')
    # sharpness = ImageEnhance.Sharpness(img)
    # img = sharpness.enhance(2.0)
    # contrast = ImageEnhance.Contrast(img)
    # img = contrast.enhance(1.5)
    return pytesseract.image_to_string(img)


def create_thumbnail(img):
    """
    Create thumbnail and return base-64 encoded
    :param img:
    :return:
    """
    # Check file path
    if img is None:
        return ""

    # Set thumbnail size
    size = 128, 128

    # Create thumbnail
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
