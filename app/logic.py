from app import app
from bson import Binary
from utils import perform_ocr, allowed_file, create_thumbnail
from werkzeug import secure_filename
import os
from flask import session
from datetime import datetime
from models import Users, History


def login_user(username, password):
    """
    Check if username and password are correct
    :param username:
    :param password:
    :return:
    """

    # Find user and check password
    user = Users.get_user(username)

    is_correct = user is not None and user.password == password

    # Set session values
    session['logged_in'] = is_correct
    session['user'] = username if is_correct else None

    return is_correct


def save_history(text, thumbnail):
    """
    Save ocr result to mongo
    :param text:
    :param thumbnail:
    :return:
    """

    username = session['user']
    timestamp = str(datetime.now())

    # Create new history object
    new_history = History()
    new_history.user = username
    new_history.text = text
    new_history.thumbnail = Binary(thumbnail.tobytes())
    new_history.timestamp = timestamp

    # Save to mongo
    new_history.save()


def get_history():
    username = session['user']

    # Retrieve history for user
    history = History.get_history_by_user(username)
    return history



def save_and_get_text(files):
    """
    Save image, perform ocr, save result to mongo
    :param files:
    :return:
    """

    text = []
    first_filepath = ""

    for i, file in enumerate(files):

        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)

            # Save file
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            if i == 0:
                first_filepath = filepath

            # Perform ocr to get text
            result = perform_ocr(filepath)
            text.append(result)

    # Join in unique text
    text = "\n".join(text)

    # Create thumbnail of first image
    thumbnail = create_thumbnail(first_filepath)

    # Save to mongo
    save_history(text, thumbnail)

    return text
