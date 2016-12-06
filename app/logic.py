from app import app
from app import mongo
from utils import perform_ocr
from utils import allowed_file
from werkzeug import secure_filename
import os


def login_user(username, password):
    """
    Check if username and password are correct
    :param username:
    :param password:
    :return:
    """

    # Find user and check password
    user = mongo.db.users.find_one({
        "username": username
    })

    return user is not None and user['password'] == password


def save_history(text):
    """
    Save ocr result to mongo
    :param text:
    :return:
    """
    mongo.db.history.insert_one({
        "text": text
    })


def save_and_get_text(files):
    """
    Save image, perform ocr, save result to mongo
    :param files:
    :return:
    """

    text = []

    for file in files:

        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)

            # Save file
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Perform ocr to get text
            result = perform_ocr(filepath)
            text.append(result)

    # Join in unique text
    text = "\n".join(text)

    # Save to mongo
    save_history(text)

    return text